# Mischa's Crypto Trader
Automating crypto trading with python.

## What is this?
A jupyter notebook to demonstrate automating crypto trading. Includes defining a strategy with automated parameter tuning and backtesting.

## How does it work?
Allows you to [pick a strategy](https://github.com/twopirllc/pandas-ta/blob/main/examples/PandasTA_Strategy_Examples.ipynb) and optimize the parameters to the trading bot and strategy automatically. Different parameters are tried and net profit calculated during backtesting.

* Uses [pyjuque](https://github.com/tudorelu/pyjuque) to perform backtesting and trading and bot framework.
* Technical analysis performed by [ta-lib](https://www.ta-lib.org/) and [pandas-ta](https://github.com/twopirllc/pandas-ta/) - generate buy and sell signals from time series exchange data.
* Crypto exchange abstraction provided by [CCXT](https://ccxt.readthedocs.io/en/latest/) - connects to any crypto exchange.
* Parameter tuning with [hyperopt](https://github.com/hyperopt/hyperopt/) - Minimizes objective function in trading bot and strategy parameter space.

## How do I run it?
Load up [the notebook](Yahoozee.ipynb) in [JupyterLab](https://jupyterlab.readthedocs.io/en/stable/).

## Screenshots
![backtesting](backtest.png)

