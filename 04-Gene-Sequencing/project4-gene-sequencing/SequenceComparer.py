from collections import namedtuple

class Entry:
    Location = namedtuple('Location', ['row', 'col'])

    def __init__(self, loc: Location, letter1: str, letter2: str,
                 cost = float('inf'), prev: Location = None):
        self.loc = loc
        self.letter1 = letter1
        self.letter2 = letter2
        self.cost = cost
        self.prev = prev
        self.isMatch = False
        self.prevDirection = None

    def __str__(self):
        # return f"{self.cost}"
        # return f"[{self.letter1},{self.letter2}]"
        # if self.prev != None: return f"{self.cost}, ({self.prev.row},{self.prev.col}), [{self.letter1},{self.letter2}]"
        # else: return f"{self.cost}, (-,-), [{self.letter1},{self.letter2}]"
        if self.prev == None: direction = "*"
        elif self.prevDirection == "left": direction = "←"
        elif self.prevDirection == "up": direction = "↑"
        elif self.prevDirection == "diag": direction = "⇖" if self.isMatch else "↖"
        else: direction = "(" + str(self.prev.row) + "," + str(self.prev.col) + ")"
        return f"{direction} {self.cost:02d}"
        # l1 = " " if self.letter1 == "" else self.letter1
        # l2 = " " if self.letter2 == "" else self.letter2
        # return f"{direction} {self.cost:02d} [{l1},{l2}]"

