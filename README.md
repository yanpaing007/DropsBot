[![Static Badge](https://img.shields.io/badge/Telegram-Bot%20Link-Link?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/fomo/app?startapp=ref_V101C)
## [Bot Link] (https://t.me/fomo/app?startapp=ref_V101C)

## Recommendation before use

# 🔥🔥 PYTHON version must be 3.10 🔥🔥

## Features

|                               Feature                                | Supported |
|:-------------------------------------------------------------------:|:---------:|
|                           Multithreading                            |     ✅     |
|                    Proxy binding to session                         |     ✅     |
|                 Auto Referral of your accounts                      |     ✅     |
|                    Automatic task completion                        |     ✅     |
|                  Support for pyrogram .session                      |     ✅     |
|                           Auto Place Order                              |     ✅     |
|                           Auto claim ref bonus                              |     ✅     |
|                           Auto claim daily reward                              |     ✅     |



## [Settings](https://github.com/yanpaing007/DropsBot/blob/main/.env-example/)
|        Settings         |                                      Description                                       |
|:-----------------------:|:--------------------------------------------------------------------------------------:|
|  **API_ID**             |        Your Telegram API ID (integer)                                                  |
|  **API_HASH**           |        Your Telegram API Hash (string)                                                 |
|  **REF_ID**             |        Your referral id after startapp=                           |
|  **FAKE_USERAGENT**     |        Use a fake user agent for sessions (True / False, default: True)                |
| **USE_RANDOM_DELAY_IN_RUN** | Whether to use random delay at startup (True / False, default: True)               |
| **RANDOM_DELAY_IN_RUN** |        Random delay at startup (e.g. [3, 15])                                          |
| **MIN_DELAY**           |        Minimum delay between actions (e.g. [2, 5])                                     |
| **BIG_SLEEP_TIME**      |        Time to sleep after a big task (e.g. [3600, 3700])                              |
| **TASK_SLEEP_TIME**     |        Time to sleep between tasks (e.g. [40, 60])                                     |
| **AUTO_CLAIM_REFERRAL** |        Automatically claim referral rewards (True / False, default: True)              |
| **AUTO_CLAIM_DAILY_BONUS** | Automatically claim daily bonus (True / False, default: True)                       |
| **AUTO_CLAIM_REFERRAL_BONUS** | Automatically claim referral bonus (True / False, default: True)                 |
| **AUTO_CLAIM_WELCOME_BONUS** | Automatically claim welcome bonus (True / False, default: True)                   |
| **AUTO_FINISH_TASK**    |        Automatically finish tasks (True / False, default: True)                        |
| **AUTO_PLACE_ORDER**    |        Automatically place orders (True / False, default: True)                        |
| **USE_PROXY_FROM_FILE** |        Whether to use a proxy from the `bot/config/proxies.txt` file (True / False, default: False) |

## Quick Start 📚

To fast install libraries and run bot - open run.bat on Windows or run.sh on Linux

## Prerequisites
Before you begin, make sure you have the following installed:
- [Python](https://www.python.org/downloads/) **version 3.10**

## Obtaining API Keys
1. Go to my.telegram.org and log in using your phone number.
2. Select "API development tools" and fill out the form to register a new application.
3. Record the API_ID and API_HASH provided after registering your application in the .env file.


## Installation
You can download the [**repository**](https://github.com/yanpaing007/DropsBot) by cloning it to your system and installing the necessary dependencies:
```shell
git clone https://github.com/yanpaing007/DropsBot.git
cd DropsBot
```

Then you can do automatic installation by typing:

Windows:
```shell
run.bat
```

Linux:
```shell
run.sh
```

# Linux manual installation
```shell
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
cp .env-example .env
nano .env  # Here you must specify your API_ID and API_HASH, the rest is taken by default
python3 main.py
```

You can also use arguments for quick start, for example:
```shell
~/DropsBot >>> python3 main.py --action (1/2)
# Or
~/DropsBot >>> python3 main.py -a (1/2)

# 1 - Run clicker
# 2 - Creates a session
```

# Windows manual installation
```shell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env-example .env
# Here you must specify your API_ID and API_HASH, the rest is taken by default
python main.py
```

You can also use arguments for quick start, for example:
```shell
~/DropsBot >>> python main.py --action (1/2)
# Or
~/DropsBot >>> python main.py -a (1/2)

# 1 - Run clicker
# 2 - Creates a session
```
