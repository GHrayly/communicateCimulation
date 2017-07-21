# -*- coding: utf-8 -*-
import os, codecs, time, random

global tplus, infoLenth, speed, reHandShake
# definition
communicationLog = 'communication.txt'
communicationCount = 'recording.txt'
tplus = 1
infoLenth = 100
speed = 1
reHandShake = 5 # the largest range of random time delay to resend the HandShake ask when the last HandShake ask failed

# model
areaSideLength = 12 # the area the
areaSideWidth = 16
sourceAmount = 6
coverage = 8

# 每次通信5ms
# if the content of the communication is not "the message",Pls change the HandShakeRes function


def main():
    fileNum = 1
    if os.path.isfile('D:\OneDrive\python\communication\communication.txt'):
        with codecs.open('D:\OneDrive\python\communication\communication.txt', 'r', 'utf-8') as f:  # 打开文件
            first_line = f.readline()  # 读第一行
            off = -50  # 设置偏移量
            while True:
                f.seek(off, 2)  # seek(off, 2)表示文件指针：从文件末尾(2)开始向前50个字符(-50)
                lines = f.readlines()  # 读取文件指针范围内所有行
                if len(lines) >= 4:  # 判断是否最后至少有两行，这样保证了最后一行是完整的
                    last_line = lines[-3]  # 取最后一行
                    break
                # 如果off为50时得到的readlines只有一行内容，那么不能保证最后一行是完整的
                # 所以off翻倍重新运行，直到readlines不止一行
                off *= 2
        for s in last_line.split():
            if s.isdigit():
                fileNum = int(s) + 1

    with open('D:\OneDrive\python\communication\communication.txt', 'at') as f:
        print('\n*********************************\n\tcommunication start\n*********************************\n', file=f)
    t = 0
    node = makenode(areaSideLength, areaSideWidth, sourceAmount, coverage)
    node, demandNum = makeDemand(node)
    # node, demandNum = Inputnode(sourceAmount)
    while True:
        with open('D:\OneDrive\python\communication\communication.txt', 'at') as f:
            print('\n********** Time: ', t, ' **********\n', file=f)
        print('\n********** Time: ', t, ' **********\n')
        node = transportSend(node, t)
        node = transportReceive(node, t)
        node = disturbCheck(node)
        node = HandShakeRespond(node, t)
        node = HandShakeAsk(node, t)
        node = timeDelay(node, t)
        node = transportOver(node, t)
        statusReport(node)
        t += tplus
        t = round(t, 4)
        stop = True
        for nodeI in node:
            if nodeI['demand']:
                stop = False
        if stop:
            with open('D:\OneDrive\python\communication\communication.txt', 'at') as f:
                print('conmmunication stop at ', t - 1, file=f)
            print('conmmunication stop at ', t - 1)
            with open('D:\OneDrive\python\communication\communication.txt', 'at') as f:
                print('\n*********************************\n\tcommunication:\t',
                      fileNum, ' end\n*********************************\n', file=f)
            # os.system('notepad D:\OneDrive\python\communication\communication.txt')
            return fileNum, t - 1, demandNum
            exit()


def statusReport(node):
    for nodeI in node:
        if nodeI['sendFlag'] and nodeI['send']['information'] == 'HandShakeRes':
            with open('D:\OneDrive\python\communication\communication.txt', 'at') as f:
                print(nodeI['name'], '\tresponse the shake hand ask from\t', nodeI['send']['target']['name'], file=f)
            print(nodeI['name'], '\tresponse the shake hand ask from\t', nodeI['send']['target']['name'])
        if nodeI['sendFlag'] and nodeI['send']['information'] == 'the message':
            with open('D:\OneDrive\python\communication\communication.txt', 'at') as f:
                print(nodeI['name'], '\tis sending message to\t', nodeI['send']['target']['name'], file=f)
            print(nodeI['name'], '\tis sending message to\t', nodeI['send']['target']['name'])
        if nodeI['sendFlag'] and nodeI['send']['information'] == 'succeed':
            with open('D:\OneDrive\python\communication\communication.txt', 'at') as f:
                print(nodeI['name'], '\treceive message from\t', nodeI['send']['target']['name'], '\tsucceed', file=f)
            print(nodeI['name'], '\treceive message from\t', nodeI['send']['target']['name'], '\tsucceed')