class SequenceComparer:

    def __init__(self, seq1, seq2, maxAlignLength = float('inf'), maxVariation = float('inf'), MATCH = 0, INDEL = 0, SUB = 0):
        self.seq1 = seq1
        self.seq2 = seq2
        self.didSwitch = False
        if len(self.seq2) > len(self.seq1):
            self.seq1 = seq2
            self.seq2 = seq1
            self.didSwitch = True
        # if len(self.seq1) < 100: print(self.seq1)
        # if len(self.seq2) < 100: print(self.seq2)
        self.maxAlignLength = maxAlignLength
        self.maxVariation = maxVariation
        self.bandwidth = self.maxVariation * 2 + 1
        self.banded = self.bandwidth != float('inf')

        self.MATCH = MATCH
        self.INDEL = INDEL
        self.SUB = SUB

        # banded version should be 7 entries wide for this project
        tableWidth = min(len(self.seq2), self.bandwidth - 1, maxAlignLength)
        tableLength = min(len(self.seq1), maxAlignLength)
        self.dpTable = [[None for _ in range(tableWidth + 1)] for _ in range(tableLength + 1)]
        self._populateTable()
    
    def setUnitCosts(self, match, indel, sub):
        self.MATCH = match
        self.INDEL = indel
        self.SUB = sub

    def __str__(self):
        dpTableString = ""
        for row in self.dpTable:
            row_string = " | ".join(map(str, row))
            dpTableString += "\t\t[" + row_string + "]\n"

        return f"SequenceComparer:\n\tseq1 - {self.seq1} ({len(self.seq1)})\n\tseq2 - {self.seq2} ({len(self.seq2)})\n\tdpTable: \n{dpTableString}"

    @staticmethod
    def commandLineAccess():
        import sys

        seq1 = sys.argv[1]
        seq2 = sys.argv[2]
        maxAlignLength = sys.argv[3]
        maxVariation = sys.argv[4]
        operation = sys.argv[5]
        params = sys.argv[6:]

        if maxAlignLength == "None":
            if maxVariation == "None": obj = SequenceComparer(seq1, seq2)
            else: obj = SequenceComparer(seq1, seq2, float('inf'), int(maxVariation))
        else:
            if maxVariation == "None": obj = SequenceComparer(seq1, seq2, int(maxAlignLength))
            else: obj = SequenceComparer(seq1, seq2, int(maxAlignLength), int(maxVariation))
        obj._performComLineOps(operation, params)
    
    def _performComLineOps(self, operation, params):
        # Implement specific operations to test
        if operation == "findMin":
            if len(params) != 3:
                print("Invalid: wrong number of parameters")
                return
            print("Minimmum:", self._findMin(params[0], params[1], params[2]))
        elif operation == "setEntry":
            if len(params) != 2 and len(params) != 3 and len(params) != 6:
                print("Invalid: wrong number of parameters")
                return
            # self.dpTable[1][0] = Entry(Entry.Location(1,0), "X", "X", 5)
            print("Before:", self)
            loc = Entry.Location(int(params[0]), int(params[1]))
            entry = Entry(loc, self.seq1[loc.row - 1], self.seq2[loc.col - 1])
            if len(params) == 2: self._determineCost(entry)
            elif len(params) == 3: self._determineCost(entry, True, True, True, int(params[2]))
            elif len(params) == 6:
                leftValid = params[3] == "T"
                upValid = params[4] == "T"
                diagValid = params[5] == "T"
                self._determineCost(entry, leftValid, upValid, diagValid, int(params[2]))
            print("After:", self)
        elif operation == "setEntryInitial":
            if len(params) != 0:
                print("Invalid: wrong number of parameters")
                return
            print("Before:", self)
            self._fillOneCell(0, 0)
            print("After:", self)
        elif operation == "setRow1":
            if len(params) != 0:
                print("Invalid: wrong number of parameters")
                return
            print("Before:", self)
            for col in range(len(self.dpTable[0])):
                self._fillOneCell(0, col)
            print("After:", self)
        elif operation == "setAllRows":
            if len(params) != 0:
                print("Invalid: wrong number of parameters")
                return
            print("Before:", self)
            self._populateTable()
            print("After:", self)
        elif operation == "results":
            if len(params) != 0:
                print("Invalid: wrong number of parameters")
                return
            print(self)
            al1, al2 = self.getAlignments()
            print(al1)
            print(al2)
            print("Total Cost:", self.getCost())
        elif operation == "str":
            if len(params) != 0:
                print("Invalid: wrong number of parameters")
                return
            print(self)
        else: print("Invalid operation")

    def _populateTable(self):
        
        for row in range(len(self.dpTable)):
            if row > self.maxAlignLength: return

            for col in range(len(self.dpTable[row])): # assume bandwidth is always smaller than maxAlignLength
                if col > self.maxAlignLength: break
                self._fillOneCell(row, col)

    def _fillOneCell(self, row, col):
        if row == 0:
            if col == 0:
                self.dpTable[col][row] = Entry(Entry.Location(row, col), "", "", 0)
                return
            else: currEntry = Entry(Entry.Location(row, col), "", self.seq2[col - 1])
        else:
            if col == 0: currEntry = Entry(Entry.Location(row, col), self.seq1[row - 1], "")
            else: currEntry = Entry(Entry.Location(row, col), self.seq1[row - 1], self.seq2[col - 1])

        if not self.banded: # the default option
            if row == 0:
                if col == 0: raise IndexError("This should already have been covered")
                else: self._determineCost(currEntry, True, False, False)
            else:
                if col == 0: self._determineCost(currEntry, False, True, False)
                else: self._determineCost(currEntry)

        else: # if it's banded
            if row == 0: # first row
                if col == 0: raise IndexError("This should already have been covered")
                elif col > self.maxVariation: return # end of column
                else: self._determineCost(currEntry, True, False, False)

            elif row <= self.maxVariation: # initial wedge for banded
                if col == 0: self._determineCost(currEntry, False, True, False)
                elif col == self.maxVariation + row: self._determineCost(currEntry, True, False, True)
                elif col > self.maxVariation + row: return # cell doesn't exist
                else: self._determineCost(currEntry, True, True, True)

            elif row > len(self.seq2) - self.maxVariation:
                currEntry.letter2 = self.seq2[len(self.seq2) - self.bandwidth + col]

                stop = row - len(self.seq2) + self.maxVariation

                if col < stop: return
                elif col == stop: self._determineCost(currEntry, False, True, True)
                else: self._determineCost(currEntry, True, True, True)

            else: # row is greater than self.maxVariation and less than self.maxAlignLength
                currEntry.letter2 = self.seq2[row + col - self.maxVariation - 1]

                if col == 0: self._determineCost(currEntry, False, True, True, 1)
                elif col == self.bandwidth - 1: self._determineCost(currEntry, True, False, True, 1)
                elif col >= self.bandwidth: return # cell doesn't exist
                else: self._determineCost(currEntry, True, True, True, 1)
        
        self.dpTable[row][col] = currEntry

    def _determineCost(self, entry: Entry, leftValid = True, upValid = True, diagValid = True, shift = 0): # does direction logic

        self.dpTable[entry.loc.row][entry.loc.col] = entry

        if leftValid: insCost = self.INDEL + self.dpTable[entry.loc.row][entry.loc.col - 1].cost # moving right -> seq1 gets a hyphen, seq2 gets its letter
        else: insCost = float('inf')

        if upValid: delCost = self.INDEL + self.dpTable[entry.loc.row - 1][entry.loc.col + shift].cost # moving down -> seq1 gets its letter, seq2 gets a hyphen
        else: delCost = float('inf')
        
        if diagValid:
            matCost = self.MATCH + self.dpTable[entry.loc.row - 1][entry.loc.col - 1 + shift].cost
            subCost = self.SUB + self.dpTable[entry.loc.row - 1][entry.loc.col - 1 + shift].cost
        else:
            matCost = float('inf')
            subCost = float('inf')

        if entry.letter1 == entry.letter2:
            entry.isMatch = True
        
        move = self._findMin(insCost, delCost, matCost if entry.isMatch else subCost) # tie priority -> insert, delete, match / substitute

        match move:
            case "left": # insert
                entry.cost = insCost
                entry.prev = Entry.Location(entry.loc.row, entry.loc.col - 1)
                entry.prevDirection = "left"
            case "up": # delete
                entry.cost = delCost
                entry.prev = Entry.Location(entry.loc.row - 1, entry.loc.col + shift)
                entry.prevDirection = "up"
            case "diag": # match / substitute
                entry.cost = matCost if entry.isMatch else subCost
                entry.prev = Entry.Location(entry.loc.row - 1, entry.loc.col - 1 + shift)
                entry.prevDirection = "diag"

    def _findMin(self, left, up, diag): # finds the cheapest option
        if left == up == diag: return "left"
        elif left <= up and left <= diag: return "left"
        elif up <= diag: return "up"
        else: return "diag"

    def getCost(self):
        targetEntry = self.dpTable[-1][-1]
        if targetEntry == None: return float('inf')
        else: return targetEntry.cost
    
    def getAlignments(self):
        if self.dpTable[-1][-1] == None: return "No Alignment Possible.", "No Alignment Possible."
        
        path = self._reconstructPath()
        al1, al2 = self._figureAlignments(path)
        if self.didSwitch: return al2, al1
        else: return al1, al2

    def _reconstructPath(self):
        stack = []

        row = len(self.dpTable) - 1
        col = len(self.dpTable[0]) - 1
        while row != 0 and col != 0:
            currEntry = self.dpTable[row][col]
            stack.append(currEntry)
            row = currEntry.prev.row
            col = currEntry.prev.col
        stack.append(self.dpTable[0][0])

        stack.reverse()
        return stack
    
    def _figureAlignments(self, path):
        alignment1 = ""
        alignment2 = ""
        count = 0
        for entry in path: # this is supposed to start at the beginning, [0][0]
            count += 1
            if count > 100: break

            if entry.prev == None: continue # this represents the empty string, so we're good.
            elif entry.prevDirection == "left":
                alignment1 += "-"
                alignment2 += entry.letter2
            elif entry.prevDirection == "up":
                alignment1 += entry.letter1
                alignment2 += "-"
            elif entry.prevDirection == "diag":
                alignment1 += entry.letter1
                alignment2 += entry.letter2
            else: return "nogood"
        return alignment1, alignment2

# for testing purposes
if __name__ == "__main__":
    SequenceComparer.commandLineAccess()