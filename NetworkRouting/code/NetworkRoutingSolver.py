from CS312Graph import *
import time
import numpy as np
import collections

class NetworkRoutingSolver:
    def __init__( self):
        pass

    def initializeNetwork( self, network ):
        assert( type(network) == CS312Graph )
        self.network = network
        self.dist = [np.inf] * len(self.network.nodes)
        self.prev = [None] * len(self.network.nodes)
        self.binaryHeap = []
        self.pointerArray = []

    def getShortestPath( self, destIndex ):
        self.dest = destIndex
        path_edges = []
        total_length = 0

        node = self.network.nodes[self.dest]
        while node.node_id != self.source:
            prevNode = node
            node = self.network.nodes[self.prev[node.node_id]] # <--- this will not work for HEAP because here is where "prev" is used
            for edge in node.neighbors:
                if edge.dest.node_id == prevNode.node_id:
                    path_edges.append( (edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)) )
                    total_length += edge.length

        return {'cost':total_length, 'path':path_edges}

    #######################
    # Time Complexity: O(1)
    #######################
    def makequeue(self):
        # populate heap array

        # SET VALUES TO DIST AND PREV
        startNode = self.network.nodes[self.source]
        self.insert_heap(0, startNode)
        for edge in startNode.neighbors:
            self.insert_heap(edge.length, edge.dest)

        return

    #######################
    # Time Complexity: O(logn)
    #######################
    def insert_heap(self, distance, nodeIn):
        index = len(self.binaryHeap)
        self.binaryHeap.append(distance)
        self.pointerArray.append(nodeIn.node_id)
        while (index != 0):
            p = self.parent(index)
            if (self.binaryHeap[p] > self.binaryHeap[index]):
                self.swap(p, index)
            index = p

    def parent(self, i):
        return (i - 1)//2

    def left_child(self, i):
        return 2*i + 1

    def right_child(self, i):
        return 2*i + 2

    #######################
    # Time Complexity: O(1)
    #######################
    def swap(self, i, j):
        self.binaryHeap[i], self.binaryHeap[j] = self.binaryHeap[j], self.binaryHeap[i]
        self.pointerArray[i], self.pointerArray[j] = self.pointerArray[j], self.pointerArray[i]

    #######################
    # Time Complexity: O(n)
    #######################
    def deletemin_array(self, tempNodes):
        # return lowest value of array
        lowestDistance = np.inf
        lowestIndex = -1
        nodeId = -1

        for i in range(len(tempNodes)):
            if lowestDistance > self.dist[tempNodes[i].node_id]:
                lowestDistance = self.dist[tempNodes[i].node_id]
                lowestIndex = i
                nodeId = tempNodes[i].node_id
        if lowestIndex != -1:
            del tempNodes[lowestIndex]

        return nodeId

    #######################
    # Time Complexity: O(n) should be O(logn
    #######################
    def decreaseKey(self, nodeIdToDecrease, updateDistance):
        for i in range(len(self.pointerArray)):                 # <---------------- CAN BE SPED UP HERE
            if nodeIdToDecrease == self.pointerArray[i]:
                self.binaryHeap[i] = updateDistance
                # change the value in heap to updateDistance
                # check if parent is bigger, if so, swap.
                index = i
                while (index != 0):
                    p = self.parent(index)
                    if (self.binaryHeap[p] > self.binaryHeap[index]):
                        self.swap(p, index)
                    index = p
                break
        return

    #########################
    # Time Complexity: O(logn)
    #########################
    def sift_down(self):
        # check right or left and replace with whichever one is smaller
        # continue until either null child or at bottom
        # if none less, then end
        index = 0
        changed = True
        while(changed):
            # if both null, break
            if (self.right_child(index) > len(self.binaryHeap)-1 and self.left_child(index) > len(self.binaryHeap)-1):
                break
            # null right, check left. if less, swap
            elif (self.right_child(index) > len(self.binaryHeap)-1):
                if (self.binaryHeap[self.left_child(index)] < self.binaryHeap[index]):
                    self.swap(self.left_child(index), index)
                    index = self.left_child(index)
                else:
                    break
            # if left < right, check left. if less, swap
            elif (self.binaryHeap[self.left_child(index)] < self.binaryHeap[self.right_child(index)]):
                if (self.binaryHeap[self.left_child(index)] < self.binaryHeap[index]):
                    self.swap(self.left_child(index), index)
                    index = self.left_child(index)
                else:
                    break
            # if left > right, check right. if less, swap
            elif (self.binaryHeap[self.left_child(index)] > self.binaryHeap[self.right_child(index)]):
                if (self.binaryHeap[self.right_child(index)] < self.binaryHeap[index]):
                    self.swap(self.right_child(index), index)
                    index = self.right_child(index)
                else:
                    break
            changed = False
        return

    ########################
    # Time Complexity: O(logn)
    ########################
    def deletemin_heap(self):
        # pop the top off of both arrays
        if (len(self.binaryHeap) == 0):
            return
        else:

            distance = self.binaryHeap.pop(0)
            i = self.pointerArray.pop(0)
            node = self.network.nodes[i]

            # set the last value to the first
            if (len(self.binaryHeap) != 0):
                bHtoAppend = self.binaryHeap.pop(len(self.binaryHeap)-1)
                self.binaryHeap.insert(0, bHtoAppend)
                pAtoAppend = self.pointerArray.pop(len(self.pointerArray)-1)
                self.pointerArray.insert(0, pAtoAppend)

                # sift down until ordered properly
                self.sift_down()

        return node, distance

    # used to populate arrays
    ###############################
    # Time Complexity Array: O(n^2)
    # Time Complexity Heap: worst case O(n^2) should be O(nlogn)
    ###############################
    def computeShortestPaths( self, srcIndex, use_heap=False ):
        # if not use heap, do priority queue
        self.source = srcIndex
        if use_heap == False:
            t1 = time.time()

            # set start distance as 0 and prev as None
            self.dist[self.source] = 0
            i = self.source
            self.prev[self.source] = None

            tempNodes = self.network.nodes[:]
            del tempNodes[self.source]

            for indx in range(len(self.network.nodes)):
                node = self.network.nodes[i] # begin with starting node
                for edge in node.neighbors: # for all edges(u, v) in E:
                    alt = self.dist[i] + edge.length
                    if (self.dist[edge.dest.node_id] > alt):
                        self.dist[edge.dest.node_id] = alt
                        self.prev[edge.dest.node_id] = edge.src.node_id
                i = self.deletemin_array(tempNodes)
            t2 = time.time()
        else:
            t1 = time.time()

            # else use heap
            self.source = srcIndex
            # set start distance as 0 and prev as None
            self.dist[self.source] = 0
            self.prev[self.source] = None

            self.makequeue()  # using dist-values as keys
            while len(self.binaryHeap) != 0:
                node, distance = self.deletemin_heap()

                for edge in node.neighbors:
                    alt = self.dist[edge.src.node_id] + edge.length
                    if (self.dist[edge.dest.node_id] == np.inf):
                        self.insert_heap( alt, edge.dest)
                        #self.dist[edge.dest.node_id] = edge.length
                        self.prev[edge.dest.node_id] = node.node_id
                    old = self.dist[edge.dest.node_id]
                    if (old > alt):
                        self.dist[edge.dest.node_id] = alt
                        self.prev[edge.dest.node_id] = edge.src.node_id
                        self.decreaseKey(edge.dest.node_id, self.dist[edge.src.node_id] + edge.length)
            t2 = time.time()
        return (t2-t1)

