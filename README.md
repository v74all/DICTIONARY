# V7lthronyx DICTIONARY v1.5 Beta - Advanced Password Generation Tool

## Overview

V7lthronyx DICTIONARY is an advanced password generation tool designed for security research purposes. It combines user-provided data, common password datasets, and advanced patterns, with optional machine learning capabilities to generate strong and personalized password lists.

دیکشنری V7lthronyx یک ابزار پیشرفته برای تولید رمز عبور است که برای اهداف تحقیقاتی امنیتی طراحی شده است. این ابزار با ترکیب داده‌های ارائه شده توسط کاربر، مجموعه‌های رمز عبور رایج و الگوهای پیشرفته، با قابلیت‌های اختیاری یادگیری ماشین، لیست‌های رمز عبور قوی و شخصی‌سازی شده تولید می‌کند.

## Features

- **User Data Integration**: Generate passwords based on personal information like names, birthdates, etc.
- **Dataset Utilization**: Use common password datasets to enhance password generation.
- **Advanced Patterns**: Apply complex patterns and transformations to create strong passwords.
- **Machine Learning**: Optionally use AI to predict and generate password patterns.
- **Output Compression**: Save results in a compressed format.
- **Size Estimation**: Preview the expected size of the generated password list.

- **یکپارچه‌سازی داده‌های کاربر**: تولید رمز عبور بر اساس اطلاعات شخصی مانند نام‌ها، تاریخ تولد و غیره.
- **استفاده از مجموعه داده‌ها**: استفاده از مجموعه‌های رمز عبور رایج برای بهبود تولید رمز عبور.
- **الگوهای پیشرفته**: اعمال الگوها و تغییرات پیچیده برای ایجاد رمزهای عبور قوی.
- **یادگیری ماشین**: استفاده اختیاری از هوش مصنوعی برای پیش‌بینی و تولید الگوهای رمز عبور.
- **بررسی نفوذ**: تأیید رمزهای عبور تولید شده در برابر رمزهای عبور نفوذ شده شناخته شده.
- **فشرده‌سازی خروجی**: ذخیره نتایج در قالب فشرده.
- **برآورد اندازه**: پیش‌نمایش اندازه مورد انتظار لیست رمز عبور تولید شده.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/v7lthronyx_DICTIONARY.git
    cd v7lthronyx_DICTIONARY
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

1. **کلون کردن مخزن**:
    ```bash
    git clone https://github.com/v74all/DICTIONARY.git
    cd v7lthronyx_DICTIONARY
    ```

2. **نصب وابستگی‌ها**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Command Line Interface (CLI)

Run the tool using the command line interface:

```bash
python main.py --datasets dataset1.txt dataset2.txt --user-data '{"name":["John","Johnny"],"birthdate":["1990"],"phone":["1234567890"],"favorite":["Football"]}' --output generated_passwords.txt --compress --use-ml
```

### رابط خط فرمان (CLI)

اجرای ابزار با استفاده از رابط خط فرمان:

```bash
python main.py --datasets dataset1.txt dataset2.txt --user-data '{"name":["John","Johnny"],"birthdate":["1990"],"phone":["1234567890"],"favorite":["Football"]}' --output generated_passwords.txt --compress --use-ml
```

#### CLI Options

- `--datasets`: Paths to base dataset files.
- `--output`: Output file for generated passwords.
- `--max`: Maximum number of generated passwords.
- `--user-data`: Comma-separated or newline-separated list of personal information.
- `--compress`: Compress the output file using gzip.
- `--estimate-size`: Estimate the size of the generated password list without creating it.
- `--verbose`: Increase logging level to DEBUG.
- `--use-ml`: Use machine learning for password generation.
- `--sync`: Sync the datasets before generating passwords.
- `--gui`: Launch the graphical user interface.
- `--min-length`: Minimum length for generated passwords.
- `--model-path`: Path to the Keras model file.

#### گزینه‌های CLI

