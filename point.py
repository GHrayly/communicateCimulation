class node:
    '''node : 网络中的物理节点，
        区域内容列表：队列，先进先出。　
        节点广播：周围区域内容设置为持续时间为传播时间t的广播内容，广播结束后删除内容列表队首元素，　
        接受广播：若周围区域内容列表为空，则无内容接收，若队列长度为１，则接收到队列中的内容，若队列长度大于１．则无法接受到信息（receive error)'''

    def __init__(self, location, sendArea, receiveArea, sendTime = 1):
        '''location : list, 节点坐标,[x,y]
            sendArea : int, 发送范围半径
            receiveArea :int, 接收范围半径
            sendTime : int, 发送信息持续时间'''
        location = []

    def sendInfo(self, content):
        '节点node 将内容content　进行广播'

    def receiveInfo(self):
        '节点node 查看附近区域的内容，若有且可以识别，则成功接收'