def makenode(a, b, n, r):
    # 撒点，确定关系
    node = []
    for i in range(n - 1):
        node.append({'position': [random.uniform(0, a), random.uniform(0, b)]})
        node[i]['name'] = 'p%d' % (i)
        node[i]['neighbor'] = []
        node[i]['sendFlag'] = False
        node[i]['receiveFlag'] = False
        node[i]['conflict'] = False
        node[i]['future'] = {'time': None, 'sendFlag': False, 'receiveFlag': False, 'duration': 0,
                              'send': {'target': {}, 'information': None, 'admit': True}}
        with open('D:\OneDrive\python\communication\communication.txt', 'at') as f:
            print(node[i]['name'], ' at ', node[i]['position'], file=f)
        print(node[i]['name'], ' at ', node[i]['position'])
    for i in range(n - 1):  # find neighbor
        for j in range(i + 1, n - 1):
            if ((node[i]['position'][1] - node[j]['position'][1]) ** 2.0 + (
                        node[i]['position'][1] - node[j]['position'][1]) ** 2.0) ** (1 / 2) <= r:
                node[i]['neighbor'].append(node[j])
                node[j]['neighbor'].append(node[i])
    for nodeI in node:
        nodeNeighbor = []
        for p in nodeI['neighbor']:
            nodeNeighbor.append(p['name'])
        with open('D:\OneDrive\python\communication\communication.txt', 'at') as f:
            print(nodeI['name'], '\t\'s neighbor is :', nodeNeighbor, file=f)
        print(nodeI['name'], '\t\'s neighbor is :', nodeNeighbor)

    return node


def Inputnode(n):
    node = []
    demandAmount = 0
    for i in range(n - 1):
        node.append({})
        node[i]['name'] = 'p%d' % (i)
        node[i]['neighbor'] = []
        node[i]['sendFlag'] = False
        node[i]['receiveFlag'] = False
        node[i]['conflict'] = False
        node[i]['future'] = {'time': None, 'sendFlag': False, 'receiveFlag': False, 'duration': 0,
                              'send': {'target': {}, 'information': None, 'admit': True}}

    node[0]['neighbor'] = []
    node[1]['neighbor'] = [node[3], node[4]]
    node[2]['neighbor'] = []
    node[3]['neighbor'] = [node[1], node[4]]
    node[4]['neighbor'] = [node[1], node[3]]

    for nodeI in node:
        nodeNeighbor = []
        for p in nodeI['neighbor']:
            nodeNeighbor.append(p['name'])
        with open('D:\OneDrive\python\communication\communication.txt', 'at') as f:
            print(nodeI['name'], '\t\'s neighbor is :', nodeNeighbor, file=f)
        print(nodeI['name'], '\t\'s neighbor is :', nodeNeighbor)

    with open('D:\OneDrive\python\communication\communication.txt', 'at') as f:
        print('\n*************************\n', file=f)
    print('\n*************************\n')
    node[0]['demand'] = []
    node[1]['demand'] = []
    node[2]['demand'] = []
    node[3]['demand'] = [node[1], node[4]]
    node[4]['demand'] = [node[1], node[3]]
    for nodeI in node:
        if nodeI['demand']:
            nodeI['send'] = {'target': nodeI['demand'][0], 'information': None, 'admit': True, 'disturb': []}
            for demand in nodeI['demand']:
                demandAmount += 1
                with open('D:\OneDrive\python\communication\communication.txt', 'at') as f:
                    print(nodeI['name'], '\tneed send message to\t', demand['name'], file=f)
                print(nodeI['name'], '\tneed send message to\t', demand['name'])
        else:
            nodeI['send'] = {'target': {}, 'information': None, 'admit': True, 'disturb': []}
            # 多个请求
            # nodeI['send'] = random.sample(nodeI['neighbor'],random.randint(0,len(nodeI['neighbor'])))
    with open('D:\OneDrive\python\communication\\recording.txt', 'at') as f:
        print('totalDemand:\t', i, file=f)

    return node, demandAmount


