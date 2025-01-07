import argparse
import json
import logging
import re
from colorama import Fore, Back, Style
from generator import DictionaryGenerator
from typing import Dict, List

def display_banner():
    banner = f"""
{Fore.GREEN}

██╗   ██╗███████╗██╗  ████████╗██╗  ██╗██████╗  ██████╗ ███╗   ██╗██╗   ██╗██╗  ██╗
██║   ██║╚════██║██║  ╚══██╔══╝██║  ██║██╔══██╗██╔═══██╗████╗  ██║╚██╗ ██╔╝╚██╗██╔╝
██║   ██║    ██╔╝██║     ██║   ███████║██████╔╝██║   ██║██╔██╗ ██║ ╚████╔╝  ╚███╔╝ 
╚██╗ ██╔╝   ██╔╝ ██║     ██║   ██╔══██║██╔══██╗██║   ██║██║╚██╗██║  ╚██╔╝   ██╔██╗ 
 ╚████╔╝    ██║  ███████╗██║   ██║  ██║██║  ██║╚██████╔╝██║ ╚████║   ██║   ██╔╝ ██╗
  ╚═══╝     ╚═╝  ╚══════╝╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝
                                                                                   

{Fore.RED}╔═══════════════════════════════════════════════════════════════════════╗
║  {Fore.GREEN}V7lthronyx DICTIONARY v1.5 Beta - Advanced Password Generation Tool{Fore.RED}    ║
║  {Style.DIM}Developed by V7lthronyx Team | For Security Research Only{Style.RESET_ALL}{Fore.RED}           ║
╚═══════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    print(banner)

def detect_data_type(value: str) -> str:
    import re
    
    if re.match(r'^\d{2,4}[-/\.]\d{1,2}[-/\.]\d{1,2}$', value):
        return 'birthdate'
    
    if re.match(r'^\+?[\d\s-]{10,}$', value):
        return 'phone'
    
    if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
        return 'email'
    
    if re.match(r'^@[\w\._]+$', value):
        return 'username'
    
    if re.match(r'^[A-Za-z\s-]+$', value):
        if len(value.split()) > 1:
            return 'full_name'
        return 'name'
    
    return 'other'

def process_user_input(input_data: str) -> Dict[str, List[str]]:
    try:
        if input_data.startswith('{'):
            return json.loads(input_data)
        
        items = [item.strip() for item in re.split(r'[,\n]', input_data) if item.strip()]
        
        categorized_data = {}
        for item in items:
            data_type = detect_data_type(item)
            if data_type not in categorized_data:
                categorized_data[data_type] = []
            categorized_data[data_type].append(item)
        
        return categorized_data
    except Exception as e:
        logging.error(f"Error processing input: {e}")
        return {}

def main():
    display_banner()

    parser = argparse.ArgumentParser(description="""
This tool generates a personalized password list by combining:
1. User-provided data (name, birthdate, etc.).
2. Common password datasets.
3. Advanced patterns and optional machine learning for password prediction.

Example Usage:
---------------
python main.py --datasets dataset1.txt dataset2.txt --user-data '{"name":["John","Johnny"],"birthdate":["1990"],"phone":["1234567890"],"favorite":["Football"]}' --output generated_passwords.txt --compress --use-ml
    """, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("--datasets", nargs='+', help="Paths to base dataset files.")
    parser.add_argument("--output", default="generated_passwords.txt", help="Output file for generated passwords.")
    parser.add_argument("--max", type=int, default=100000, help="Maximum number of generated passwords.")
    parser.add_argument("--user-data", type=str, default='',
                       help='Comma-separated or newline-separated list of personal information. Types will be detected automatically.')
    parser.add_argument("--compress", action="store_true", help="Compress the output file using gzip.")
    parser.add_argument("--estimate-size", action="store_true", help="Estimate the size of the generated password list without creating it.")
    parser.add_argument("--verbose", action="store_true", help="Increase logging level to DEBUG.")
    parser.add_argument("--use-ml", action="store_true", help="Use machine learning for password generation.")
    parser.add_argument("--sync", action="store_true", help="Sync the datasets before generating passwords.")
    parser.add_argument("--gui", action="store_true", help="Launch the graphical user interface.")
    parser.add_argument("--min-length", type=int, default=6, help="Minimum length for generated passwords.")
    parser.add_argument("--model-path", type=str, default="password_model.keras", help="Path to the Keras model file.")

    args = parser.parse_args()

    if args.gui:
        from gui import main as gui_main
        gui_main()
        return

    if args.verbose:
        logging.basicConfig(
            filename='v7lthronyx_DICTIONARY.log',
            filemode='a',
            format='%(asctime)s - %(levelname)s - %(message)s',
            level=logging.DEBUG
        )
        logging.debug("Verbose mode enabled.")
    else:
        logging.basicConfig(
            filename='v7lthronyx_DICTIONARY.log',
            filemode='a',
            format='%(asctime)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )

    if not args.datasets:
        logging.info("No datasets provided. Using default random data.")

    if args.sync:
        logging.info("Syncing datasets...")
        logging.info("Datasets synced successfully.")

    logging.info("Initializing the password generator...")
    try:
        generator = DictionaryGenerator(base_datasets=args.datasets, model_path=args.model_path)
    except Exception as e:
        logging.error(f"Failed to initialize the generator: {e}")
        exit(1)

    if args.use_ml:
        try:
            generator.load_or_train_model()
        except Exception as e:
            logging.error(f"Failed to load or train the model: {e}")
            exit(1)
    else:
        logging.info("ML usage not requested. Proceeding without ML.")

    user_data = process_user_input(args.user_data)
    logging.info(f"Detected data categories: {list(user_data.keys())}")

    if args.estimate_size:
        try:
            size = generator.estimate_size(user_data=user_data, max_combinations=args.max)
            print(f"{Fore.GREEN}[INFO]{Style.RESET_ALL} Estimated size of the generated password list: {size}")
            logging.info(f"Estimated size of the generated password list: {size}")
        except Exception as e:
            logging.error(f"Failed to estimate the size of the password list: {e}")
        exit(0)

    logging.info("Generating password list...")
    try:
        password_list = generator.generate_personalized_list(
            user_data=user_data,
            max_combinations=args.max,
            use_ml=args.use_ml,
            min_length=args.min_length
        )
    except Exception as e:
        logging.error(f"Failed to generate password list: {e}")
        exit(1)

    try:
        generator.save_to_file(password_list, args.output, compress=args.compress)
        print(f"{Fore.GREEN}[INFO]{Style.RESET_ALL} Password list saved to {args.output}")
        logging.info(f"Password list saved to {args.output}")
    except Exception as e:
        logging.error(f"Failed to save the password list: {e}")

if __name__ == "__main__":
    main()
