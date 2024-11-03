import os
import glob
import asyncio
import argparse
from itertools import cycle
import sys

from pyrogram import Client
from better_proxy import Proxy

from bot.config import settings
from bot.utils import logger
from bot.core.tapper import run_tapper
from bot.core.registrator import register_sessions
from bot.utils.api_check import check_base_url, get_local_version_info, get_version_info


start_text = """
Select an action:

    1. Run clicker
    2. Create session
"""

global tg_clients

def get_session_names() -> list[str]:
    session_names = glob.glob("sessions/*.session")
    session_names = [
        os.path.splitext(os.path.basename(file))[0] for file in session_names
    ]

    return session_names


def get_proxies() -> list[Proxy]:
    if settings.USE_PROXY_FROM_FILE:
        try:
            with open(file="bot/config/proxies.txt", encoding="utf-8-sig") as file:
                proxies = [Proxy.from_str(proxy=row.strip()).as_url for row in file]
        except FileNotFoundError:
            logger.error("Proxies file not found.")
            proxies = []
        except Exception as e:
            logger.error(f"Error reading proxies file: {e}")
            proxies = []
    else:
        proxies = []
        logger.info("USE_PROXY_FROM_FILE is set to False. No proxies loaded.")

    return proxies


async def get_tg_clients() -> list[Client]:
    global tg_clients

    session_names = get_session_names()

    if not session_names:
        raise FileNotFoundError("Not found session files")

    if not settings.API_ID or not settings.API_HASH:
        raise ValueError("API_ID and API_HASH not found in the .env file.")

    tg_clients = [
        Client(
            name=session_name,
            api_id=settings.API_ID,
            api_hash=settings.API_HASH,
            workdir="sessions/",
            plugins=dict(root="bot/plugins"),
        )
        for session_name in session_names
    ]

    return tg_clients


async def process() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--action", type=int, help="Action to perform")

    if check_base_url() is False:
        sys.exit(
            "Detected api change! Stopped the bot for safety.Please raise an issue on the GitHub repository.")
    else:
        logger.info("<green>No change in API!</green>")
    github_version,message = get_version_info()
    local_version = get_local_version_info()
        
    if github_version is not None and local_version is not None and message is not None:
        if github_version == local_version:
            logger.info(f"<cyan>Bot is up to date! v{local_version}</cyan>")
        else:
            logger.info(f"<cyan>Bot is out of date, update the bot with command 'git pull', </cyan><light-red>v{local_version}</light-red> <cyan>> </cyan><light-red>v{github_version}</light-red>")
        logger.info(f"<cyan>Developer message: {message}</cyan>")

    logger.info(f"Detected {len(get_session_names())} sessions | {len(get_proxies())} proxies")

    action = parser.parse_args().action

    if not action:
        print(start_text)

        while True:
            action = input("> ")

            if not action.isdigit():
                logger.warning("Action must be number")
            elif action not in ["1", "2"]:
                logger.warning("Action must be 1 or 2")
            else:
                action = int(action)
                break

    if action == 2:
        await register_sessions()
    elif action == 1:
        tg_clients = await get_tg_clients()

        await run_tasks(tg_clients=tg_clients)


async def run_tasks(tg_clients: list[Client]):
    proxies = get_proxies()
    proxies_cycle = cycle(proxies) if proxies else None
    tasks = [
        asyncio.create_task(
            run_tapper(
                tg_client=tg_client,
                proxy=next(proxies_cycle) if proxies_cycle else None,
            )
        )
        for tg_client in tg_clients
    ]

    await asyncio.gather(*tasks)
