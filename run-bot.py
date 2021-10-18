#!/usr/bin/env python3
# run a trading bot

import time
from dotenv import load_dotenv
import os
from typing import Dict
from trader.strategy.ema_cross import EMACross
from pyjuque.Bot import defineBot
import sys
from pathlib import Path

sys.path.append(Path(__file__).parent)


# trade for reals?
SIMULATION = False
# how much to give the bot to play with
# (in quote price, a.k.a. dollars)
STARTING_BALANCE = 1000

load_dotenv()

api_key = os.environ["EXCHG_API_KEY"]
secret = os.environ["EXCHG_SECRET"]
subaccount = os.environ["EXCHG_SUBACCOUNT"]
exchange_config = {
    "name": "ftx",  # change me to your exchange
    "params": {"api_key": api_key, "secret": secret},
}
if subaccount:
    exchange_config["params"]["headers"] = {"FTX-SUBACCOUNT": subaccount}

db_url = os.environ.get("DATABASE_URL", "sqlite:///trader.db")


def gen_config(
    StratClass,
    params: Dict[str, float],
    signal_distance: float = 0.3,
    take_profit: float = 4,
    stop_loss_value: float = 6,
    initial_entry_allocation: float = 33,
) -> dict:
    return {
        "name": "eth_ema_cross_optimized_v1",
        "db_url": db_url,
        "test_run": SIMULATION,
        "exchange": exchange_config,
        "symbols": [
            "ETH-PERP",
        ],
        "sleep": 60,
        "starting_balance": STARTING_BALANCE,
        "strategy": {"class": StratClass, "params": params},
        "timeframe": "1m",
        "entry_settings": {
            "initial_entry_allocation": initial_entry_allocation,
            "signal_distance": signal_distance,  # pct under buy signal to place order
            "leverage": 1,
        },
        "exit_settings": {
            "take_profit": take_profit,
            "stop_loss_value": stop_loss_value,
            "exit_on_signal": True,
            "sell_on_end": True,
        },
    }


def params_to_bot_config(p):
    # strat params
    fast_ma_len = p.pop("fast_ma_len")
    slow_ma_len = p.pop("slow_ma_len")
    bot_config = gen_config(
        StratClass=EMACross,
        params=dict(fast_ma_len=fast_ma_len, slow_ma_len=slow_ma_len),
        **p
    )
    return bot_config


config = params_to_bot_config(
    # profit: 0.00986
    {
        "fast_ma_len": 7.723984110583816,
        "signal_distance": 0.09673297413983993,
        "slow_ma_len": 6.514447627441819,
        "stop_loss_value": 13.115218651491784,
        "take_profit": 3.837416072341963,
    }
)
bot_controller = defineBot(config)
exchange = bot_controller.exchange


def run_bot():
    while True:
        bot_controller.executeBot()
        bot_controller.status_printer.start()
        left_to_sleep = config["sleep"]
        while left_to_sleep > 0:
            if bot_controller.status_printer != None:
                open_orders = bot_controller.bot_model.getOpenOrders(
                    bot_controller.session
                )
                bot_controller.status_printer.text = (
                    "Open Orders: {}   |   Checking signals in {}".format(
                        len(open_orders), left_to_sleep
                    )
                )
            time.sleep(1)
            left_to_sleep -= 1


if __name__ == "__main__":
    # print(exchange.has["fetchOHLCV"])
    # print(exchange["timeframes"])
    run_bot()
