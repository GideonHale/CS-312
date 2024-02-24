from collections import namedtuple

class HeapQueue:
    def __init__( self, finalNumNodes):
        # initialize everybody with the proper length to maintain constant time insert
        self.items = [None] * finalNumNodes # the actual heap, items are tuples containing an id and a value
        self.tracker = [None] * finalNumNodes # tracks the where each item is in the heap, provides the heap index for a given id
        self.size = 0
        
    Item = namedtuple('Item', ['id', 'val'])

    def insert( self, identification, value ):

        newItem = self.Item(identification, value)

        self.items[self.size] = newItem
        self.size += 1
        
        self.tracker[newItem.id] = self.size - 1

        self._floatUp(self.size - 1)
    
    def deleteMin( self ):

        firstItem = self.items[0]
        lastItem = self.items[self.size - 1]

        self.items[0] = lastItem
        self.items[self.size - 1] = None

        self.tracker[lastItem.id] = 0
        self.tracker[firstItem.id] = None

        self.size -= 1

        self._siftDown(0)

        return firstItem.id
        
    def decrease( self, nodeID, newVal ):

        heapIndex = self.tracker[nodeID]
        currItem = self.items[heapIndex]

        # assert(type(currItem) == self.Item)
        if newVal < currItem.val:
            self.items[heapIndex] = self.Item(currItem.id, newVal)
            self._floatUp(heapIndex)
            self._siftDown(heapIndex)
            return True
        
        return False
    
    def _floatUp( self, currNodePos ):

        while currNodePos > 0:
            parentPos = (currNodePos - 1) // 2

            if self.items[currNodePos].val < self.items[parentPos].val:
                self._swap(parentPos, currNodePos)
                currNodePos = parentPos

            else: return
    
    def _siftDown( self, currNodePos ):
        # loop until
            # current node has no children or
            # current node has one child and it's bigger or
            # current node has two children and both are bigger
        while True:
            currNode = self.items[currNodePos]
            lChildPos = 2 * currNodePos + 1
            rChildPos = 2 * currNodePos + 2
            if lChildPos < self.size: lChild = self.items[lChildPos]
            if rChildPos < self.size: rChild = self.items[rChildPos]

            # if there are zero or one children:
            if rChildPos > self.size - 1: # if rChild doesn't exist:
                if lChildPos > self.size - 1: return # if lChild doesn't exist: stop (we are done)
                
                if lChild.val < currNode.val: # if lChild is smaller than currNode:
                    self._swap(currNodePos, lChildPos) # swap
                    return # stop (we are done)
                
                else: return # lChild is bigger than currNode: stop (we are done)
            
            # else if both children are bigger than currNode: stop (we are done)
            elif lChild.val >= currNode.val and rChild.val >= currNode.val: return
            
            elif lChild.val <= rChild.val: # else if lChild is less than or equal to rChild:
                self._swap(currNodePos, lChildPos) # swap with lChild
                currNodePos = lChildPos # set currNode to lChild

            elif rChild.val <= lChild.val: # else if rChild is less than lChild:
                self._swap(currNodePos, rChildPos) # swap with rChild
                currNodePos = rChildPos # set currNode to rChild

            else: assert(False) # this should never happen, all cases are supposed to be covered
    
    # also rearranges self.tracker[] appropriately
    def _swap( self, index1, index2 ):

        itemA = self.items[index1]
        itemB = self.items[index2]

        # assert(type(itemA) == self.Item)
        # assert(type(itemB) == self.Item)

        self.items[index1] = itemB
        self.items[index2] = itemA
        
        trackA = self.tracker[itemA.id]
        trackB = self.tracker[itemB.id]
        self.tracker[itemA.id] = trackB
        self.tracker[itemB.id] = trackA


class ArrayQueue:
    def __init__( self, numNodes ):
        # nodes are named numerically upon insertion
        self.totalNumNodes = numNodes
        self.vals = [None] * self.totalNumNodes
        self.size = 0

    def insert( self, index, val ):
        # pretty simple operation
        self.vals[index] = val
        self.size += 1
    
    def deleteMin( self ):
        # accesses _findMin(), which takes O(n) time
        minIndex = self._findMin()
        self.vals[minIndex] = None
        self.size -= 1
        return minIndex
    
    def _findMin( self ):
        # this function takes O(1) time
        currMinIndex = 0
        for i in range(len(self.vals)):
            if self.vals[currMinIndex] == None:
                # assert(currMinIndex != len(self.vals) - 1)
                currMinIndex = i + 1
                continue

            if self.vals[i] == None: continue
            
            if self.vals[i] < self.vals[currMinIndex]: currMinIndex = i

        return currMinIndex
        
    def decrease( self, nodeID, newVal ):
        # returns true if the value was updated, false otherwise
        if newVal < self.vals[nodeID]:
            self.vals[nodeID] = newVal
            return True
        
        return False