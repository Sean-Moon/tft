import time


tm = time.localtime(time.time())
item = time.strftime('%Y-%m-%d %I:%M:%S %p', tm)
print(item)
print(time.time() / 60)
time.sleep(1 * 60 * 5)
print(time.time() / (60*60*24))