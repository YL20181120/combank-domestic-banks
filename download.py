import json
import time

import requests

def get_branches(code: str):
    url = "https://www.seylanbank.lk/corporate/corporate/account/fundtransfer/unregistered/getBranches"

    payload = f'type={code}&accountCard=account'
    headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'origin': 'https://www.seylanbank.lk',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'referer': 'https://www.seylanbank.lk/corporate/',
        'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
        'x-csrf-token': '2653e3f9-3293-40dc-a2d1-055d891d25b3',
        'x-requested-with': 'XMLHttpRequest',
        'Cookie': 'TS019e1da7=010e7b7cc21db04a7dbc933727b7db80a0fa98bd09c0352bf37abceed44de1470ed5e5894b6f7c16396145241168df45c316c8e4fb; JSESSIONID=A27710F8BD609A354CD3701925470B6E; _ga=GA1.2.783324133.1777001708; style=null; JSESSIONID=3510D02A688500FC32FD3FAB98A8A489; _gid=GA1.2.1571444028.1781065432; TS01dc4fc6=010e7b7cc269fe42d9302921197a4ecd39a30c7b48d80803aa864d6c1732e01ed7e00aa2ff95b7f9af08053218af771d683e3caad8; _ga_0KWDJPHHQP=GS2.2.s1781160030$o20$g1$t1781161578$j60$l0$h0',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    with open(f'{code}.json', 'w') as f:
        f.write(response.text)
