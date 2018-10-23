#!/usr/bin/python3


from CS312Graph import *
import time
import math


class NetworkRoutingSolver:
    def __init__(self):
        pass

    def initializeNetwork(self, network):
        assert(type(network) == CS312Graph)
        self.network = network

    def getShortestPath(self, destIndex):
        self.dest = destIndex

        path_edges = []
        total_length = 0

        destNode = self.network.nodes[self.dest]
        node = destNode
        srcNode = self.network.nodes[self.source]

        while(node.node_id != srcNode.node_id):
            prevNodeId = self.prevNodes[node.node_id]
            # This node is the srcNode
            if (prevNodeId == -1):
                prevNodeId = srcNode.node_id
             # This destination node is not reachable
            elif(prevNodeId is None):
                return {'cost': math.inf, 'path': []}

            prevNode = self.network.nodes[prevNodeId]

            for edge in prevNode.neighbors:
                if (edge.dest.node_id == node.node_id):
                    total_length += edge.length
                    path_edges.append(
                        (edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)))
                    node = prevNode

        return {'cost': total_length, 'path': path_edges}

    def computeShortestPaths(self, srcIndex, use_heap=False):
        self.source = srcIndex

        t1 = time.time()
        if (use_heap == True):
            # Use heap implementation
            queue = PriorityQueueHeap()
        else:
            # Use the unsorted array implementation
            queue = PriorityQueueArray()

        self.dijkstrasAlgorithm(self.network, self.source,
                                queue)

        t2 = time.time()
        return (t2-t1)

    def dijkstrasAlgorithm(self, graph, srcNodeId, queueObj):
        # TODO comments
        self.distances = dict()
        self.prevNodes = dict()

        for node in graph.getNodes():
            self.distances[node.node_id] = math.inf
            self.prevNodes[node.node_id] = None

        self.distances[srcNodeId] = 0
        self.prevNodes[srcNodeId] = -1

        queueObj.makeQueue(graph.nodes)
        while (len(queueObj.queue) > 0):
            currNode = queueObj.deleteMin(self.distances)
            for edge in currNode.neighbors:
                neighborNode = edge.dest
                distanceBetween = self.distances[currNode.node_id] + edge.length
                if (self.distances[neighborNode.node_id] > distanceBetween):
                    self.prevNodes[neighborNode.node_id] = currNode.node_id
                    self.distances[neighborNode.node_id] = distanceBetween
                    queueObj.decreaseKey(neighborNode)


class PriorityQueueHeap:
    def __init__(self):
        self.queue = list()
        pass

    def makeQueue(self, nodes):
        pass

    def insert(self, node):
        self.queue.append(node)

    def deleteMin(self, distances):
            # Delete the first one and return it
        pass

    def decreaseKey(self, nodeToChange):
        pass


class PriorityQueueArray:
    def __init__(self):
        self.queue = list()
        pass

    def makeQueue(self, nodes):
        # Make the queue from the list of nodes

        for x in nodes:
            self.insert(x)

    def insert(self, node):
        # Adds the node into the queue

        self.queue.append(node)

    def deleteMin(self, distances):
        # Find the node that currently has the shortest path
        #  then pop it off the queue and return it

        minNodeVal = math.inf
        minNode = None
        minNodeIndex = 0
        for i, node in enumerate(self.queue):
            if (distances[node.node_id] < minNodeVal):
                minNodeVal = distances[node.node_id]
                minNode = node
                minNodeIndex = i

        # I put this here for the odd ball case where some nodes
        # in the queue are unreachable and therefore have a distance values of INF
        # Having the value of INF causes them to not be caught by the if statement
        # in the for loop above. So I just take whatever is first in the queue
        if(minNode is None):
            minNode = self.queue[0]

        del self.queue[minNodeIndex]
        return minNode

    def decreaseKey(self, nodeToChange):
        # Nothing to be done here
        pass
