import pandas as pd
import numpy as np

stock_list = pd.read_csv('../input/stock_list.csv')

returns = pd.DataFrame()
last_price = np.zeros((len(stock_list)))

cleancomma = lambda items: float(str(items).replace(',', ''))
to_float = lambda items: float(items)

for i in range(len(stock_list)):
    stock_name = stock_list.stock_name[i]
    print(stock_name)
    path = '../input/'+stock_name+'.csv'
    stock = pd.read_csv(path)
    stock['f_adj_price'] = stock['Adj Close'].map(cleancomma).map(to_float)
    returns[stock_name] = (stock['f_adj_price']/stock['f_adj_price'].shift(12))-1
    last_price[i] = stock['f_adj_price'].iloc[-1]

cov_mat = returns.dropna().cov()

num_port = 30000
rf = 0.04
all_wts = np.zeros((num_port, len(returns.columns)))
port_returns = np.zeros((num_port))
port_risk = np.ones((num_port))
sharpe_ratio = np.zeros((num_port))

# SIMULATE x PORTFOLIOS

np.random.seed(42)

for i in range(num_port):

    # Portfolio weights
    wts = np.random.uniform(size=len(returns.columns))
    wts = wts / np.sum(wts)
    all_wts[i, :] = wts

    # Portfolio Return
    port_ret = np.sum(returns.mean() * wts)
    port_returns[i] = port_ret

    # Portfolio Risk
    port_sd = np.sqrt(np.dot(wts.T, np.dot(cov_mat, wts)))
    port_risk[i] = port_sd

    # Portfolio Sharpe Ratio, assuming 0% Risk Free Rate
    sr = (port_ret - rf) / port_sd
    sharpe_ratio[i] = sr

    # Save portfolios of interest (min var, max return and max SR)
    if sr >= max(sharpe_ratio[0:-1]):
        max_sr_ret = port_ret
        max_sr_risk = port_sd
        max_sr_w = wts
        max_sr = sr

    if port_ret >= max(port_returns[0:-1]):
        max_ret_ret = port_ret
        max_ret_risk = port_sd
        max_ret_w = wts

    if port_sd <= min(port_risk[0:-1]):
        min_var_ret = port_ret
        min_var_risk = port_sd
        min_var_w = wts
