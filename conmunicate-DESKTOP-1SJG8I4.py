# -*- coding: utf-8 -*-
# time
global tplus, infoLenth, speed, reShakeHand
tplus = 1
infoLenth = 4
speed = 1
reShakeHand = 10
# modle
areaSideLength = 12
areaSideWidth = 16
sourceAmount = 4
coverage = 8
# 每次通信5ms

import random


def main():
    t = 0
    point = makePoint(areaSideLength, areaSideWidth, sourceAmount, coverage)
    point = makeDemand(point)
    while True:
        point = timeDelay(point, t)
        point = conmunicate(point, t)
        t += tplus
        t = round(t,4)
        stop = True
        for pointI in point:
            if pointI['demand'] != []:
                stop = False
        if stop:
            print(t)
            exit()


def makePoint(a, b, n, r):
    # 撒点，确定关系
    point = []
    for i in range(n - 1):
        point.append({'position': [random.uniform(0, a), random.uniform(0, b)]})
        point[i]['name'] = 'p%d\t' % (i)
        point[i]['neighbor'] = []
        point[i]['sendFlag'] = False
        point[i]['receiveFlag'] = False
        point[i]['conflict'] = False
        point[i]['future'] = {'time': None, 'sendFlag': False, 'receiveFlag': False, 'duration': 0,
                              'send': {'target': {}, 'information': None, 'admit': True}}
        print(point[i]['name'], '\tat\t', point[i]['position'], '\n')
    for i in range(n - 1):  # find neighbor
        for j in range(i + 1, n - 1):
            if ((point[i]['position'][1] - point[j]['position'][1]) ** 2.0 + (
                        point[i]['position'][1] - point[j]['position'][1]) ** 2.0) ** (1 / 2) <= r:
                point[i]['neighbor'].append(point[j])
                point[j]['neighbor'].append(point[i])
    return point


def makeDemand(point):
    for pointI in point:
        pointI['demand'] = random.sample(pointI['neighbor'], random.randint(0, min(1, len(pointI['neighbor']))))
        if pointI['demand']:
            pointI['send'] = {'target': pointI['demand'][0], 'information': None, 'admit': True}
        else:
            pointI['send'] = {'target': {}, 'information': None, 'admit': True}
        # 多个请求
        # pointI['send'] = random.sample(pointI['neighbor'],random.randint(0,len(pointI['neighbor'])))
    return point


def timeDelay(point, time):
    for pointI in point:
        if pointI['future']['time'] == time:
            pointI['sendFlag'] = pointI['future']['sendFlag']
            pointI['send']['target'] = pointI['future']['send']['target']
            pointI['send']['information'] = pointI['future']['send']['information']
            pointI['send']['admit'] = pointI['future']['send']['admit']
            pointI['receiveFlag'] = pointI['future']['receiveFlag']

            pointI['future']['sendFlag'] = False
            pointI['future']['send']['target'] = {}
            pointI['future']['send']['information'] = None
            pointI['future']['send']['admit'] = True
            pointI['future']['receiveFlag'] = False
            # if
            pointI['future']['time'] += pointI['future']['duration']
            pointI['future']['duration'] = 0
    return point


def conmunicate(point, time):
    point = transportReceive(point, time)
    point = transportOver(point, time)
    point = transportSend(point, time)
    point = shakeHandRespond(point, time)
    point = shakeHandAsk(point, time)
    return point


def shakeHandAsk(point, time):
    for pointI in point:
        if not (pointI['receiveFlag'] or pointI['sendFlag']):
            if pointI['demand'] and pointI['send']['admit']:
                pointI['sendFlag'] = True
                pointI['send']['target'] = pointI['demand'][0]
                pointI['send']['information'] = 'shakeHandAsk'
                # once-per-time ask
                pointI['future']['time'] = time + tplus
                pointI['future']['sendFlag'] = False
                pointI['future']['send']['admit'] = False
                pointI['future']['send']['information'] = None
                # resend ask at random time (untill the demand desolved)
                pointI['future']['duration'] = random.randint(1, reShakeHand) * tplus
    return point


def shakeHandRespond(point, time):
    for pointI in point:
        if not (pointI['receiveFlag'] or pointI['sendFlag']):
            sender = pointI
            i = 0
            for s in pointI['neighbor']:
                if s['sendFlag']:
                    i = i + 1
                    sender = s
            if i == 1 and sender['send']['target'] == pointI:
                pointI['sendFlag'] = True
                pointI['send']['target'] = sender
                pointI['send']['information'] = 'shakeHandRes'
                pointI['future']['time'] = time + tplus
                pointI['future']['receiveFlag'] = True
                pointI['future']['duration'] =
    return point


def transportSend(point, time):
    tneed = infoLenth / speed
    for pointI in point:
        if pointI['send']['target']:
            if pointI['send']['target']['send']['information'] == 'shakeHandRes':
                pointI['sendFlag'] = True
                pointI['send']['information'] = 'the message'

                pointI['future']['time'] = time + int(tneed)*tplus
                pointI['future']['sendFlag'] = False
                pointI['future']['send']['admit'] = True
                pointI['future']['duration'] = tplus
    return point


def transportReceive(point, time):
    for pointI in point:
        if pointI['receiveFlag']:
            i = 0
            for s in pointI['neighbor']:
                if s['sendFlag']:
                    i = i + 1
                    sender = s
            if i != 1:
                pointI['conflict'] = True

            if time + tplus == sender['future']['time']:
                if not pointI['conflict']:
                    pointI['future']['time'] = sender['future']['time']
                    pointI['future']['sendFlag'] = True
                    pointI['future']['send']['target'] = sender
                    pointI['future']['send']['information'] = 'succeed'
                    pointI['future']['duration'] = tplus
                else:
                    pointI['future']['time'] = time + tplus
                    pointI['conflict'] = False
                pointI['future']['receiveFlag'] = False

    return point


def transportOver(point, time):
    for pointI in point:
        if pointI['sendFlag']:
           if pointI['send']['target']['sendFlag']:
               if pointI['send']['target']['send']['information'] == 'succeed':
                   pointI['demand'] = []
    return point


if __name__ == "__main__":
    main()
