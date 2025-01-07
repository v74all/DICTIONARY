import numpy as np
from typing import List, Dict
import os
import gzip
import logging
import random
from tqdm import tqdm
from utils import generate_password_list
from zxcvbn import zxcvbn
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Embedding, Dropout, Bidirectional, Conv1D
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

class DictionaryGenerator:
    def __init__(self, base_datasets: List[str] = None, model_path="password_model.keras"):
        self.base_passwords = []
        if base_datasets:
            for dataset in base_datasets:
                self.base_passwords.extend(self.load_dataset(dataset))
        self.model_path = model_path
        self.char_to_idx = {}
        self.idx_to_char = {}
        self.model = None
        self.max_sequence_length = 32  
        self.vocab_size = 256 
        
        all_chars = set(''.join([chr(i) for i in range(32, 127)])) 
        self.char_to_idx = {char: idx for idx, char in enumerate(sorted(all_chars))}
        self.idx_to_char = {idx: char for char, idx in self.char_to_idx.items()}

        self.min_password_length = 8
        self.char_embedding_size = 256
        self.pattern_memory = {}

    def load_dataset(self, file_path: str) -> List[str]:
        try:
            if not file_path:
                return []
            with open(file_path, 'r', encoding='utf-8') as file:
                return [line.strip() for line in file.readlines() if line.strip()]
        except Exception as e:
            logging.error(f"Error loading dataset {file_path}: {e}")
            return []

    def sanitize_user_info(self, user_info: List[str]) -> List[str]:
        sanitized = []
        for info in user_info:
            if info.startswith('<') and info.endswith('>'):
                continue
            clean_info = ''.join(e for e in info if e.isalnum() or e in ['_', '-', '@'])
            sanitized.append(clean_info)
        return sanitized

    def preprocess_data(self):
        if not self.base_passwords:
            self.base_passwords = generate_password_list(8, 16, 1000)

        sequences = []
        next_chars = []
        
        for password in self.base_passwords:
            for i in range(len(password)):
                seq = password[max(0, i-self.max_sequence_length+1):i+1]
                seq = seq.ljust(self.max_sequence_length)[:self.max_sequence_length]
                sequences.append(seq)
                
                next_char = password[i+1] if i+1 < len(password) else '\0'
                next_chars.append(next_char)

        X = np.zeros((len(sequences), self.max_sequence_length, len(self.char_to_idx)), dtype=np.float32)
        y = np.zeros((len(sequences), len(self.char_to_idx)), dtype=np.float32)
        
        for i, (sequence, next_char) in enumerate(zip(sequences, next_chars)):
            for t, char in enumerate(sequence):
                if char in self.char_to_idx:
                    X[i, t, self.char_to_idx[char]] = 1.0
            if next_char in self.char_to_idx:
                y[i, self.char_to_idx[next_char]] = 1.0

        return X, y, len(self.char_to_idx)

    def create_model(self, vocab_size):
        model = Sequential([
            Embedding(vocab_size, self.char_embedding_size, 
                     input_length=self.max_sequence_length),
            Bidirectional(LSTM(256, return_sequences=True)),
            Dropout(0.2),
            Bidirectional(LSTM(128, return_sequences=True)),
            Dropout(0.2),
            Bidirectional(LSTM(64)),
            Dropout(0.2),
            Dense(128, activation='relu'),
            Dense(vocab_size, activation='softmax')
        ])
        
        model.compile(
            loss='categorical_crossentropy',
            optimizer='adam',
            metrics=['accuracy']
        )
        return model

    def train_model(self):
        try:
            X, y, vocab_size = self.preprocess_data()
            if X is None or len(X) == 0:
                logging.error("No training data available")
                return False

            model = self.create_model(vocab_size)
            
            callbacks = [
                EarlyStopping(
                    monitor='val_loss',
                    patience=3,
                    restore_best_weights=True
                ),
                ModelCheckpoint(
                    self.model_path,
                    monitor='val_loss',
                    save_best_weights_only=True
                )
            ]

            model.fit(
                X, y,
                batch_size=32,
                epochs=50,
                validation_split=0.2,
                callbacks=callbacks,
                verbose=1
            )

            self.model = model
            model.save(self.model_path)
            
            return True
            
        except Exception as e:
            logging.error(f"Model training failed: {str(e)}")
            return False

    def load_or_train_model(self):
        try:
            if os.path.exists(self.model_path):
                logging.info("Loading existing model...")
                self.model = load_model(self.model_path)
                return True
            else:
                logging.info("No existing model found. Training new model...")
                return self.train_model()
        except Exception as e:
            logging.error(f"Error loading/training model: {e}")
            return False

    def generate_passwords_with_model(self, seed_text: str, num_passwords: int = 10, max_length: int = 16) -> List[str]:
        if not self.model:
            return []

        passwords = []
        for _ in tqdm(range(num_passwords)):
            current = seed_text[:self.max_sequence_length]
            current = current.ljust(self.max_sequence_length)[:self.max_sequence_length]
            
            password = seed_text
            
            while len(password) < max_length:
                x_pred = np.zeros((1, self.max_sequence_length, len(self.char_to_idx)))
                for t, char in enumerate(current):
                    if char in self.char_to_idx:
                        x_pred[0, t, self.char_to_idx[char]] = 1.0

                preds = self.model.predict(x_pred, verbose=0)[0]
                next_index = np.random.choice(len(preds), p=preds)
                next_char = self.idx_to_char[next_index]

                if next_char == '\0' or len(password) >= max_length:
                    break

                password += next_char
                current = password[-self.max_sequence_length:]
                current = current.ljust(self.max_sequence_length)[:self.max_sequence_length]

            if len(password) >= self.min_password_length:
                passwords.append(password)

        return passwords

    def generate_patterns(self, user_info: List[str]) -> List[str]:
        patterns = []
        for word in user_info:
            if not word:
                continue
            patterns.append(word.lower())
            patterns.append(word.upper())
            patterns.append(word.capitalize())
            patterns.extend([f"{word}{str(i)}" for i in range(100)])
            subs = {'a':'@', 'e':'3', 'i':'1', 'o':'0', 's':'$'}
            modified = word.lower()
            for char, repl in subs.items():
                if char in modified:
                    patterns.append(modified.replace(char, repl))
        
        valid_info = [word for word in user_info if word]
        for i in range(len(valid_info)):
            for j in range(i + 1, len(valid_info)):
                patterns.append(f"{valid_info[i]}{valid_info[j]}")
                patterns.append(f"{valid_info[i]}_{valid_info[j]}")
                patterns.append(f"{valid_info[i]}-{valid_info[j]}")
                
        return list(set(patterns))

    def apply_combination_method(self, word: str, method: str) -> List[str]:
        results = []
        years = range(1960, 2024)
        common_numbers = ['123', '1234', '12345', '111', '000', '666', '777', '888', '999']
        special_chars = ['!', '@', '#', '$', '%', '&', '*', '?', '.', '-', '_', '+']
        
        if method == 'basic':
            word_variations = [
                word.lower(), word.upper(), word.capitalize(),
                word.title(), word.lower()[::-1],
            ]
            
            for variation in word_variations:
                results.append(variation)
                results.extend([f"{variation}{year}" for year in years])
                results.extend([f"{variation}{num}" for num in common_numbers])
                results.extend([f"{variation}{char}" for char in special_chars])
                
        elif method == 'advanced':
            base_forms = [word.lower(), word.capitalize()]
            for base in base_forms:
                for char in special_chars:
                    for i in range(100):
                        results.append(f"{base}{char}{i:02d}")
                        results.append(f"{base}{i:02d}{char}")
                        results.append(f"{char}{base}{i:02d}")
                
                for year in years:
                    results.append(f"{base}{year}")
                    for char in special_chars[:4]:
                        results.append(f"{base}{char}{year}")
                        results.append(f"{base}{year}{char}")
                
        elif method == 'complex':
            l33t_map = {
                'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$',
                't': '7', 'b': '8', 'g': '9', 'l': '1', 'z': '2'
            }
            
            l33t_variations = []
            word_lower = word.lower()
            
            from itertools import combinations
            chars_to_replace = [c for c in word_lower if c in l33t_map]
            
            for r in range(len(chars_to_replace) + 1):
                for combo in combinations(chars_to_replace, r):
                    temp_word = word_lower
                    for char in combo:
                        temp_word = temp_word.replace(char, l33t_map[char])
                    l33t_variations.append(temp_word)
            
            for variation in l33t_variations:
                results.append(variation)
                results.extend([f"{variation}{year}" for year in years])
                for char in special_chars:
                    results.append(f"{variation}{char}")
                    for num in common_numbers:
                        results.append(f"{variation}{char}{num}")
                        results.append(f"{variation}{num}{char}")
            
        elif method == 'l33t':
            l33t_advanced = {
                'a': ['@', '4'], 'e': ['3'], 'i': ['1', '!'],
                'o': ['0'], 's': ['$', '5'], 't': ['7', '+'],
                'b': ['8'], 'g': ['9'], 'l': ['1'], 'z': ['2'],
                'h': ['#'], 'x': ['*'], 'c': ['(', '{'],
                'n': ['^'], 'w': ['uu', 'vv'], 'v': ['\\/'],
                'm': ['nn'], 'k': ['|<'], 'd': ['|)']
            }
            
            def generate_l33t_variations(text, pos=0, current=''):
                if pos == len(text):
                    results.append(current)
                    return
                
                char = text[pos].lower()
                if char in l33t_advanced:
                    for replacement in l33t_advanced[char]:
                        generate_l33t_variations(text, pos + 1, current + replacement)
                    generate_l33t_variations(text, pos + 1, current + char)
                else:
                    generate_l33t_variations(text, pos + 1, current + char)
            
            generate_l33t_variations(word)
            
            base_results = results.copy()
            for base in base_results:
                for year in years:
                    results.append(f"{base}{year}")
                for num in common_numbers:
                    results.append(f"{base}{num}")
            
        elif method == 'custom':
            pass
        
        contextual_suffixes = [
            '123', '1234', '12345', 'abc', 'xyz', 'qwerty',
            '111', '000', '!@#', '$%^', '...', '___',
            'pass', 'pwd', 'password'
        ]
        
        base_results = results.copy()
        for base in base_results:
            results.extend([f"{base}{suffix}" for suffix in contextual_suffixes])
        
        results = [p for p in results if len(p) >= 8]
        
        seen = set()
        return [x for x in results if not (x in seen or seen.add(x))]

    def generate_personalized_list(self, user_data: Dict[str, List[str]], max_combinations: int = 100000, 
                                 use_ml: bool = False,
                                 combination_method: str = 'basic',
                                 custom_pattern: str = '',
                                 min_length: int = 8) -> List[str]:
        user_info = [item for sublist in user_data.values() for item in sublist]
        user_info = self.sanitize_user_info(user_info)
        
        passwords = []
        
        for word in user_info:
            if combination_method == 'random':
                methods = ['basic', 'advanced', 'complex', 'l33t']
                method = random.choice(methods)
                passwords.extend(self.apply_combination_method(word, method))
            elif combination_method == 'custom' and custom_pattern:
                pattern = custom_pattern
                pattern = pattern.replace('[word]', word)
                pattern = pattern.replace('[name]', word.capitalize())
                pattern = pattern.replace('[number]', str(random.randint(0, 999)))
                pattern = pattern.replace('[symbol]', random.choice('!@#$%&*'))
                passwords.append(pattern)
            else:
                passwords.extend(self.apply_combination_method(word, combination_method))

        pattern_passwords = self.generate_patterns(user_info)
        passwords.extend(pattern_passwords)
        
        if use_ml and self.model and user_info:
            model_passwords = self.generate_passwords_with_model(user_info[0])
            passwords.extend(model_passwords)
        
        related_combinations = []
        words = user_info.copy()
        
        for i in range(len(words)):
            for j in range(i + 1, len(words)):
                word1, word2 = words[i], words[j]
                related_combinations.extend([
                    f"{word1}{word2}",
                    f"{word1}_{word2}",
                    f"{word1.capitalize()}{word2}",
                    f"{word1[:3]}{word2[:3]}",
                    f"{word1}{word2[:3]}",
                    f"{word1[:1]}{word2}"
                ])

        passwords.extend(related_combinations)

        for word in user_info:
            if len(word) >= 3:
                transformations = [
                    word * 2,
                    word + word[::-1],
                    ''.join([c * 2 for c in word]),
                    ''.join(c if i % 2 == 0 else c.upper() for i, c in enumerate(word.lower()))
                ]
                passwords.extend(transformations)

        unique_passwords = list(dict.fromkeys(passwords))[:max_combinations]
        
        strong_passwords = [pwd for pwd in unique_passwords if self.is_strong_password(pwd) and len(pwd) >= min_length]
        
        return strong_passwords

    def save_to_file(self, password_list: List[str], file_name: str, compress: bool = False):
        filtered_passwords = [pwd for pwd in password_list if "<SPORTS_TEAM/HOBBY>" not in pwd]
        try:
            if compress:
                with gzip.open(file_name + '.gz', 'wt', encoding='utf-8') as file:
                    for password in filtered_passwords:
                        file.write(f"{password}\n")
            else:
                with open(file_name, 'w', encoding='utf-8') as file:
                    for password in filtered_passwords:
                        file.write(f"{password}\n")
        except IOError as e:
            logging.error(f"Error saving file {file_name}: {e}")

    def is_strong_password(self, password: str) -> bool:
        result = zxcvbn(password)
        return result['score'] >= 3