def makeDemand(node):
    i = 0
    with open('D:\OneDrive\python\communication\communication.txt', 'at') as f:
        print('\n*************************\n', file=f)
    print('\n*************************\n')
    for nodeI in node:
        nodeI['demand'] = random.sample(nodeI['neighbor'], random.randint(0, len(nodeI['neighbor'])))
        if nodeI['demand']:
            nodeI['send'] = {'target': nodeI['demand'][0], 'information': None, 'admit': True, 'disturb': []}
            for demand in nodeI['demand']:
                i += 1
                with open('D:\OneDrive\python\communication\communication.txt', 'at') as f:
                    print(nodeI['name'], '\tneed send message to\t', demand['name'], file=f)
                print(nodeI['name'], '\tneed send message to\t', demand['name'])
        else:
            nodeI['send'] = {'target': {}, 'information': None, 'admit': True, 'disturb': []}
            # 多个请求
            # nodeI['send'] = random.sample(nodeI['neighbor'],random.randint(0,len(nodeI['neighbor'])))
    return node, i


def timeDelay(node, time):
    for nodeI in node:
        if nodeI['future']['time'] == time:
            nodeI['sendFlag'] = nodeI['future']['sendFlag']
            nodeI['send']['target'] = nodeI['future']['send']['target']
            nodeI['send']['information'] = nodeI['future']['send']['information']
            nodeI['send']['admit'] = nodeI['future']['send']['admit']
            nodeI['receiveFlag'] = nodeI['future']['receiveFlag']

            nodeI['future']['sendFlag'] = False
            nodeI['future']['send']['target'] = {}
            nodeI['future']['send']['information'] = None
            nodeI['future']['send']['admit'] = True
            nodeI['future']['receiveFlag'] = False
            # if
            nodeI['future']['time'] += nodeI['future']['duration']
            nodeI['future']['duration'] = 0
    return node


def HandShakeAsk(node, time):
    for nodeI in node:
        if not (nodeI['receiveFlag'] or nodeI['sendFlag'] or nodeI['send']['disturb']):
            if nodeI['demand'] and nodeI['send']['admit']:
                nodeI['sendFlag'] = True
                nodeI['send']['target'] = nodeI['demand'][0]
                nodeI['send']['information'] = 'HandShakeAsk'
                with open('D:\OneDrive\python\communication\communication.txt', 'at') as f:
                    print(nodeI['name'], '\task to shake hand with\t', nodeI['send']['target']['name'], file=f)
                print(nodeI['name'], '\task to shake hand with\t', nodeI['send']['target']['name'])
                # once-per-time ask
                nodeI['future']['time'] = time + tplus
                nodeI['future']['sendFlag'] = False
                nodeI['future']['send']['admit'] = False
                nodeI['future']['send']['information'] = None
                # resend ask at random time (until the demand desolved)
                nodeI['future']['duration'] = random.randint(1, reHandShake) * tplus
    return node


def disturbCheck(node):
    for nodeI in node:
        for s in nodeI['neighbor']:
            if s['sendFlag']:
                if s['send']['information'] == 'HandShakeRes' and s['send']['target']['name'] != \
                        nodeI['name']:  # in case disturb
                    nodeI['send']['disturb'].append(s)  # in case disturb
                if s['send']['information'] == 'succeed' or s['send']['information'] == 'failed':  # in case disturb
                    if s['send']['target']['name'] != nodeI['name']:
                        nodeI['send']['disturb'].remove(s)  # in case disturb
    return node


