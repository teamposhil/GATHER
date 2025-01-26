from pymongo import MongoClient
from dotenv import load_dotenv
import os
import random
import time
load_dotenv()  # .env 파일 로드
MONGO_URI = os.getenv("MONGO_URI")
# MongoDB 클라이언트 설정
client = MongoClient(MONGO_URI)
userdb = client["user"]  # 데이터베이스 이름
user_collection = userdb["user"]

stockdb = client["stocks"]
stock_domestic_collection = stockdb["domestic"]
stock_international_collection = stockdb["international"]
rate_collection = stockdb["rate"]
gmtodt_collection = stockdb["gmtodt"]
sasungin = stock_international_collection.find_one({"company_name": "SASUNG"})["price"]
pear = stock_international_collection.find_one({"company_name": "PEAR"})["price"]
envidia = stock_international_collection.find_one({"company_name": "ENVIDIA"})["price"]
hiot = stock_international_collection.find_one({"company_name": "HIOTGAMES"})["price"]
qalmart = stock_international_collection.find_one({"company_name": "QALMART"})["price"]
ppizer = stock_international_collection.find_one({"company_name": "PPIZER"})["price"]
sasungdo = stock_domestic_collection.find_one({"company_name": "SASUNG"})["price"]
og= stock_domestic_collection.find_one({"company_name": "OG"})["price"]
jongshim = stock_domestic_collection.find_one({"company_name": "jongshim"})["price"]
lyundai = stock_domestic_collection.find_one({"company_name": "lyundai"})["price"]
rate = rate_collection.find_one({"codecheck": "code"})["rate"]
gmtodt = gmtodt_collection.find_one({"codecheck": "code"})["gmtodt"]
def int_stock_price(stock_name,price,rate):
    return_price = int(price*rate)

    stock_international_collection.update_one({"company_name":stock_name}, {"$set":{"price":int(return_price/10*10)}})
    return return_price
def dom_stock_price(stock_name,price,rate):
    return_price = int(price*rate)
    stock_domestic_collection.update_one({"company_name":stock_name}, {"$set":{"price":int(return_price/10*10)}})
def gmtodt_price():
    return_price = random.randint(900, 1500)
    gmtodt_collection.update_one({"codecheck":"code"}, {"$set":{"gmtodt":int(return_price)}})
while(True):
    stockdb = client["stocks"]
    stock_domestic_collection = stockdb["domestic"]
    stock_international_collection = stockdb["international"]
    rate_collection = stockdb["rate"]
    gmtodt_collection = stockdb["gmtodt"]
    sasungin = stock_international_collection.find_one({"company_name": "SASUNG"})["price"]
    pear = stock_international_collection.find_one({"company_name": "PEAR"})["price"]
    envidia = stock_international_collection.find_one({"company_name": "ENVIDIA"})["price"]
    hiot = stock_international_collection.find_one({"company_name": "HIOTGAMES"})["price"]
    qalmart = stock_international_collection.find_one({"company_name": "QALMART"})["price"]
    ppizer = stock_international_collection.find_one({"company_name": "PPIZER"})["price"]
    sasungdo = stock_domestic_collection.find_one({"company_name": "SASUNG"})["price"]
    og = stock_domestic_collection.find_one({"company_name": "OG"})["price"]
    jongshim = stock_domestic_collection.find_one({"company_name": "jongshim"})["price"]
    lyundai = stock_domestic_collection.find_one({"company_name": "lyundai"})["price"]
    rate = rate_collection.find_one({"codecheck": "code"})["rate"]
    gmtodt = gmtodt_collection.find_one({"codecheck": "code"})["gmtodt"]
    rate = random.randint(70, 130) / 100
    print(sasungin, pear, envidia, hiot, qalmart, ppizer, sasungdo, og, jongshim, lyundai, rate)
    sasungin = int_stock_price("SASUNG",sasungin, rate)
    pear = int_stock_price("PEAR",pear, rate)
    envidia = int_stock_price("ENVIDIA",envidia, rate)
    hiot = int_stock_price("HIOTGAMES",hiot, rate)
    qalmart = int_stock_price("QALMART",qalmart, rate)
    ppizer = int_stock_price("PPIZER",ppizer, rate)
    sasungdo = dom_stock_price("SASUNG",sasungdo, rate)
    og = dom_stock_price("OG",og, rate)
    jongshim = dom_stock_price("jongshim",jongshim, rate)
    lyundai = dom_stock_price("lyundai",lyundai, rate)
    rate = rate_collection.update_one({"codecheck":"code"}, {"$set":{"rate":rate}})
    gmtodt = gmtodt_price()
    time.sleep(60)

