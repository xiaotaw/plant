#encoding=utf8
import os
import sys
import time

pwd = os.path.split(os.path.realpath(__file__))[0]
parent = os.path.split(pwd)[0]

print(parent)

sys.path.append(parent)

from core import plant

test_plant = plant.Plant()
test_plant.start()

start_time = time.time()
for i in range(10):
    time.sleep(0.5)
    
    now = time.time()
    duration = now - start_time
    print(duration, test_plant.q.qsize())
