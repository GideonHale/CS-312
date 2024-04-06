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


import time
import numpy as np
from TSPClasses import *
import heapq
import itertools


class TSPSolver:
	def __init__( self, gui_view ):
		self._scenario = None

	def setupWithScenario( self, scenario ):
		self._scenario = scenario


	''' <summary>
		This is the entry point for the default solver
		which just finds a valid random tour.  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of solution,
		time spent to find solution, number of permutations tried during search, the
		solution found, and three null values for fields not used for this
		algorithm</returns>
	'''

	# O(nk) time, O(n) space
	def defaultRandomTour(self, time_allowance = 60.0):
		
		results = {}
		cities = self._scenario.getCities() # this takes up O(n) space
		ncities = len(cities)
		foundTour = False
		count = 0
		bssf = None
		start_time = time.time()
		
		# Assuming a viable tour exists, this loops k times, where k can be anywhere
		# from 1 to n!. It will in practice be much closer to 1 than n!.
		while not foundTour and time.time()-start_time < time_allowance:
			perm = np.random.permutation(ncities) # random permutation cause O(n!) time
			
			route = [] # this ends up being O(n) space, and is reset at each iteration
			# loops n times
			for i in range( ncities ): route.append( cities[ perm[i] ] )
			
			bssf = TSPSolution(route)
			count += 1
			if bssf.cost < np.inf: foundTour = True

		end_time = time.time()

		results['cost'] = bssf.cost if foundTour else math.inf
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None

		return results


	''' <summary>
		This is the entry point for the greedy solver, which you must implement for
		the group project (but it is probably a good idea to just do it for the branch-and
		bound project as a way to get your feet wet).  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number of solutions found, the best
		solution found, and three null values for fields not used for this
		algorithm</returns>
	'''

	# O(n^3) time, O(n) space
	def greedy(self, time_allowance = 60.0):

		results = {}
		cities = self._scenario.getCities() # O(n) space
		ncities = len(cities)
		foundValidTour = False
		count = 0
		bssf = None
		start_time = time.time()

		# Assuming a viable tour exists and we have regular probability, this loops n times maximum
		while not foundValidTour and time.time()-start_time < time_allowance:
			visitedCities = [False for _ in range(ncities)] # O(n) space
			# This random permutation will in practice find a viable starting point in O(n) time.
			currIndex = np.random.randint(ncities)
			startCity = cities[currIndex]
			route = [] # O(n) space

			# loops n times
			for _ in cities:
				currCity = cities[currIndex]
				route.append(currCity)
				visitedCities[currIndex] = True
				nextIndex = None
				# loops n times
				for i in range(ncities):
					if visitedCities[i]: continue
					if nextIndex == None or currCity.costTo(cities[i]) < currCity.costTo(cities[nextIndex]):
						nextIndex = i
				currIndex = nextIndex

			count += 1
			bssf = TSPSolution(route)
			if bssf.cost < np.inf: foundValidTour = True

		end_time = time.time()

		print(f"Greedy Algorithm: {end_time - start_time} sec, {bssf.cost} cost")

		results['cost'] = bssf.cost if foundValidTour else math.inf
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None

		return results


	''' <summary>
		This is the entry point for the branch-and-bound algorithm that you will implement
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number solutions found during search (does
		not include the initial BSSF), the best solution found, and three more ints:
		max queue size, total number of states created, and number of pruned states.</returns>
	'''

	# O(kn^3) time where k is the total number of generated states between n and n! (see while loop)
	# O(pn^2) space where p is the max size of the priority queue
	def branchAndBound(self, time_allowance = 60.0):

		results = {}
		cities = self._scenario.getCities() # this is O(n) space
		ncities = len(cities)
		count = 0
		start_time = time.time()
		bssf = self.greedy(time_allowance)['soln'] # this is O(n^3) time (see above)
		# print("bssf", bssf.cost)

		pq = [] # say this only ever has a max length of p (see also maxPQSize 5 lines later)
		startCity = 0
		state1 = State(cities, startCity) # each State object is O(n^2) space
		heapq.heappush(pq, (None, state1)) # O(log n)

		maxPQSize = 0
		childrenCount = 0
		prunedCount = 0

		# This will loop anywhere from n to n! times, since that is the absolute maximum number of
		# possible states. It will likely be closer to n, though in part due to the time constraint.
		# Let's just say that it loops k times.
		while len(pq) > 0 and time.time() - start_time < time_allowance:

			parent = heapq.heappop(pq)[1] # O(log n)
			if parent.lowerBound > bssf.cost:
				prunedCount += 1
				# print("PRUNED")
				continue

			# loops n times
			for nextDest in range(len(cities)):
				if nextDest in parent.path: continue

				# in creating a state, it is automatically reduced, which takes O(n^2) time
				child = State(parent, nextDest)
				childrenCount += 1

				if child.lowerBound > bssf.cost:
					# print("NOT ADDED")
					continue

				if child.depth() < ncities: heapq.heappush(pq, (None, child)) # O(log n) for push
				elif child.edgeMat[child.lastCity()][child.path[0]] != np.inf:
					# _buildRoute() is O(n) time
					newBSSF = TSPSolution(self._buildRoute(child.path))
					if newBSSF < bssf:
						bssf = newBSSF
						count += 1
				# else: print("INVALID TOUR")
			
			if len(pq) > maxPQSize: maxPQSize = len(pq)

		end_time = time.time()

		results['cost'] = bssf.cost
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = bssf
		results['max'] = maxPQSize
		results['total'] = childrenCount
		results['pruned'] = prunedCount

		return results
	
	# O(n) time
	def _buildRoute(self, path):
		cities = self._scenario.getCities()
		return [cities[cityIndex] for cityIndex in path]


	''' <summary>
		This is the entry point for the algorithm you'll write for your group project.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number of solutions found during search, the
		best solution found.  You may use the other three field however you like.
		algorithm</returns>
	'''

	def fancy( self, time_allowance=60.0 ): pass


