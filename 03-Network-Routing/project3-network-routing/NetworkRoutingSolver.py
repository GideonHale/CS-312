# !/usr/bin/python3


from CS312Graph import *
import time
from PriorityQueue import *


class NetworkRoutingSolver:
    def __init__( self ):
        pass

    def initializeNetwork( self, network ):
        assert( type(network) == CS312Graph )
        self.network = network

    def computeShortestPaths( self, srcIndex, use_heap=False ):
        self.source = srcIndex
        t1 = time.time()

        self._dijkstra(srcIndex, use_heap)
        
        t2 = time.time()
        return (t2-t1)
    
    def _dijkstra( self, srcIndex, heapImpl ):
        allNodes = self.network.nodes

        # heapImpl = False # fixme: remove this later

        if heapImpl:
            pQueue = HeapQueue(len(allNodes))
        else:
            pQueue = ArrayQueue(len(allNodes))
        
        self.distances = [float('inf') for _ in range(len(allNodes))]
        self.distances[srcIndex] = 0
        self.prevNodes = {node.node_id: None for node in self.network.getNodes()}

        for node in allNodes: pQueue.insert(node.node_id, self.distances[node.node_id])
        while pQueue.size != 0:
            currSrc = pQueue.deleteMin()
            for edge in allNodes[currSrc].neighbors:
                assert(type(edge) == CS312GraphEdge)
                currDest = edge.dest.node_id
                if self.distances[currSrc] + edge.length < self.distances[currDest]:
                    self.distances[currDest] = self.distances[currSrc] + edge.length
                    self.prevNodes[currDest] = currSrc
                    pQueue.decrease(currDest, self.distances[currDest])

    def getShortestPath( self, destIndex ):
        totalLength = self.distances[destIndex]

        if totalLength == float('inf'): return {'cost':float('inf'), 'path':[]}

        # get the indices for the path
        pathIndices = []
        currPrevIndex = destIndex
        while currPrevIndex != self.source:
            pathIndices.append(currPrevIndex)
            currPrevIndex = self.prevNodes[currPrevIndex]
        pathIndices.append(self.source)
        # pathIndices now starts with the final destination and ends with the source

        # calculate distances
        edgeDists = []
        lengthLeft = totalLength
        for i in range(len(pathIndices) - 1):
            subLength = self.distances[pathIndices[i + 1]]
            edgeDists.append(lengthLeft - subLength)
            lengthLeft = subLength
        # edgeDists starts at the back and goes in reverse order like pathIndices

        # construct path (in reverse)
        pathEdges = []
        for i in range(len(edgeDists)):
            pathEdges.append( (self.network.nodes[pathIndices[i]].loc,
                               self.network.nodes[pathIndices[i + 1]].loc,
                               '{:.0f}'.format(edgeDists[i])) )
        
        pathEdges = reversed(pathEdges)

        return {'cost':totalLength, 'path':pathEdges}