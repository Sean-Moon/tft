import time
import datetime
from mongo_connector import MongoConnector
from handler_korbit import KorbitAPI

def preprocessing():
    print("data preparing")
    conn = MongoConnector()
    korbit = KorbitAPI()
    resp = korbit.all_detailed_ticker() 
    ts = datetime.datetime.now().timestamp()
    resp['ts'] = ts
    conn.insertData(resp)
    conn.close()

while(True):
    time.sleep(1 * 60 * 5)
    time_struct = time.localtime(time.time())
    print(time.strftime('%Y-%m-%d %I:%M:%S %p', time_struct))
    preprocessing()
