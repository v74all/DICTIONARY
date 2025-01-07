import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QTextEdit, QFileDialog, QCheckBox, QLineEdit, QMessageBox, QDialog, QSizePolicy, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from generator import DictionaryGenerator
import logging
from translations import TRANSLATIONS

class HelpDialog(QDialog):
    def __init__(self, parent=None, help_text=""):
        super().__init__(parent)
        self.setWindowTitle(parent.tr(parent.current_language, 'help_title'))
        self.setGeometry(200, 200, 600, 400)
        
        layout = QVBoxLayout()
        
        help_content = QTextEdit()
        help_content.setReadOnly(True)
        help_content.setPlainText(help_text)
        help_content.setStyleSheet("""
            QTextEdit {
                background-color: #000000;
                color: #00ff00;
                border: 1px solid #00ff00;
                font-family: 'Courier';
                padding: 10px;
            }
        """)
        
        layout.addWidget(help_content)
        self.setLayout(layout)

class PasswordGeneratorGUI(QMainWindow):
    VERSION = "v1.5 Beta"
    
    def __init__(self):
        super().__init__()
        self.current_language = 'en'
        self.translations = TRANSLATIONS
        self.initUI()
        self.add_version_label()

    def initUI(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
            }
            QWidget {
                background-color: #1a1a1a;
                color: #00ff00;
                font-family: 'Courier';
            }
            QLabel {
                color: #00ff00;
                font-weight: bold;
                font-size: 12px;
            }
            QTextEdit, QLineEdit {
                background-color: #000000;
                border: 1px solid #00ff00;
                color: #00ff00;
                font-family: 'Courier';
                padding: 5px;
            }
            QPushButton {
                background-color: #000000;
                color: #00ff00;
                border: 1px solid #00ff00;
                padding: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00ff00;
                color: #000000;
            }
            QCheckBox {
                color: #00ff00;
            }
            QCheckBox::indicator {
                border: 1px solid #00ff00;
            }
            QCheckBox::indicator:checked {
                background-color: #00ff00;
            }
        """)
        
        self.setWindowTitle(self.tr(self.current_language, 'title'))
        self.setGeometry(100, 100, 900, 700)

        self.languageButton = QPushButton(self.translations[self.current_language]['language_button'])
        self.languageButton.clicked.connect(self.toggleLanguage)
        
        layout = QVBoxLayout()
        layout.setSizeConstraint(QVBoxLayout.SetDefaultConstraint)
        
        top_buttons = QHBoxLayout()
        top_buttons.addWidget(self.languageButton)
        
        self.helpButton = QPushButton(self.tr(self.current_language, 'help_button'))
        self.helpButton.clicked.connect(self.showHelp)
        top_buttons.addWidget(self.helpButton)
        
        layout.addLayout(top_buttons)

        header = QLabel(self.tr(self.current_language, 'header'))
        header.setFont(QFont('Courier', 10))
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        self.userDataLabel = QLabel(self.tr(self.current_language, 'user_data_label'))
        layout.addWidget(self.userDataLabel)

        self.userDataInput = QTextEdit()
        layout.addWidget(self.userDataInput)

        user_data_methods = QHBoxLayout()
        
        self.loadUserDataButton = QPushButton("Load from File")
        self.loadUserDataButton.clicked.connect(self.loadUserDataFromFile)
        user_data_methods.addWidget(self.loadUserDataButton)
        
        self.clearUserDataButton = QPushButton("Clear")
        self.clearUserDataButton.clicked.connect(self.userDataInput.clear)
        user_data_methods.addWidget(self.clearUserDataButton)
        
        layout.insertLayout(layout.indexOf(self.userDataInput) + 1, user_data_methods)

        example_text = """Enter information manually or load from file. Examples:

1. JSON Format:
{
    "name": ["John", "Johnny"],
    "birthdate": ["1990-05-15"],
    "phone": ["1234567890"],
    "email": ["john@example.com"]
}

