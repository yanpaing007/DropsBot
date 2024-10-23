import asyncio
from datetime import datetime
import json
import os,sys
from random import randint, choices, random
from time import time
from urllib.parse import unquote, quote

import aiohttp
from aiohttp_proxy import ProxyConnector
from better_proxy import Proxy
from pyrogram import Client
from pyrogram.errors import Unauthorized, UserDeactivated, AuthKeyUnregistered, FloodWait
from pyrogram.raw.functions.messages import RequestAppWebView
from pyrogram.raw.types import InputBotAppShortName

from typing import Callable
import functools
from bot.config import settings
from bot.exceptions import InvalidSession
from bot.utils import logger
from .agents import generate_random_user_agent
from .headers import headers

def error_handler(func: Callable):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            await asyncio.sleep(1)
    return wrapper


class Tapper:
    def __init__(self, tg_client: Client, proxy: str | None):
        self.session_name = tg_client.name
        self.tg_client = tg_client
        self.proxy = proxy

    async def get_tg_web_data(self) -> str:
        
        if self.proxy:
            proxy = Proxy.from_str(self.proxy)
            proxy_dict = dict(
                scheme=proxy.protocol,
                hostname=proxy.host,
                port=proxy.port,
                username=proxy.login,
                password=proxy.password
            )
        else:
            proxy_dict = None

        self.tg_client.proxy = proxy_dict

        try:
            if not self.tg_client.is_connected:
                try:
                    await self.tg_client.connect()

                except (Unauthorized, UserDeactivated, AuthKeyUnregistered):
                    raise InvalidSession(self.session_name)
            
            while True:
                try:
                    peer = await self.tg_client.resolve_peer('fomo')
                    break
                except FloodWait as fl:
                    fls = fl.value

                    logger.warning(f"{self.session_name} | FloodWait {fl}")
                    logger.info(f"{self.session_name} | Sleep {fls}s")
                    await asyncio.sleep(fls + 10)
            
            ref_id = choices([settings.REF_ID, "V101C"], weights=[60, 40], k=1)[0]
            web_view = await self.tg_client.invoke(RequestAppWebView(
                peer=peer,
                app=InputBotAppShortName(bot_id=peer, short_name="app"),
                platform='android',
                write_allowed=True,
                start_param=ref_id
            ))
            
            auth_url = web_view.url
            tg_web_data = unquote(string=auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0])
           
            if self.tg_client.is_connected:
                await self.tg_client.disconnect()

            return ref_id, tg_web_data

        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error: {error}")
            await asyncio.sleep(delay=3)
            return None, None

    @error_handler
    async def make_request(self, http_client, method, endpoint=None, url=None, **kwargs):
        full_url = url or f"https://api.miniapp.dropstab.com/api{endpoint or ''}"
        response = await http_client.request(method, full_url, **kwargs)
        return await response.json()
        
    @error_handler
    async def login(self, http_client, tg_web_data: str):
        response = await self.make_request(http_client, "POST", "/auth/login", json={"webAppData": tg_web_data})
        return response

    @error_handler
    async def check_proxy(self, http_client: aiohttp.ClientSession) -> None:
        response = await self.make_request(http_client, 'GET', url='https://httpbin.org/ip', timeout=aiohttp.ClientTimeout(5))
        ip = response.get('origin')
        logger.info(f"{self.session_name} | Proxy IP: {ip}")

    @error_handler
    async def daily_bonus(self, http_client):
        return await self.make_request(http_client, "POST", "/bonus/dailyBonus")

    @error_handler
    async def welcome_bonus(self, http_client):
        return await self.make_request(http_client, "POST", "/bonus/welcomeBonus")

    @error_handler
    async def get_task(self, http_client):
        return await self.make_request(http_client, "GET", "/quest")

    @error_handler
    async def verify_task(self, http_client,task_id:int):
        return await self.make_request(http_client, "PUT", f"/quest/{task_id}/verify")

    @error_handler
    async def claim_task(self, http_client,task_id:int):
        return await self.make_request(http_client, "PUT", f"/quest/{task_id}/claim")

    @error_handler
    async def claim_referral_reward(self, http_client):
        return await self.make_request(http_client, "POST", "refLink/claim")


    @error_handler
    async def check_ref_status(self, http_client):
        return await self.make_request(http_client, "GET", "/refLink")
    
    @error_handler
    async def apply_ref(self,http_client,ref_id:str):
        return await self.make_request(http_client, "PUT", "/user/applyRefLink",json={"code":ref_id})
    
    @error_handler
    async def get_order(self,http_client):
        return await self.make_request(http_client, "GET", "/order")
    
    @error_handler
    async def claim_order(self,http_client,order_id:int):
        return await self.make_request(http_client, "PUT", f"/order/{order_id}/claim")
    
    @error_handler
    async def choose_coin(self,http_client):
        crypto_data=await self.make_request(http_client, "GET", f"/order/coins")
        if not crypto_data:
            return None
        best_coin = None
        best_change = float('-inf')
        
        for coin in crypto_data:
            change24h = coin.get('change24h', float('-inf'))
            if change24h > best_change:
                best_change = change24h
                best_coin = coin
        return best_coin 
    
    @error_handler
    async def get_coin_detail(self,http_client,coin_id:int):
        return await self.make_request(http_client, "GET", f"/order/coinStats/{coin_id}")
    
    @error_handler
    async def create_order(self,http_client,coin_id:int,period_id:int,decide:bool):
        return await self.make_request(http_client, "POST", f"/order",json={"coinId":coin_id,"short":decide,"periodId":period_id})
    
    @error_handler
    async def mark_fail_order(self,http_client,order_id:int):
        return await self.make_request(http_client, "PUT", f"/order/{order_id}/markUserChecked")
    
    @error_handler
    async def process_orders(self, http_client):
        get_order = await self.get_order(http_client=http_client)
        if not get_order:
            logger.error(f"{self.session_name} | <red>Failed to get order!</red>")
            return

        balance = get_order.get('totalScore', 0)
        result = get_order.get('results', {})

        if not result:
            logger.error(f"{self.session_name} | <red>No results available!</red>")
            return

        orders = result.get('orders', 0)
        win = result.get('wins', 0)
        lose = result.get('loses', 0)
        win_rate = result.get('winRate', 0)
        logger.info(f"{self.session_name} | Balance - [<yellow>{balance}</yellow>] DPS | Orders - [<yellow>{orders}</yellow>] | Wins - [<yellow>{win}</yellow>] | Loses - [<yellow>{lose}</yellow>] | Win Rate - [<yellow>{win_rate} %</yellow>]")
        periods = get_order.get('periods', [])

        for item in periods:
            
            order = item.get('order', None)
            period = item.get('period', None)

            if period:
                period_id = period.get('id', None)
                threshold = period.get('unlockThreshold', 0)

                if order is None:
                    if balance > threshold:
                        logger.info(f"{self.session_name} | Starting a new order in <yellow>slot:{period_id}</yellow>.")
                        await self.start_new_order(http_client, period_id)
                    else:
                        logger.info(f"{self.session_name} | <yellow>Slot:{period_id}</yellow> is below balance threshold, skipping.")
                    continue

                order_id = order.get('id', None)
                bet = "Long" if not order.get('short', None) else "Short"
                reward = int(order.get('reward', 0))
                result = "Won" if order.get('result', None) else "Lose"
                status = order.get('status', None)
                finish_at = order.get('secondsToFinish', None)

                if status == 'CLAIM_AVAILABLE' and finish_at == 0:
                    claim_order = await self.claim_order(http_client, order_id)
                    if claim_order:
                        logger.info(f"{self.session_name} | Your <yellow>{bet}</yellow> order in <yellow>slot:{period_id}</yellow> was <yellow>{result}</yellow>, reward : <yellow>{reward}</yellow>!")
                        await self.start_new_order(http_client, period_id)
                        
                    else:
                        logger.error(f"{self.session_name} | <red>Failed to claim order!</red>")
                elif status == 'PENDING':
                    logger.info(f"{self.session_name} | Your <yellow>{bet}</yellow> order in <yellow>slot:{period_id}</yellow> is still pending! Will finish in <yellow>{finish_at}</yellow> minutes.")
                    
                elif status == 'NOT_WIN' and finish_at == 0:
                    check_fail_order = await self.mark_fail_order(http_client, order_id)
                    if check_fail_order and check_fail_order.get('status') == 'OK':
                        logger.info(f"{self.session_name} | <yellow>{bet}</yellow> order in <yellow>slot:{period_id}</yellow> was <yellow>{result}</yellow>, reward : <yellow> 0 :(</yellow>!")
                    
                    
    @error_handler
    async def start_new_order(self, http_client, period_id):
        logger.info(f"{self.session_name} | Waiting 10 seconds before placing order!")
        await asyncio.sleep(10)
        logger.info(f"{self.session_name} | Choosing best coin to place order...")
        choose_coin = await self.choose_coin(http_client)
        if not choose_coin:
            logger.error(f"{self.session_name} | <red>Failed to choose best coin!</red>")
            return

        logger.info(f"{self.session_name} | Selected <yellow>{choose_coin.get('name')}</yellow> coin to place order!")
        coin_id = choose_coin.get('id')

        coin_detail = await self.get_coin_detail(http_client, coin_id)
        if not coin_detail:
            logger.error(f"{self.session_name} | <red>Failed to get coin detail!</red>")
            return

        total_player = coin_detail.get('total', 0)
        long = coin_detail.get('long', 0)
        short = coin_detail.get('short', 0)
        name = coin_detail.get('coin').get('name', 'Unknown')
        decide = short > long
        long_or_short = "Long" if not decide else "Short"

        logger.info(f"{self.session_name} | Total Players : <yellow>{total_player}</yellow> | Long : <yellow>{long}</yellow> | Short : <yellow>{short}</yellow>")
        logger.info(f"{self.session_name} | Placing {long_or_short} order for <yellow>{name}</yellow>!")

        place_order = await self.create_order(http_client, coin_id, period_id, decide)
        if place_order:
            logger.info(f"{self.session_name} | Successfully placed <yellow>{long_or_short}</yellow> order on <yellow>{name}</yellow>!")
        else:
            logger.error(f"{self.session_name} | <red>Failed to place order!</red>")
        
        

    
    
    async def run(self) -> None:        
        if settings.USE_RANDOM_DELAY_IN_RUN:
            random_delay = randint(settings.RANDOM_DELAY_IN_RUN[0], settings.RANDOM_DELAY_IN_RUN[1])
            logger.info(f"{self.tg_client.name} | Bot will start in <yellow>{random_delay}s</yellow>")
            await asyncio.sleep(delay=random_delay)
        
        proxy_conn = ProxyConnector().from_url(self.proxy) if self.proxy else None
        http_client = aiohttp.ClientSession(headers=headers, connector=proxy_conn)
        if self.proxy:
            await self.check_proxy(http_client=http_client)
        
        if settings.FAKE_USERAGENT:        
            http_client.headers['User-Agent'] = generate_random_user_agent(device_type='android', browser_type='chrome')

        token_expiration = 0
        small_sleep = randint(settings.MIN_DELAY[0], settings.MIN_DELAY[1])
        big_sleep = randint(settings.BIG_SLEEP_TIME[0], settings.BIG_SLEEP_TIME[1])
        
        while True:
            try:
                
                if http_client.closed:
                    if proxy_conn:
                        if not proxy_conn.closed:
                            proxy_conn.close()

                    proxy_conn = ProxyConnector().from_url(self.proxy) if self.proxy else None
                    http_client = aiohttp.ClientSession(headers=headers, connector=proxy_conn)
                    if settings.FAKE_USERAGENT:            
                        http_client.headers['User-Agent'] = generate_random_user_agent(device_type='android', browser_type='chrome')     
                current_time = time()
                if current_time >= token_expiration:
                    if (token_expiration != 0):
                        logger.info(f"{self.session_name} | Token expired, refreshing...")
                    ref_id, init_data = await self.get_tg_web_data()
                    login_response = await self.login(http_client=http_client, tg_web_data=init_data)
                
                    
                    if login_response and "jwt" in login_response:
                        access_token = login_response.get("jwt").get("access").get("token")
                        token_expiration = current_time + 3600
                        http_client.headers["Authorization"] = f"Bearer {access_token}"
                        if login_response.get('user').get('usedRefLinkCode') is None:
                            apply_ref=await self.apply_ref(http_client= http_client,ref_id=ref_id)
                            logger.info(f"{self.session_name} | <yellow>Referral code applied</yellow>") if apply_ref else logger.error(f"{self.session_name} | <red>Referral code not applied</red>")
                if access_token:
                    http_client.headers["Authorization"] = f"Bearer {access_token}"
                    logger.info(f"{self.session_name} | <green>Logged in</green>")
                else:
                    logger.error(f"{self.session_name} | Fail to login!")
                    continue
                        
                await asyncio.sleep(delay=small_sleep)
                
                daily_bonus = await self.daily_bonus(http_client=http_client)
                if daily_bonus.get('success'):
                    logger.info(f"{self.session_name} | <yellow>Daily bonus successfully claimed!</yellow>")
                await asyncio.sleep(delay=small_sleep)
                
                check_ref_reward = await self.check_ref_status(http_client=http_client)
                if check_ref_reward['availableToClaim'] != 0:
                    claim_ref_reward = await self.claim_ref_reward()
                    if claim_ref_reward:
                        logger.info(f"{self.session_name} | <yellow>Referral reward successfully claimed!</yellow>")
                await asyncio.sleep(delay=small_sleep)
                
                is_new_user = login_response['user']['welcomeBonusReceived']
                if not is_new_user:
                    claim_welcome_bonus = await self.welcome_bonus(http_client=http_client)
                    if claim_welcome_bonus:
                        logger.info(f"{self.session_name} | <yellow>Welcome bonus successfully claimed!</yellow>")
                await asyncio.sleep(delay=small_sleep)
                
                tasks = await self.get_task(http_client=http_client)
                for task_type in tasks:
                    if task_type['name'] == 'Refs':
                        continue

                    for task in task_type['quests']:
                        if task['name'] in ['Follow News Channel','Follow Drops Analytics Channel']:
                            continue
                        if task['claimAllowed'] == False and task['status'] == "NEW":
                            status = await self.verify_task(http_client,task_id=task['id'])
                            logger.info(f"{self.session_name} | <yellow>{task['name']}</yellow> started!")
                            logger.info(f"{self.session_name} | Sleeping for <yellow>{randint(settings.TASK_SLEEP_TIME[0], settings.TASK_SLEEP_TIME[1])}</yellow> seconds,before starting another task!")
                            await asyncio.sleep(delay=randint(settings.TASK_SLEEP_TIME[0], settings.TASK_SLEEP_TIME[1]))
                            
                        elif task['claimAllowed'] == True and task['status'] == "NEW":
                            status = await self.claim_task(http_client,task_id=task['id'])
                            if status['status'] == 'OK':
                                logger.info(f"{self.session_name} | <green>{task['name']} claimed!</green>")
                            await asyncio.sleep(delay=2)
                            
                
                await self.process_orders(http_client)

                sleep_time = big_sleep
                logger.info(f'{self.session_name} | Sleep <yellow>{round(sleep_time / 60, 2)}m.</yellow>')
                await asyncio.sleep(sleep_time)
                await http_client.close()
                if proxy_conn:
                    if not proxy_conn.closed:
                        proxy_conn.close()
            except InvalidSession as error:
                raise error

            except Exception as error:
                logger.error(f"{self.session_name} | Unknown error: {error}")
                await asyncio.sleep(delay=3)
                logger.info(f'{self.session_name} | Sleep <yellow>10m.</yellow>')
                await asyncio.sleep(600)
                


async def run_tapper(tg_client: Client, proxy: str | None):
    try:
        await Tapper(tg_client=tg_client, proxy=proxy).run()
    except InvalidSession:
        logger.error(f"{tg_client.name} | Invalid Session")