import random

import Algorithms
from Request import Request


def generateRealTime():
    req = []
    amount=10000
    disksize=200
    chanceOfRealTime=0.001
    for i in range(amount):
        if(random.random()<chanceOfRealTime):
            req.append(Request(random.randint(0, amount * 10), random.randint(0, disksize),random.randint(0,disksize) ))
        else:
            req.append(Request(random.randint(0,amount*10),random.randint(0,disksize),disksize+1))
    return req

def generateNormal():
    req = []
    amount = 100
    disksize = 200
    for i in range(amount):
        req.append(Request(random.randint(0, amount * 10), random.randint(0, disksize), disksize+1))
    return req


disk = generateNormal()

Algorithms.runFCFS(generateNormal())
Algorithms.runSSTF(generateNormal())
Algorithms.runSCAN(generateNormal())
Algorithms.runCSCAN(generateNormal())
Algorithms.runEDF(generateRealTime())
Algorithms.runFDSCAN(generateRealTime())




