import functools
import requests
import time

from fastapi import FastAPI, Response
from textwrap import dedent

app = FastAPI()

class HashableDict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))

@app.get("/")
async def root():
    data = '''
    <html>
    <head><title>Selectel Balance Exporter</title></head>
    <body>
            <h1>Selectel Exporter</h1>
            <p><a href="/probe?api_token=XXXXXXX">probe Selectel with given API token</a></p>
    </body>
    </html>
    '''
    return Response(content=data)

@app.get("/probe")
async def probe(
        api_token: str,
        target: str = "https://api.selectel.ru/v3/billing/balance",
        billing: str = "vpc",  # gotten from https://developers.selectel.ru/docs/control-panel/balance/
        with_prediction: str = "1",  # gotten from the same page as previous one
        force: bool = False,
        verbose: bool = False,
        cache_age = 60 * 60):
    
    if force:
        get_balance.cache_clear()
    balanceResponse = get_balance(
        api_token = api_token,
        url = target,
        params = HashableDict({"billing": billing, "with_prediction": with_prediction}),
        ttl = time.time() // cache_age,
    )

    probeSuccess = 1 if balanceResponse else 0
    expiryDays = balanceResponse["data"][billing]["prediction"]["days"]
    account_sum = int(balanceResponse["data"][billing]["sum"]) / 100
    balanceResponseInfo = dedent(f"""
        # HELP balance_expiry_days time in days until there will be no money on the account
        # TYPE balance_expiry_days gauge
        balance_expiry_days {expiryDays}
        # HELP balance_probe_success whether the probe was successful or not
        # TYPE balance_probe_success gauge
        balance_probe_success {probeSuccess}
        # HELP balance_sum current sum on the account
        # TYPE balance_sum gauge
        balance_sum {int(account_sum)}
    """)
    return Response(content=balanceResponseInfo)

@functools.lru_cache()
def get_balance(
        api_token: str,
        url: str,
        params: HashableDict,
        ttl):
    headers = {"Content-Type": "application/json", "X-Token": api_token}
    r = requests.get(url, params=params, headers=headers)
    return r.json()