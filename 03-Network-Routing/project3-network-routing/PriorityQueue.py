from collections import namedtuple

# We shall assume that memory allocation requires O(1) time. Also all methods and
# operations for this class require O(n) space complexity total, n being the
# maximum number of items.
class HeapQueue:
    def __init__( self, maxNumNodes):
        # We'll initialize everybody with proper length to maintain constant time append.
        # The actual heap, its items being tuples containing an id and a value.
        self.items = [None] * maxNumNodes # O(1) time, O(n) space
        # The location of each item in the heap, indexed by id.
        self.tracker = [None] * maxNumNodes # O(1) time, O(n) space
        # running size of the portion of the heap in current use
        self.size = 0
        
    Item = namedtuple('Item', ['id', 'val'])

    # O(logn) time, O(1) space
    def insert( self, id, val ):

        newItem = self.Item(id, val)

        self.items[self.size] = newItem
        self.size += 1
        
        self.tracker[newItem.id] = self.size - 1

        self._floatUp(self.size - 1) # O(logn) time, see _floatUp() below
    
    # O(logn) time, O(1) space
    def deleteMin( self ):

        firstItem = self.items[0]
        lastItem = self.items[self.size - 1]

        self.items[0] = lastItem
        self.items[self.size - 1] = None

        self.tracker[lastItem.id] = 0
        self.tracker[firstItem.id] = None

        self.size -= 1

        self._siftDown(0) # O(logn) time, see _siftDown() below

        return firstItem.id
        
    # O(logn) time, O(1) space
    def decrease( self, nodeID, newVal ):

        heapIndex = self.tracker[nodeID]
        currItem = self.items[heapIndex]

        if newVal < currItem.val:
            self.items[heapIndex] = self.Item(currItem.id, newVal)
            self._floatUp(heapIndex) # O(logn) time, see _floatUP() below
            self._siftDown(heapIndex) # O(logn) time, see _siftDown() below
            return True
        
        return False
    
    # O(logn) time, O(1) space
    def _floatUp( self, currNodePos ):
        # This is where logn complexity is caused throughout the whole data structure.

        # the heap always has a depth of logn, so this will loop no more than logn times
        while currNodePos > 0: # all the other stuff in here takes O(1) time
            parentPos = (currNodePos - 1) // 2

            if self.items[currNodePos].val < self.items[parentPos].val:
                self._swap(parentPos, currNodePos) # O(1) time, see _swap() below
                currNodePos = parentPos

            else: return
    
    # O(logn) time, O(1) space
    def _siftDown( self, currNodePos ):
        # This was probably the most complicated function to write and thereby
        # caused a lot of bugs. I hope you appreciate it.
        # This is where logn complexity is caused throughout the whole data structure.

        # loop until
            # current node has no children or
            # current node has one child and it's bigger or
            # current node has two children and both are bigger
        # this loops potentially from root to leaf node, which is at most logn times
        # everything else takes O(1) time
        while True:
            currNode = self.items[currNodePos]
            lChildPos = 2 * currNodePos + 1
            rChildPos = 2 * currNodePos + 2
            if lChildPos < self.size: lChild = self.items[lChildPos]
            if rChildPos < self.size: rChild = self.items[rChildPos]

            # if there are zero or one children:
            if rChildPos > self.size - 1: # if rChild doesn't exist:
                # if lChild doesn't exist: stop (we are done)
                if lChildPos > self.size - 1: return
                
                if lChild.val < currNode.val: # if lChild is smaller than currNode:
                    # O(1) time, see _swap() below
                    self._swap(currNodePos, lChildPos) # swap;
                    return # stop (we are done)
                
                else: return # lChild is bigger than currNode: stop (we are done)
            
            # else if both children are bigger than currNode: stop (we are done)
            elif lChild.val >= currNode.val and rChild.val >= currNode.val: return
            
            # else if lChild is less than or equal to rChild:
            elif lChild.val <= rChild.val:
                # O(1) time, see _swap() below
                self._swap(currNodePos, lChildPos) # swap with lChild;
                currNodePos = lChildPos # set currNode to lChild

            elif rChild.val <= lChild.val: # else if rChild is less than lChild:
                # O(1) time, see _swap() below
                self._swap(currNodePos, rChildPos) # swap with rChild;
                currNodePos = rChildPos # set currNode to rChild

            # this should never happen, all cases are supposed to be covered
            else: assert(False)
    
    # O(1) time, O(1) space
    def _swap( self, index1, index2 ):
        # also rearranges self.tracker[] appropriately

        # this is all O(1) time stuff, since it doesn't at all depend upon n
        itemA = self.items[index1]
        itemB = self.items[index2]

        self.items[index1] = itemB
        self.items[index2] = itemA
        
        trackA = self.tracker[itemA.id]
        trackB = self.tracker[itemB.id]
        self.tracker[itemA.id] = trackB
        self.tracker[itemB.id] = trackA


# We continue to assume that memory allocation requires O(1) time, and so also that all
# operations for this class require O(n) space complexity total, n being the maximum
# number of items.
class ArrayQueue:
    def __init__( self, maxNumNodes ):
        # nodes are named numerically upon insertion
        self.vals = [None] * maxNumNodes
        self.size = 0

    # O(1) time, O(1) space
    def insert( self, index, val ):
        # this only takes O(1) time if vals[] is already initialized to size
        self.vals[index] = val
        self.size += 1
    
    # O(n) time, O(1) space
    def deleteMin( self ):
        # accesses _findMin(), which takes O(n) time
        minIndex = self._findMin()
        self.vals[minIndex] = None
        self.size -= 1
        return minIndex
    
    # O(n) time, O(1) space
    def _findMin( self ):
        currMinIndex = 0
        for i in range(len(self.vals)): # loops n times
            if self.vals[currMinIndex] == None:
                currMinIndex = i + 1
                continue

            if self.vals[i] == None: continue
            
            if self.vals[i] < self.vals[currMinIndex]: currMinIndex = i

        return currMinIndex
        
    # O(1) time, O(1) space
    def decrease( self, nodeID, newVal ):
        # returns true if the value was updated, false otherwise
        if newVal < self.vals[nodeID]:
            self.vals[nodeID] = newVal
            return True
        
        return False