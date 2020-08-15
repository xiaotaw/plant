#
import os
import sys
pwd = os.path.split(os.path.realpath(__file__))[0]
parent = os.path.split(pwd)[0]
grandparent = os.path.split(parent)[0]

sys.path.append(parent)

print("pwd: %s" % pwd)
print("parent: %s" % parent)
print("grandparent: %s" % grandparent)