banks = """
[
    {
        "version": 1,
        "bankCode": "7463",
        "bankName": "AMANA BANK PLC",
        "slipEnable": true,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": false,
        "remarks": "",
        "ceftBankCode": "6463"
    },
    {
        "version": 0,
        "bankCode": "7676",
        "bankName": "ASIA ASSET FINANCE",
        "slipEnable": true,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": false,
        "remarks": null,
        "ceftBankCode": "6676"
    },
    {
        "version": 2,
        "bankCode": "7010",
        "bankName": "BANK OF CEYLON",
        "slipEnable": true,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": true,
        "remarks": "",
        "ceftBankCode": "6010"
    },
    {
        "version": 0,
        "bankCode": "7700",
        "bankName": "BANK OF CHINA LIMITED",
        "slipEnable": false,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": false,
        "remarks": null,
        "ceftBankCode": "6700"
    },
    {
        "version": 1,
        "bankCode": "7481",
        "bankName": "CARGILLS BANK LTD",
        "slipEnable": true,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": true,
        "remarks": "",
        "ceftBankCode": "6481"
    },
    {
        "version": 0,
        "bankCode": "6667",
        "bankName": "CBC FINANCE LIMITED",
        "slipEnable": false,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": false,
        "remarks": null,
        "ceftBankCode": "6667"
    },
    {
        "version": 1,
        "bankCode": "7825",
        "bankName": "CENTRAL FINANCE COMP",
        "slipEnable": true,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": false,
        "remarks": "",
        "ceftBankCode": "6825"
    },
    {
        "version": 2,
        "bankCode": "7047",
        "bankName": "CITI BANK",
        "slipEnable": true,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": false,
        "remarks": "",
        "ceftBankCode": "6047"
    },
    {
        "version": 1,
        "bankCode": "7746",
        "bankName": "CITIZENS DEV.BUS FIN",
        "slipEnable": true,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": false,
        "remarks": "",
        "ceftBankCode": "6746"
    },
    {
        "version": 5,
        "bankCode": "7056",
        "bankName": "COMMERCIAL BANK",
        "slipEnable": true,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": true,
        "remarks": "",
        "ceftBankCode": "6056"
    },
    {
        "version": 0,
        "bankCode": "6870",
        "bankName": "COMMERCIAL CREDIT AND FINANCE PLC",
        "slipEnable": false,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": false,
        "remarks": null,
        "ceftBankCode": "6870"
    },
    {
        "version": 1,
        "bankCode": "7205",
        "bankName": "DEUTSCHE BANK (ASIA)",
        "slipEnable": true,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": false,
        "remarks": "",
        "ceftBankCode": "6205"
    },
    {
        "version": 4,
        "bankCode": "7454",
        "bankName": "DFCC  BANK PLC",
        "slipEnable": true,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": true,
        "remarks": "",
        "ceftBankCode": "6454"
    },
    {
        "version": 0,
        "bankCode": "7995",
        "bankName": "DIALOG FINANCE PLC",
        "slipEnable": true,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": false,
        "remarks": null,
        "ceftBankCode": "6995"
    },
    {
        "version": 0,
        "bankCode": "7940",
        "bankName": "FINTREX FINANCE LTD",
        "slipEnable": true,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": false,
        "remarks": null,
        "ceftBankCode": "6940"
    },
    {
        "version": 1,
        "bankCode": "7074",
        "bankName": "HABIB BANK LTD",
        "slipEnable": true,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": false,
        "remarks": "",
        "ceftBankCode": "6074"
    },
    {
        "version": 1,
        "bankCode": "7083",
        "bankName": "HATTON NATIONAL BANK",
        "slipEnable": true,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": true,
        "remarks": "",
        "ceftBankCode": "6083"
    },
    {
        "version": 1,
        "bankCode": "7737",
        "bankName": "HDFC BANK",
        "slipEnable": true,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": false,
        "remarks": "",
        "ceftBankCode": "6737"
    },
    {
        "version": 3,
        "bankCode": "7904",
        "bankName": "HNB FINANCE PLC",
        "slipEnable": true,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": false,
        "remarks": null,
        "ceftBankCode": "6904"
    },
    {
        "version": 2,
        "bankCode": "7092",
        "bankName": "HONGKONG&SHANGHAI BK",
        "slipEnable": true,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": true,
        "remarks": "",
        "ceftBankCode": "6092"
    },
    {
        "version": 1,
        "bankCode": "7108",
        "bankName": "INDIAN BANK",
        "slipEnable": true,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": false,
        "remarks": "",
        "ceftBankCode": "6108"
    },
    {
        "version": 2,
        "bankCode": "7117",
        "bankName": "INDIAN OVERSEAS BANK",
        "slipEnable": true,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": false,
        "remarks": "",
        "ceftBankCode": "6117"
    },
    {
        "version": 0,
        "bankCode": "6987",
        "bankName": "JANASHAKTHI FINANCE PLC",
        "slipEnable": false,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": false,
        "remarks": null,
        "ceftBankCode": "6987"
    },
    {
        "version": 1,
        "bankCode": "7773",
        "bankName": "LB FINANCE PLC",
        "slipEnable": true,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": false,
        "remarks": "",
        "ceftBankCode": "6773"
    },
    {
        "version": 1,
        "bankCode": "7977",
        "bankName": "LOLC DEVELOPMENT FINANCE PLC",
        "slipEnable": true,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": false,
        "remarks": null,
        "ceftBankCode": "6977"
    },
    {
        "version": 5,
        "bankCode": "7861",
        "bankName": "LOLC FINANCE PLC",
        "slipEnable": true,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": true,
        "remarks": "",
        "ceftBankCode": "6861"
    },
    {
        "version": 0,
        "bankCode": "6845",
        "bankName": "MAHINDRA IDEAL FINANCE",
        "slipEnable": false,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": false,
        "remarks": null,
        "ceftBankCode": "6845"
    },
    {
        "version": 2,
        "bankCode": "7898",
        "bankName": "MBSL & FINANCE SL",
        "slipEnable": true,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": false,
        "remarks": "",
        "ceftBankCode": "6898"
    },
    {
        "version": 1,
        "bankCode": "7269",
        "bankName": "MUSLIM COMMERCIAL BK",
        "slipEnable": true,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": false,
        "remarks": "",
        "ceftBankCode": "6269"
    },
    {
        "version": 1,
        "bankCode": "7162",
        "bankName": "NATION'S TRUST BANK",
        "slipEnable": true,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": true,
        "remarks": "",
        "ceftBankCode": "6162"
    },
    {
        "version": 1,
        "bankCode": "7719",
        "bankName": "NATIONAL SAVINGS BNK",
        "slipEnable": true,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": false,
        "remarks": "",
        "ceftBankCode": "6719"
    },
    {
        "version": 1,
        "bankCode": "7214",
        "bankName": "NDB BANK",
        "slipEnable": true,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": true,
        "remarks": "",
        "ceftBankCode": "6214"
    },
    {
        "version": 3,
        "bankCode": "7311",
        "bankName": "PAN ASIA BANK LTD",
        "slipEnable": true,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": true,
        "remarks": "",
        "ceftBankCode": "6311"
    },
    {
        "version": 2,
        "bankCode": "7135",
        "bankName": "PEOPLES BANK",
        "slipEnable": true,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": true,
        "remarks": "",
        "ceftBankCode": "6135"
    },
    {
        "version": 3,
        "bankCode": "7922",
        "bankName": "PEOPLES LEASING",
        "slipEnable": true,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": false,
        "remarks": null,
        "ceftBankCode": "6922"
    },
    {
        "version": 1,
        "bankCode": "7296",
        "bankName": "PUBLIC BANK",
        "slipEnable": true,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": false,
        "remarks": "",
        "ceftBankCode": "6296"
    },
    {
        "version": 1,
        "bankCode": "7755",
        "bankName": "REGIONAL DEVELOPMENT",
        "slipEnable": true,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": false,
        "remarks": "",
        "ceftBankCode": "6755"
    },
    {
        "version": 1,
        "bankCode": "7278",
        "bankName": "SAMPATH BANK",
        "slipEnable": true,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": true,
        "remarks": "",
        "ceftBankCode": "6278"
    },
    {
        "version": 2,
        "bankCode": "7728",
        "bankName": "SANASA DEVELOPMENT",
        "slipEnable": true,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": false,
        "remarks": "",
        "ceftBankCode": "6728"
    },
    {
        "version": 0,
        "bankCode": "7931",
        "bankName": "SARVODAYA DEVELOPMENT FINANCE LIMITED",
        "slipEnable": true,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": false,
        "remarks": null,
        "ceftBankCode": "6931"
    },
    {
        "version": 0,
        "bankCode": "7782",
        "bankName": "SENKADAGALA FINANCE",
        "slipEnable": true,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": false,
        "remarks": "",
        "ceftBankCode": "6782"
    },
    {
        "version": 0,
        "bankCode": "6630",
        "bankName": "SINGER FINANCE PLC",
        "slipEnable": false,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": false,
        "remarks": null,
        "ceftBankCode": "6630"
    },
    {
        "version": 0,
        "bankCode": "6603",
        "bankName": "SOFTLOGIC FINANCE",
        "slipEnable": true,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": false,
        "remarks": null,
        "ceftBankCode": "6603"
    },
    {
        "version": 2,
        "bankCode": "7038",
        "bankName": "STANDARD CHARTERED",
        "slipEnable": true,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": true,
        "remarks": "",
        "ceftBankCode": "6038"
    },
    {
        "version": 2,
        "bankCode": "7144",
        "bankName": "STATE BANK OF INDIA",
        "slipEnable": true,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": false,
        "remarks": "",
        "ceftBankCode": "6144"
    },
    {
        "version": 0,
        "bankCode": "7302",
        "bankName": "UNION BNK OF CMB PLC",
        "slipEnable": true,
        "ceftEnable": true,
        "cardSlipEnable": false,
        "cardCeftEnable": false,
        "remarks": "",
        "ceftBankCode": "6302"
    }
]
"""
data = json.loads(banks)
for bank in data:
    get_branches(bank['bankCode'])
    time.sleep(10)