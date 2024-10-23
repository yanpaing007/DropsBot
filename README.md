[![Static Badge](https://img.shields.io/badge/Telegram-Bot%20Link-Link?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/Tomarket_ai_bot/app?startapp=0001b3Lf)
## Note ##
**This bot source code is from gravelfire repository which I can no longer find,and I added some feature and fixed some bugs,the source code credit goes to @GravelFire**
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
|                           Auto farming                              |     ✅     |
|                    Automatic quest completion                       |     ✅     |
|                      Auto Daily Reward                              |     ✅     |
|                       Auto Claim Stars                              |     ✅     |
|                       Auto Claim Combo                              |     ✅     |
|                       Auto Rank Upgrade                             |     ✅     |
|                        Auto Play Raffle                             |     ✅     |
|                       Auto Add 🍅 to name                           |     ✅     |
|                        Auto Claim Stash                             |     ✅     |
|                  Auto add wallet address                            |     ✅     |


## [Settings](https://github.com/yanpaing007/Tomarket/blob/main/.env-example/)
|        Settings         |                                      Description                                       |
|:-----------------------:|:--------------------------------------------------------------------------------------:|
|  **API_ID**             |        Your Telegram API ID (integer)                                                  |
|  **API_HASH**           |        Your Telegram API Hash (string)                                                 |
|  **REF_ID**             |        Your referral id after startapp=                             |
| **POINTS_COUNT**        | Number of points per game (e.g., [450, 600]) |
|  **FAKE_USERAGENT**     |        Use a fake user agent for sessions (True / False)                               |
|  **AUTO_PLAY_GAME**     |        Automatically play games (True / False)                                         |
|  **AUTO_TASK**          |        Automatically complete tasks (True / False)                                     |
|  **AUTO_DAILY_REWARD**  |        Automatically claim daily rewards (True / False)                                |
|  **AUTO_CLAIM_STARS**  |        Automatically claim star rewards (True / False)                                 |
|  **AUTO_CLAIM_COMBO**   |        Automatically claim combo rewards (True / False)                                |
|    **AUTO_RANK_UPGRADE**    |                  Automatically upgrade rank (True / False)                   |
| **USE_RANDOM_DELAY_IN_RUN** | Whether to use random delay at startup (True / False)                              |
| **RANDOM_DELAY_IN_RUN** |        Random delay at startup (e.g. [0, 15])                                          |
| **Auto_play_raffle** |        Automatically play raffle(True/False)                                          |
| **AUTO_ADD_WALLET** |        Automatically add wallet(True/False)                                          |
| **USE_PROXY_FROM_FILE** |        Whether to use a proxy from the `bot/config/proxies.txt` file (True / False)    |

## Quick Start 📚

To fast install libraries and run bot - open run.bat on Windows or run.sh on Linux

## Prerequisites
Before you begin, make sure you have the following installed:
- [Python](https://www.python.org/downloads/) **version 3.10**

## Obtaining API Keys
1. Go to my.telegram.org and log in using your phone number.
2. Select "API development tools" and fill out the form to register a new application.
3. Record the API_ID and API_HASH provided after registering your application in the .env file.

## Wallet.json example to add adress to tomarket
- I suggest,manually adding the wallet if possible
```
{
    "session1_name"{
        "address":"your_bidget_ton_address1"
    },
    "session2_name"{
        "address":"your_bidget_ton_address2"
    },
    "session3_name"{
        "address":"your_bidget_ton_address3"
    },
}
```

## Installation
You can download the [**repository**](https://github.com/yanpaing007/Tomarket) by cloning it to your system and installing the necessary dependencies:
```shell
git clone https://github.com/yanpaing007/Tomarket.git
cd Tomarket
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
~/Tomarket >>> python3 main.py --action (1/2)
# Or
~/Tomarket >>> python3 main.py -a (1/2)

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
~/Tomarket >>> python main.py --action (1/2)
# Or
~/Tomarket >>> python main.py -a (1/2)

# 1 - Run clicker
# 2 - Creates a session
```
