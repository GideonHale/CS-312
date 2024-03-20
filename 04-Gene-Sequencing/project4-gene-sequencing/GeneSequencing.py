#!/usr/bin/python3

from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT6':
	from PyQt6.QtCore import QLineF, QPointF
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import random
from SequenceComparer import *

# Used to compute the bandwidth for banded version
MAXINDELS = 3

# Used to implement Needleman-Wunsch scoring
MATCH = -3
INDEL = 5
SUB = 1

class GeneSequencing:

	def __init__( self ):
		pass

# This is the method called by the GUI.  _seq1_ and _seq2_ are two sequences to be aligned, _banded_ is a boolean that tells
# you whether you should compute a banded alignment or full alignment, and _align_length_ tells you
# how many base pairs to use in computing the alignment

	def align( self, seq1: str, seq2: str, banded: bool, align_length: int):

		seqComp = SequenceComparer(seq1, seq2, align_length, MAXINDELS if banded else float('inf'),
							 	   MATCH, INDEL, SUB)
		
		score = seqComp.getCost()
		alignment1, alignment2 = seqComp.getAlignments()
		# if len(seq1) < 100 and len(seq2) < 100: print(seqComp)
		# print(alignment1)
		# print(alignment2)
		# print("Total Cost:", score)

		return {'align_cost':score, 'seqi_first100':alignment1, 'seqj_first100':alignment2}