2. Simple Format:
name:John, name:Johnny
birthdate:1990-05-15
phone:1234567890
email:john@example.com

3. Free Text Format:
Just type any information you know:
- Names
- Dates
- Phone numbers
- Email addresses
- Usernames
- Hobbies
- Pet names
- etc."""

        self.userDataInput.setPlaceholderText(example_text)

        self.datasetLabel = QLabel(self.tr(self.current_language, 'datasets_label'))
        layout.addWidget(self.datasetLabel)

        self.datasetInput = QLineEdit()
        layout.addWidget(self.datasetInput)

        self.browseButton = QPushButton(self.tr(self.current_language, 'browse_button'))
        self.browseButton.clicked.connect(self.browseDatasets)
        layout.addWidget(self.browseButton)

        self.maxLabel = QLabel(self.tr(self.current_language, 'max_combinations'))
        layout.addWidget(self.maxLabel)

        self.maxInput = QLineEdit('100000')
        layout.addWidget(self.maxInput)

        self.minLengthLabel = QLabel("Min Password Length:")
        layout.addWidget(self.minLengthLabel)

        self.minLengthInput = QLineEdit('6')
        layout.addWidget(self.minLengthInput)

        self.useMLCheckBox = QCheckBox(self.tr(self.current_language, 'use_ml'))
        layout.addWidget(self.useMLCheckBox)

        self.compressCheckBox = QCheckBox(self.tr(self.current_language, 'compress_output'))
        layout.addWidget(self.compressCheckBox)

        self.estimateSizeCheckBox = QCheckBox(self.tr(self.current_language, 'estimate_size'))
        layout.addWidget(self.estimateSizeCheckBox)

        self.outputFileLabel = QLabel(self.tr(self.current_language, 'output_file_label'))
        layout.addWidget(self.outputFileLabel)

        self.outputFileInput = QLineEdit('generated_passwords.txt')
        layout.addWidget(self.outputFileInput)

        self.syncCheckBox = QCheckBox(self.tr(self.current_language, 'sync'))
        layout.addWidget(self.syncCheckBox)

        self.verboseCheckBox = QCheckBox(self.tr(self.current_language, 'verbose'))
        layout.addWidget(self.verboseCheckBox)

        self.combinationLabel = QLabel(self.tr(self.current_language, 'combination_label'))
        layout.addWidget(self.combinationLabel)

        self.combinationSelect = QComboBox()
        for key, value in self.translations[self.current_language]['combination_options'].items():
            self.combinationSelect.addItem(value, key)
        layout.addWidget(self.combinationSelect)

        self.patternLabel = QLabel(self.tr(self.current_language, 'pattern_label'))
        self.patternLabel.hide()
        layout.addWidget(self.patternLabel)

        self.patternInput = QLineEdit()
        self.patternInput.setPlaceholderText(self.tr(self.current_language, 'pattern_placeholder'))
        self.patternInput.hide()
        layout.addWidget(self.patternInput)

        self.combinationSelect.currentIndexChanged.connect(self.onCombinationMethodChanged)

        self.generateButton = QPushButton(self.tr(self.current_language, 'generate_button'))
        self.generateButton.clicked.connect(self.generatePasswords)
        layout.addWidget(self.generateButton)

        self.outputLabel = QLabel(self.tr(self.current_language, 'output_label'))
        layout.addWidget(self.outputLabel)

        self.outputDisplay = QTextEdit()
        self.outputDisplay.setReadOnly(True)
        layout.addWidget(self.outputDisplay)

        footer = QLabel(self.tr(self.current_language, 'footer'))
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer)

        container = QWidget()
        container.setLayout(layout)
        container.setMinimumWidth(500)
        container.setMinimumHeight(400)

        self.setCentralWidget(container)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def add_version_label(self):
        version_label = QLabel(f"Version {self.VERSION}")
        version_label.setStyleSheet("""
            QLabel {
                color: #32CD32;
                font-size: 10px;
                font-style: italic;
                padding: 2px;
            }
        """)
        version_label.setAlignment(Qt.AlignRight)
        self.statusBar().addPermanentWidget(version_label)

    def browseDatasets(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Select Dataset Files", "", "Text Files (*.txt);;All Files (*)", options=options)
        if files:
            self.datasetInput.setText(';'.join(files))

    def generatePasswords(self):
        if not self.validateInputs():
            return
            
        try:
            self.outputDisplay.clear()
            self.outputDisplay.append("Starting password generation process...")
            QApplication.processEvents()

            if not self.validateInputs():
                return

            user_data = self.userDataInput.toPlainText()
            datasets = [ds.strip() for ds in self.datasetInput.text().split(';') if ds.strip()]
            max_combinations = int(self.maxInput.text())
            use_ml = self.useMLCheckBox.isChecked()
            compress_output = self.compressCheckBox.isChecked()
            output_file = self.outputFileInput.text()
            min_length = int(self.minLengthInput.text())

            combination_method = self.combinationSelect.currentData()
            custom_pattern = self.patternInput.text() if combination_method == 'custom' else ''

            if self.estimateSizeCheckBox.isChecked():
                self.estimatePasswordListSize(user_data, max_combinations)
                return

            self.outputDisplay.append("Initializing password generator...")
            QApplication.processEvents()
            
            generator = DictionaryGenerator(base_datasets=datasets)
            
            if use_ml:
                self.outputDisplay.append("Loading/training ML model...")
                QApplication.processEvents()
                generator.load_or_train_model()

            user_data_dict = self.process_user_input(user_data)
            if not user_data_dict:
                QMessageBox.warning(self, "Warning", "No valid user data provided.")
                return

            self.outputDisplay.append("Generating passwords...")
            QApplication.processEvents()
            
            passwords = generator.generate_personalized_list(
                user_data=user_data_dict,
                max_combinations=max_combinations,
                use_ml=use_ml,
                combination_method=combination_method,
                custom_pattern=custom_pattern,
                min_length=min_length
            )

            if passwords:
                generator.save_to_file(passwords, output_file, compress=compress_output)
                self.outputDisplay.clear()
                self.outputDisplay.append(f"Generated {len(passwords)} passwords.")
                self.outputDisplay.append("\nSample passwords:")
                for pwd in passwords[:10]:
                    self.outputDisplay.append(pwd)
                self.outputDisplay.append(f"\nAll passwords saved to: {output_file}")
                
                if compress_output:
                    self.outputDisplay.append(f"File has been compressed as: {output_file}.gz")
            else:
                self.outputDisplay.append("No passwords were generated.")

        except Exception as e:
            logging.error(f"Error generating passwords: {e}")
            QMessageBox.critical(
                self,
                self.tr(self.current_language, 'error_title'),
                f"{self.tr(self.current_language, 'error_message')} {str(e)}"
            )

    def validateInputs(self) -> bool:
        try:
            if not self.userDataInput.toPlainText().strip():
                QMessageBox.warning(self, "Validation Error", "Please enter user data.")
                return False

            try:
                max_combinations = int(self.maxInput.text())
                if max_combinations <= 0:
                    raise ValueError("Maximum combinations must be positive")
            except ValueError:
                QMessageBox.warning(self, "Validation Error", "Please enter a valid number for maximum combinations.")
                return False

            try:
                min_length = int(self.minLengthInput.text())
                if min_length < 6:
                    raise ValueError("Minimum length must be at least 6")
            except ValueError:
                QMessageBox.warning(self, "Validation Error", "Please enter a valid number for minimum length.")
                return False

            if self.useMLCheckBox.isChecked():
                try:
                    import tensorflow as tf
                    if not tf.test.is_built_with_cuda():
                        QMessageBox.warning(self, "Warning", "ML enabled but CUDA not available. Processing may be slower.")
                except ImportError:
                    QMessageBox.critical(self, "Error", "TensorFlow not available. ML functions disabled.")
                    self.useMLCheckBox.setChecked(False)
                    return False

            return True
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Validation error: {str(e)}")
            return False

    def estimatePasswordListSize(self, user_data: str, max_combinations: int):
        try:
            user_data_dict = self.process_user_input(user_data)
            if not user_data_dict:
                QMessageBox.warning(self, "Warning", "No valid user data provided for estimation.")
                return

            generator = DictionaryGenerator()
            estimated_size = generator.estimate_size(user_data_dict, max_combinations)
            
            self.outputDisplay.clear()
            self.outputDisplay.append(f"Estimated password list size: {estimated_size:,} passwords")
            
            if estimated_size > 1000000:
                self.outputDisplay.append("\nWarning: Large password list may require significant time and resources.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to estimate size: {str(e)}")

    def showHelp(self):
        help_dialog = HelpDialog(self, self.tr(self.current_language, 'help_text'))
        help_dialog.exec_()

    def toggleLanguage(self):
        self.current_language = 'fa' if self.current_language == 'en' else 'en'
        self.updateTranslations()

    def updateTranslations(self):
        self.setWindowTitle(self.tr(self.current_language, 'title'))
        self.languageButton.setText(self.tr(self.current_language, 'language_button'))
        self.userDataLabel.setText(self.tr(self.current_language, 'user_data_label'))
        self.datasetLabel.setText(self.tr(self.current_language, 'datasets_label'))
        self.browseButton.setText(self.tr(self.current_language, 'browse_button'))
        self.maxLabel.setText(self.tr(self.current_language, 'max_combinations'))
        self.useMLCheckBox.setText(self.tr(self.current_language, 'use_ml'))
        self.compressCheckBox.setText(self.tr(self.current_language, 'compress_output'))
        self.estimateSizeCheckBox.setText(self.tr(self.current_language, 'estimate_size'))
        self.generateButton.setText(self.tr(self.current_language, 'generate_button'))
        self.outputLabel.setText(self.tr(self.current_language, 'output_label'))
        self.helpButton.setText(self.tr(self.current_language, 'help_button'))
        self.outputFileLabel.setText(self.tr(self.current_language, 'output_file_label'))
        self.syncCheckBox.setText(self.tr(self.current_language, 'sync'))
        self.verboseCheckBox.setText(self.tr(self.current_language, 'verbose'))
        self.combinationLabel.setText(self.tr(self.current_language, 'combination_label'))
        self.patternLabel.setText(self.tr(self.current_language, 'pattern_label'))
        self.patternInput.setPlaceholderText(self.tr(self.current_language, 'pattern_placeholder'))

    def tr(self, language: str, key: str) -> str:
        return self.translations[language].get(key, key)

    def loadUserDataFromFile(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Select User Data File",
                "",
                "Text Files (*.txt);;All Files (*)"
            )
            
            if file_path:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.userDataInput.setText(content)
                    self.outputDisplay.append(f"Loaded user data from: {file_path}")
                    
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to load user data file: {str(e)}"
            )

    def process_user_input(self, input_text: str) -> dict:
        try:
            import json
            return json.loads(input_text)
        except json.JSONDecodeError:
            data = {}
            
            lines = input_text.split('\n')
            current_category = 'general'
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    if key not in data:
                        data[key] = []
                    data[key].append(value)
                    
                else:
                    if 'general' not in data:
                        data['general'] = []
                    data['general'].append(line)
            
            return data

    def onCombinationMethodChanged(self, index):
        method = self.combinationSelect.currentData()
        if (method == 'custom'):
            self.patternLabel.show()
            self.patternInput.show()
        else:
            self.patternLabel.hide()
            self.patternInput.hide()

def main():
    app = QApplication(sys.argv)
    gui = PasswordGeneratorGUI()
    gui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
