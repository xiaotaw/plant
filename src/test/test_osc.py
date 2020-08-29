#encoding=utf8
# refrence: https://pypi.org/project/python-osc/

import time
import random

from pythonosc import udp_client


client = udp_client.SimpleUDPClient("127.0.0.1", 10000)

for x in range(10000):
    client.send_message("/*", x)
    time.sleep(1)