def HandShakeRespond(node, time):
    for nodeI in node:
        if not (nodeI['receiveFlag'] or nodeI['sendFlag']):
            sender = {'send': {'target': None}}
            i = 0
            for s in nodeI['neighbor']:
                if s['sendFlag']:
                    i = i + 1
                    sender = s
        if not (nodeI['receiveFlag'] or nodeI['sendFlag']):
            sender = {'send': {'target': None}}
            i = 0
            if not nodeI['send']['disturb']:
                for s in nodeI['neighbor']:
                    if s['sendFlag']:
                        i = i + 1
                        sender = s
            if i == 1 and sender['send']['target']['name'] == nodeI['name']:
                if not nodeI['send']['disturb']:  # prevent disturb when neighbor receiving while sending HandShakeRes
                    if sender['send']['information'] == 'HandShakeAsk':
                        nodeI['sendFlag'] = True
                        nodeI['send']['target'] = sender
                        nodeI['send']['information'] = 'HandShakeRes'
                        nodeI['future']['time'] = time + tplus
                        nodeI['future']['receiveFlag'] = True
                        nodeI['future']['duration'] = 0
    return node


def transportSend(node, time):
    tneed = infoLenth / speed
    for nodeI in node:
        if nodeI['demand']:
            if nodeI['demand'][0]['sendFlag']:
                if nodeI['demand'][0]['send']['information'] == 'HandShakeRes' and \
                                nodeI['demand'][0]['send']['target']['name'] == nodeI['name']:
                    nodeI['sendFlag'] = True
                    nodeI['send']['target'] = nodeI['demand'][0]
                    nodeI['send']['information'] = 'the message'

                    nodeI['future']['time'] = time + int(tneed) * tplus
                    nodeI['future']['sendFlag'] = False
                    nodeI['future']['send']['admit'] = True
                    nodeI['future']['duration'] = tplus
    return node


def transportReceive(node, time):
    # improve : receiver change its status automatically when sender stop sending message
    #  (rather than getting sender's stopping time)
    for nodeI in node:
        if nodeI['receiveFlag']:
            i = 0
            for s in nodeI['neighbor']:
                if s['sendFlag']:
                    i = i + 1  # shake hand influence receive
                    if s['send']['target']['name'] == nodeI['name'] and s['send']['information'] == 'the message':
                        # i += 1  # shake hand don`t influence receive
                        sender = s
            if i != 1:
                nodeI['conflict'] = True

            if time + tplus == sender['future']['time']:
                if not nodeI['conflict']:
                    nodeI['future']['time'] = sender['future']['time']
                    nodeI['future']['sendFlag'] = True
                    nodeI['future']['send']['target'] = sender
                    nodeI['future']['send']['information'] = 'succeed'
                    nodeI['future']['duration'] = tplus
                else:
                    nodeI['future']['time'] = sender['future']['time']
                    nodeI['future']['sendFlag'] = True
                    nodeI['future']['send']['target'] = sender
                    nodeI['future']['send']['information'] = 'failed'
                    nodeI['future']['duration'] = tplus
                    nodeI['conflict'] = False
                nodeI['future']['receiveFlag'] = False

    return node


def transportOver(node, time):
    for nodeI in node:
        if nodeI['demand']:
            if nodeI['demand'][0]['sendFlag'] and nodeI['demand'][0].get('send', False).get('information',
                                                                                              False) == 'succeed':
                if nodeI['demand'][0]['send']['target']['name'] == nodeI['name']:
                    # if nodeI['send']['target']['sendFlag']:
                    #     if nodeI['send']['target']['send']['information'] == 'succeed':
                    nodeI['demand'].pop(0)
    return node


if __name__ == "__main__":
    localtime = time.asctime(time.localtime(time.time()))
    with open(communicationCount, 'at') as f:
        print('\ntime:', localtime, '\ninfoLength:\t', infoLenth, ' \tspeed:\t', speed, '\treHandShakeTime:\t',
              reHandShake, file=f)
    for i in range(20):
        fileNum, time, demandAmount = main()
        with open(communicationCount, 'at') as f:
            print('number:\t', fileNum, '\tdemandAmount:\t', demandAmount, ' \truntime:\t', time, '\tefficiency:\t',
                  ((100 * (demandAmount * (infoLenth + 2) / speed) / time) if time else 100), '%', file=f)
    if os.name == 'nt':
        os.system('notepad communicationLog')
        os.system('notepad  communicationCount')
    elif os.name == 'posix':
        os.system('gedit communication.txt')
        os.system('gedit recording.txt')
    print('\nsucceed\n')
