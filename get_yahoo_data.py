#%%
import requests
import pandas as pd
import bs4 as bs
import json
import time
CHANGE_COLUMNS= ['name', 'last', 'change%']
def make_req_and_make_df_dict(url):
    """
    make requests and then pass to pandas dataframe and then convert to dictionary
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
        }
        res = requests.get(url,headers=headers).content
        df = pd.read_html(res)[0]
        df.drop(columns=['Market Time', 'Change', 'Volume', 'Open Interest','Day Chart'], axis=1, inplace=True)
        if df.shape[1] != 4:
            print(f"Data from {url} not the right shape")

        df.columns = ['name', 'description', 'last', 'change%']
        df_dict =  df.to_dict('records')
        #print(df_dict)
        return df_dict
    except:
        print(f'ran into errors in make_req for URL: {url}')
        return None
def make_req_and_make_df_dict_crypto(url):
    """
    same thing for, but for crypto
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
        }
        res = requests.get(url,headers=headers).content
        df = pd.read_html(res)[0]
        df.drop(columns=["#", "Unnamed: 1", 'Name', 'Market Cap', 'Vol (24H)', 'Total Vol', 'Chg (7D)'],axis=1, inplace=True)
        df.columns = CHANGE_COLUMNS
        df_dict =  df.to_dict('records')
        return df_dict
    except:
        print(f'ran into errors in make_req for URL: {url}')
        return None

def make_req_and_make_df_dict_bonds(url):
    """
    same thing for, but for crypto
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
        }
        res = requests.get(url,headers=headers).content
        df = pd.read_html(res)[0]
        df.drop(columns=["Unnamed: 0", 'Prev.', 'High', 'Low', 'Time','Chg.', 'Unnamed: 9'],axis=1, inplace=True)
        df.columns = CHANGE_COLUMNS
        df_dict =  df.to_dict('records')
        return df_dict
    except:
        print(f'ran into errors in make_req for URL: {url}')
        return None

def wrangle_data():
    ## regular market stuff
    URLS = [
        'https://finance.yahoo.com/commodities', #futures and commodities
        # 'https://www.investing.com/currencies/fx-futures', #currency
    ]

    ## crypto
    CRYPTO_URL ='https://www.investing.com/crypto/currencies'
    ##bonds
    RATES_BONDS_URL = 'https://www.investing.com/rates-bonds/'
    df_dict_list = []
    for url in URLS:
        try:
            df_dict = make_req_and_make_df_dict(url)
            df_dict_list.append(df_dict)
        except:
            print(f'ran into errors trying to get {url}')
            df_dict_list.append(None)
    try:
        df_dict = make_req_and_make_df_dict_crypto(CRYPTO_URL)
        df_dict_list.append(df_dict)
    except:
        print(f'ran into errors trying to get {CRYPTO_URL}')
        df_dict_list.append(None)
    try:
        df_dict = make_req_and_make_df_dict_bonds(RATES_BONDS_URL)
        df_dict_list.append(df_dict)
    except:
        print(f'ran into errors trying to get {RATES_BONDS_URL}')
        df_dict_list.append(None)
    data = {
      'ym': None,
      'es': None,
      'nq': None,
      'rty': None,
      #'dxy': None,
      'us10y': None,
      'si': None,
      'gc': None,
      #'vix': None,
      'btc': None,
      'eth': None,

    }
    for df_dicts in df_dict_list:
        if df_dicts:
            if not data['ym']:
                data['ym'] = [df_dict for df_dict in df_dicts if 'YM' in df_dict['name']][0]

            if not data['es']:
                data['es'] = [df_dict for df_dict in df_dicts if 'ES' in df_dict['name']][0]
            if not data['nq']:
                data['nq'] = [df_dict for df_dict in df_dicts if 'NQ' in df_dict['name']][0]
            if not data['rty']:
                data['rty'] = [df_dict for df_dict in df_dicts if 'RTY' in df_dict['name']][0]
            if not data['us10y']:
                data['us10y'] = [df_dict for df_dict in df_dicts if 'ZN' in df_dict['name']][0]
            if not data['si']:
                data['si'] = [df_dict for df_dict in df_dicts if 'SI' in df_dict['name']][0]
            if not data['gc']:
                data['gc'] = [df_dict for df_dict in df_dicts if 'GC' in df_dict['name']][0]
                print(data['gc'])
            if not data['btc']:
                check_for_btc = [df_dict for df_dict in df_dicts if df_dict['name'] == 'BTC']
                if check_for_btc:
                    data['btc'] = check_for_btc[0]
            if not data['eth']:
                check_for_eth = [df_dict for df_dict in df_dicts if df_dict['name'] == 'ETH']
                if check_for_eth:
                    data['eth'] = check_for_eth[0]

    return data

if __name__ == "__main__":
    print('running script directly through commandline')
    testing = wrangle_data()
    print(testing)
    print('finished running script')