- `--datasets`: مسیرهای فایل‌های مجموعه داده پایه.
- `--output`: فایل خروجی برای رمزهای عبور تولید شده.
- `--max`: حداکثر تعداد رمزهای عبور تولید شده.
- `--user-data`: لیست اطلاعات شخصی جدا شده با کاما یا خط جدید.
- `--compress`: فشرده‌سازی فایل خروجی با استفاده از gzip.
- `--estimate-size`: برآورد اندازه لیست رمز عبور تولید شده بدون ایجاد آن.
- `--verbose`: افزایش سطح لاگینگ به DEBUG.
- `--use-ml`: استفاده از یادگیری ماشین برای تولید رمز عبور.
- `--sync`: همگام‌سازی مجموعه داده‌ها قبل از تولید رمز عبور.
- `--gui`: راه‌اندازی رابط کاربری گرافیکی.
- `--min-length`: حداقل طول برای رمزهای عبور تولید شده.
- `--model-path`: مسیر فایل مدل Keras.

### Graphical User Interface (GUI)

Launch the GUI for a more interactive experience:

```bash
python main.py --gui
```

### رابط کاربری گرافیکی (GUI)

راه‌اندازی GUI برای تجربه‌ای تعاملی‌تر:

```bash
python main.py --gui
```

#### GUI Features

- **Language Switch**: Toggle between English and Persian.
- **User Data Input**: Enter personal information manually or load from a file.
- **Dataset Selection**: Browse and select dataset files.
- **Advanced Options**: Enable machine learning, breach check, output compression, and size estimation.
- **Combination Methods**: Choose from various password combination methods or define a custom pattern.
- **Generate Passwords**: Generate and view the password list directly in the GUI.

#### ویژگی‌های GUI

- **تغییر زبان**: تغییر بین انگلیسی و فارسی.
- **ورود داده‌های کاربر**: وارد کردن اطلاعات شخصی به صورت دستی یا بارگذاری از یک فایل.
- **انتخاب مجموعه داده‌ها**: مرور و انتخاب فایل‌های مجموعه داده.
- **گزینه‌های پیشرفته**: فعال کردن یادگیری ماشین، بررسی نفوذ، فشرده‌سازی خروجی و برآورد اندازه.
- **روش‌های ترکیب**: انتخاب از میان روش‌های مختلف ترکیب رمز عبور یا تعریف یک الگوی سفارشی.
- **تولید رمزهای عبور**: تولید و مشاهده لیست رمز عبور به طور مستقیم در GUI.

## Help

For detailed instructions on how to use the password generator, refer to the help section within the GUI or use the `--help` option in the CLI.

## راهنما

برای دستورالعمل‌های دقیق در مورد نحوه استفاده از تولید کننده رمز عبور، به بخش راهنما در GUI مراجعه کنید یا از گزینه `--help` در CLI استفاده کنید.

## Example Usage

### CLI Example

```bash
python main.py --datasets common_passwords.txt --user-data 'name:John, birthdate:1990-05-15, phone:1234567890' --output passwords.txt --max 50000 --use-ml
```

### مثال CLI

```bash
python main.py --datasets common_passwords.txt --user-data 'name:John, birthdate:1990-05-15, phone:1234567890' --output passwords.txt --max 50000 --use-ml
```

### GUI Example

1. Launch the GUI:
    ```bash
    python main.py --gui
    ```

2. Enter user data, select datasets, and configure options.
3. Click "Generate Passwords" to create and view the password list.

### مثال GUI

1. راه‌اندازی GUI:
    ```bash
    python main.py --gui
    ```

2. وارد کردن داده‌های کاربر، انتخاب مجموعه داده‌ها و پیکربندی گزینه‌ها.
3. کلیک بر روی "Generate Passwords" برای ایجاد و مشاهده لیست رمز عبور.

## Logging

Logs are saved to `v7lthronyx_DICTIONARY.log` in the current directory. Use the `--verbose` option to enable detailed logging.

## لاگینگ

لاگ‌ها در `v7lthronyx_DICTIONARY.log` در دایرکتوری فعلی ذخیره می‌شوند. از گزینه `--verbose` برای فعال کردن لاگینگ دقیق استفاده کنید.

## License

This tool is for security research purposes only. Use responsibly and ethically.

## مجوز

این ابزار فقط برای اهداف تحقیقاتی امنیتی است. به صورت مسئولانه و اخلاقی استفاده کنید.
