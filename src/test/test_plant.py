#encoding=utf8
import os
import sys
import time

from src.core import plant

test_plant = plant.Plant()
test_plant.start()

start_time = time.time()
for i in range(10):
    time.sleep(0.5)
    
    now = time.time()
    duration = now - start_time
    print(duration, test_plant.q.qsize())