class State:
	from collections import namedtuple
	ExemptCities = namedtuple('ExemptCities', ['srcs', 'dests'])
	DEPTH_MULTIPLIER = 1

	# each State object takes O(n^2) time and O(n^2) space to create and maintain
	def __init__(self, param1, param2):
		if type(param1) == list: # the first instance
			cities = param1
			start = param2
			# a matrix of edge costs
			self.edgeMat = [[src.costTo(dest) for dest in cities] for src in cities]
			self.lowerBound = 0
			self.path = [start] # an array of city indices
			self.exemptCities = self.ExemptCities([],[])
		else: # all following instances
			parent = param1
			nextCityIndex = param2
			self.edgeMat = [row.copy() for row in parent.edgeMat]
			self.lowerBound = parent.lowerBound.copy()
			self.path = parent.path.copy()
			self.exemptCities = self.ExemptCities(parent.exemptCities.srcs.copy(),
										 parent.exemptCities.dests.copy())

			self._addToPath(nextCityIndex)

		self._reduce()
	
	def __str__(self):
		output = "(" + str(self.lowerBound) + ")\n"
		output += str(self.edgeMat)
		return output
	
	def __lt__(self, other):
		return self.lowerBound - self.DEPTH_MULTIPLIER * self.depth() < other.lowerBound - self.DEPTH_MULTIPLIER * other.depth()
		# return self.lowerBound < other.lowerBound
	
	# O(n) time
	def _addToPath(self, next):
		last = self.lastCity()
		self.path.append(next)

		# infinitize all rows and columns next (which is actually just an index of the next city)
		self.lowerBound += self.edgeMat[last][next]
		for destIndex in self.edgeMat[last]: destIndex = np.inf
		for srcIndex in self.edgeMat: srcIndex[next] = np.inf

		# mark the last and next as exempt as src and dest, respectively
		self.exemptCities.srcs.append(last)
		self.exemptCities.dests.append(next)

	# O(n^2) time
	def _reduce(self):
		addToLowBnd = 0

		# loops n times
		for src in range(len(self.edgeMat)):
			if src in self.exemptCities.srcs: continue

			shortestEdgeCost = min(self.edgeMat[src]) # O(n) time
			
			if shortestEdgeCost != np.inf:
				# loops n times
				for dest in range(len(self.edgeMat[src])):
					self.edgeMat[src][dest] -= shortestEdgeCost
			
			addToLowBnd += shortestEdgeCost
		
		edgeMatTrans = np.transpose(self.edgeMat) # O(n^2) time
		# loops n times
		for dest in range(len(edgeMatTrans)):
			if dest in self.exemptCities.dests: continue

			shortestEdgeCost = min(edgeMatTrans[dest])

			if shortestEdgeCost != np.inf:
				# loops n times
				for src in range(len(edgeMatTrans[dest])):
					edgeMatTrans[dest][src] -= shortestEdgeCost
			
			addToLowBnd += shortestEdgeCost
		
		self.edgeMat = np.transpose(edgeMatTrans) # O(n^2) time
		
		self.lowerBound += addToLowBnd
	
	def lastCity(self): return self.path[-1]

	def depth(self): return len(self.path)