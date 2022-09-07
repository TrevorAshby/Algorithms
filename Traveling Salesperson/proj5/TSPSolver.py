#!/usr/bin/python3
import copy
from queue import PriorityQueue

from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))


LVL_MULTIPLY = 190

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
	
	def defaultRandomTour( self, time_allowance=60.0 ):
		results = {}
		cities = self._scenario.getCities()
		ncities = len(cities)
		foundTour = False
		count = 0
		bssf = None
		start_time = time.time()
		while not foundTour and time.time()-start_time < time_allowance:
			# create a random permutation
			perm = np.random.permutation( ncities )
			route = []
			# Now build the route using the random permutation
			for i in range( ncities ):
				route.append( cities[ perm[i] ] )
			bssf = TSPSolution(route)
			count += 1
			if bssf.cost < np.inf:
				# Found a valid route
				foundTour = True
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

	#########################
	# Time Complexity O(n^3)
	# Space Complexity O(n^2)
	#########################
	# MY GREEDY
	"""def greedy( self,time_allowance=60.0 ):
		# initialize results, cities, ncities, and other variables
		results = {}
		cities = self._scenario.getCities()
		count = 0

		start_time = time.time()
		lowest_bssf = None
		lowest_bssf_cost = math.inf
		bssf = None
		foundTour = False

		# run a loop that will go through each city as the starting point
		for pos in range(len(cities)):
			startingCity = cities[pos]
			edges = startingCity._scenario._edge_exists
			curCity = startingCity
			route = []
			routeNames = []
			route.append(startingCity)
			routeNames.append(startingCity._name)
			for i in range(len(cities)):
				minLength = math.inf
				minName = "blank"
				minIndex = .5
				for edge_pos in range(len(cities)):
					dist = curCity.costTo(cities[edge_pos])
					if dist < minLength and cities[edge_pos]._name not in routeNames:
						minLength = dist
						minName = cities[edge_pos]._name
						minIndex = cities[edge_pos]._index
				if minName != "blank":
					routeNames.append(cities[minIndex]._name)
					route.append(cities[minIndex])
					curCity = cities[minIndex]
			bssf = TSPSolution(route)
			count += 1

			if bssf.cost < lowest_bssf_cost:
				lowest_bssf = bssf
				lowest_bssf_cost = lowest_bssf.cost
		if lowest_bssf.cost < np.inf:
			# Found a valid route
			foundTour = True
		end_time = time.time()
		results['cost'] = lowest_bssf.cost if foundTour else math.inf
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = lowest_bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None
		return results"""

	def greedy(self, time_allowance=60.0, startIndex=0):
		results = {}
		cities = self._scenario.getCities()
		ncities = len(cities)
		startingCity = cities[startIndex]  # Start at city index defined in function parameters (default 0)
		foundTour = False
		count = 0
		bssf = None
		start_time = time.time()
		curCity = startingCity
		route = []
		routeNames = []
		route.append(startingCity)
		routeNames.append(startingCity._name)
		failed = False
		while not foundTour and not failed and time.time() - start_time < time_allowance:
			if len(route) == ncities:
				break
			for i in range(
					ncities - 1):  # Loop through all of the cities once. This loop should add a city to route each time.
				minLength = math.inf
				minName = "blank"
				minIndex = .5
				for j in range(
						ncities):  # Loop through all of the cities from the perspective of curCity. This will be used to find min
					dist = curCity.costTo(cities[j])
					if dist < minLength and cities[
						j]._name not in routeNames:  # Find shortest remaining path from curCity.
						minLength = dist
						minName = cities[j]._name
						minIndex = cities[j]._index
				if minName != "blank":
					routeNames.append(cities[minIndex]._name)
					route.append(cities[minIndex])
					curCity = cities[minIndex]
					if len(route) == ncities:
						foundTour = True
						break
				else:
					# It failed
					# print("IT FAILED")
					failed = True
					break
		bssf = TSPSolution(route)  # Update BSSF with route found above
		if failed:
			bssf.cost = math.inf
		if bssf.cost < np.inf:
			foundTour = True
		end_time = time.time()
		# Return results
		results['cost'] = bssf.cost if foundTour else math.inf
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None
		return results

	# TIME: 2N^2
	# SPACE: N^2
	def reduce(self, mat, rows, cols):  # Takes a matrix and the visited rows and Cols as parameters,
		# returns the reduced matrix [0] and the cost to reduce [1]
		cost = 0
		# LOOP THROUGH ROWS
		for i in range(len(mat[0])):
			min = math.inf
			if i not in rows:
				# LOOP THROUGH COLS
				for j in range(len(mat[0])):
					if j not in cols:
						if mat[i][j] == 0:  # This means the row already has a 0 in it
							min = 0
							break
						elif mat[i][j] < min:
							min = mat[i][j]
				if min == math.inf:  # This means a row didn't get reduced (there were only infinites in the row.)
					return (mat,
							math.inf)  # When ever you get a return from the reduce function make sure that you check to see if [1] == inf, if it is you won't even want to look at the mat
				if min != 0:
					# HERE LOOP THROUGH THE COLS AGAIN AND SUBTRACT MIN FROM EACH VAL
					for j in range(len(mat[0])):
						if j not in cols:
							mat[i][j] = mat[i][j] - min
				cost = cost + min
		# LOOP THROUGH COLS
		for i in range(len(mat[0])):
			min = math.inf
			if i not in cols:
				# LOOP THROUGH ROWS
				for j in range(len(mat[0])):
					if j not in rows:
						if mat[j][i] == 0:  # This means the row already has a 0 in it
							min = 0
							break
						elif mat[j][i] < min:
							min = mat[j][i]
				if min == math.inf:  # This means a row didn't get reduced (there were only infinites in the row.)
					return (mat, math.inf)
				if min != 0:
					# HERE LOOP THROUGH THE ROWS AGAIN AND SUBTRACT MIN FROM EACH VAL
					for j in range(len(mat[0])):
						if j not in rows:
							mat[j][i] = mat[j][i] - min
				cost = cost + min
		return (mat, cost)

	#########################
	# Time Complexity O(n^2)
	# Space Complexity O(n^2)
	#########################
	# MY REDUCE
	"""def reduce(self, costMatrix, numCities, lowerBound):
		# create initial reduced cost matrix & initial lower bound
		# make sure that every row has a 0
		for row in range(numCities):
			# go through each column and find lowest value or 0
			hasZero = False
			lowestVal = math.inf
			for col in range(numCities):
				if lowestVal > costMatrix[row][col]:
					lowestVal = costMatrix[row][col]
				if costMatrix[row][col] == 0:
					hasZero = True
			if hasZero:
				continue
			else:
				if lowestVal != math.inf:
					lowerBound += lowestVal
					for col in range(numCities):
						costMatrix[row][col] -= lowestVal

		# make sure that every col has a 0
		for col in range(numCities):
			hasZero = False
			lowestVal = math.inf
			for row in range(numCities):
				if lowestVal > costMatrix[row][col]:
					lowestVal = costMatrix[row][col]
				if costMatrix[row][col] == 0:
					hasZero = True
			if hasZero:
				continue
			else:
				if lowestVal != math.inf:
					lowerBound += lowestVal
					for row in range(numCities):
						costMatrix[row][col] -= lowestVal

		return costMatrix, lowerBound
	"""


	def infiniteRowsAndColumns(self, inputMatrix, rowIn, colIn):
		returnMatrix = inputMatrix.copy()
		for row in range(len(returnMatrix)):
			for col in range(len(returnMatrix)):
				if col == colIn or row == rowIn:
					returnMatrix[row][col] = math.inf
		return returnMatrix

	def branchAndBound( self, time_allowance=60.0 ):
		results = {}
		cities = self._scenario.getCities()
		ncities = len(cities)
		foundTour = False
		count = 0
		solutionCount = 0
		trimCount = 0
		curSolution = []
		bssf = math.inf	#USE THE GREEDY TO GET A bssf THAT'S BETTER THAN INF
		priorityQ = PriorityQueue()
		start_time = time.time()
		# ************************ ************************
		#						GET BSSF
		# ************************ ************************
		#TIME: n^3
		for i in range(ncities):	#Loop through every possible starting city, to get the best BSSF w/ greedy
			failure = False
			startingCity = cities[i]
			route = []
			routeNames = []
			route.append(startingCity)
			routeNames.append(startingCity._name)
			failed = False
			greedyCurCity = startingCity
			if len(route) == ncities:
				break
			for i in range(ncities - 1):  # Loop through all of the cities once this loop should add a city to route each time.
				minLength = math.inf
				minName = "blank"
				minIndex = .5
				for j in range(
						ncities):  # Loop through all of the cities from the perspective of curCity. This will be used to find min
					dist = greedyCurCity.costTo(cities[j])
					if dist < minLength and cities[j]._name not in routeNames:
						minLength = dist
						minName = cities[j]._name
						minIndex = cities[j]._index
				if minName != "blank":
					routeNames.append(cities[minIndex]._name)
					route.append(cities[minIndex])
					greedyCurCity = cities[minIndex]
					if len(route) == ncities:
						foundTour = True
						break
				else:
					# It failed
					print("IT FAILED")
					failure = True
					break
			if not failure:
				greedyBSSF = TSPSolution(route).cost
			else:
				greedyBSSF = math.inf
			if greedyBSSF < bssf:
				bssf = greedyBSSF
		# ************************ ************************
		#				MAKE THE INITIAL MATRIX
		# ************************ ************************
		initMat = [[0 for i in range(ncities)] for j in range(ncities)]
		#************************ ************************
		#				INITIALIZE MATRIX
		#************************ ************************
		for i in range(ncities):
			for j in range(ncities):
				initMat[i][j] = cities[i].costTo(cities[j])
		# ************************ ************************
		#		REDUCE THE MATRIX AND GET LOWER BOUND
		# ************************ ************************
		reducedMat = copy.deepcopy(initMat)
		reducedReturn = self.reduce(reducedMat, [], [])	#REDUCE is always N^2 (call with empty [][] rows and cols cause none have been visited
		reducedMat = reducedReturn[0]
		initialLowerBound = reducedReturn[1]
		# ************************ ************************
		# GET THE REDUCED MATRIX FOR EACH IN THE FIRST ROW
		# ************************ ************************
		# ORDER FOR GETTING THINGS FROM NODE
		# [0] SCORE
		# [1] LVL
		# [2] LOWERBOUND
		# [3] MAT
		# [4] ROWS
		# [5] COLS
		for i in range(ncities):
			if i != 0:	#That would add infinity to the score
				addedCost = reducedMat[0][i]
				if addedCost + initialLowerBound > bssf:
					trimCount+=1
					continue
				removedRow = 0
				removedCol = i
				curMat = copy.deepcopy(reducedMat)
				curMat[i][0] = math.inf
				count += 1
				reducedReturn = self.reduce(curMat, [removedRow], [removedCol])
				curMat = reducedReturn[0]
				lowerBound = reducedReturn[1] + addedCost + initialLowerBound
				level = 0
				score = lowerBound - (level * LVL_MULTIPLY)
				if lowerBound < bssf:
					node = [score, level, lowerBound, curMat, [removedRow], [removedCol]]
					priorityQ.put(node)
					#count+=1
				else:
					trimCount+=1
		maxQueueSize = 0
		while len(priorityQ.queue) != 0 and time.time() - start_time < time_allowance:
			# ************************ ************************
			# 		HELPS TO FIND THE MAX QUEUE SIZE
			# ************************ ************************
			qSize = len(priorityQ.queue)
			if qSize > maxQueueSize:
				maxQueueSize = qSize
			curNode = priorityQ.get()
			curLvl = curNode[1]
			curLowerBound = curNode[2]
			curMat = curNode[3]
			curRows = curNode[4]
			curCols = curNode[5]
			# ************************ ************************
			# 	IF YOU'VE COME TO THE END OF A BRANCH
			# ************************ ************************
			# IF IT'S A SOLUTION YEET!
			# Run through the pQueue, any
			# if node.lowerBound < bssf keep it else, remove from queue
			if curLvl == ncities - 2:
				addedCost = math.inf
				if curCols[-1] not in curRows and 0 not in curCols:
					addedCost = curMat[curCols[-1]][0] 					#This is the cost to get from the last node back to node 0
					foundSolution = curLowerBound + addedCost
					if foundSolution < bssf:
						print("YEET!")
						bssf = foundSolution
						solutionCount+=1
						curSolution = curCols		#The columns are the order of each city you visit.
						#LOOP THROUGH PQUEUE IF SOMETHING IS GREATER THAN BSSF DON'T PUT IT ON THE NEW PQ
						newPQ = PriorityQueue()
						while len(priorityQ.queue) != 0:	#The time of this while loop varies worse case is N!
							checkNode = priorityQ.get()
							if checkNode[2] < bssf:
								newPQ.put(checkNode)
							else:
								trimCount+=1
						priorityQ = newPQ
				else:
					trimCount+=1
				continue
			# ************************ ************************
			# 	LOOP THROUGH ALL OF THE CHILDREN OF A BRANCH
			# ************************ ************************
			for i in range(ncities):	#This loop will go N times
				if i not in curCols:
					addedCost = curMat[curCols[-1]][i]
					removedRow = curCols[-1]
					removedCol = i
					if addedCost + curLowerBound > bssf:	#Check to see if the added cost already puts it over
						trimCount+=1						#This way you don't need to call reduce()
						continue
					newMat = copy.deepcopy(curMat)		#Space: N^2
					newMat[i][curCols[-1]] = math.inf
					reducedReturn = self.reduce(newMat, curRows, curCols)
					count += 1
					newMat = reducedReturn[0]
					lowerBound = reducedReturn[1] + addedCost + curLowerBound
					level = curLvl + 1
					score = lowerBound - (level * LVL_MULTIPLY)
					if lowerBound < bssf:
						newRows = copy.deepcopy(curRows)
						newCols = copy.deepcopy(curCols)
						newRows.append(removedRow)
						newCols.append(removedCol)
						node = [score, level, lowerBound, newMat, newRows, newCols]
						priorityQ.put(node)
					else:
						trimCount+=1
		route = []
		route.append(cities[0])
		for i in range(len(curSolution)):	#Runs N times
			route.append(cities[curSolution[i]])
		end_time = time.time()
		results['cost'] = bssf if foundTour else math.inf
		results['time'] = end_time - start_time
		results['count'] = solutionCount
		results['soln'] = TSPSolution(route)
		results['max'] = maxQueueSize
		results['total'] = count
		results['pruned'] = trimCount
		return results
		pass


	''' <summary>
		This is the entry point for the branch-and-bound algorithm that you will implement
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number solutions found during search (does
		not include the initial BSSF), the best solution found, and three more ints: 
		max queue size, total number of states created, and number of pruned states.</returns> 
	'''
	# MY BRANCH AND BOUND
	"""def branchAndBound( self, time_allowance=60.0 ):
		LVL_OFFSET = 450
		# get the first greedy bssf that can be used for initial trimming
		greedyResult = self.greedy()
		#########################
		# Time Complexity O(n^3)
		# Space Complexity O(n^2)
		#########################
		bssf = greedyResult['soln']

		# initialize results, cities, ncities, and other variables
		results = {}
		cities = self._scenario.getCities()
		numCities = len(cities)
		count = 0
		start_time = time.time()

		# generate unreduced cost matrix
		costMatrix = np.full((numCities,numCities), np.inf)
		# loop through each row filling in matrix
		for row in range(numCities):
			#########################
			# Time Complexity O(n^2)
			# Space Complexity O(n^2)
			#########################
			# loop through each column for every row filling in cost
			for col in range(numCities):
				costMatrix[row][col] = cities[row].costTo(cities[col])

		# create initial reduced cost matrix & initial lower bound
		totalStates = 0
		numTrimmed = 0
		lowerBound = 0
		foundTour = False
		#########################
		# Time Complexity O(n^2)
		# Space Complexity O(n^2)
		#########################
		costMatrix, lowerBound = self.reduce(costMatrix, numCities, lowerBound)

		# create priority queue
		priorityQueue = []
		route = []
		routeNames = []

		# GLOBAL CONST LVL_OFFSET 190
		# score - (lvl * lvl_offset)

		route.append(cities[0])
		routeNames.append(cities[0]._name)
		priorityQueue.append((costMatrix, route, routeNames, lowerBound, 0, 1, lowerBound - (1 * LVL_OFFSET)))
		queueMaxSize = len(priorityQueue)
		# push 'A' onto the Queue, and calculate from there
		# calculate potential paths, start evaluating paths
		#########################
		# Time Complexity O(n^2 * b^n)
		# Space Complexity O(n^2 * b^n)
		# Worst Case Scenario O(n^2 n!)
		#########################
		while priorityQueue and time.time() - start_time < time_allowance:
			if len(priorityQueue) > queueMaxSize:
				queueMaxSize = len(priorityQueue)

			priorityQueue.sort(key=lambda tup: tup[6], reverse=True)
			currentDecision = priorityQueue.pop()
			if len(currentDecision[1]) == numCities and currentDecision[3] < bssf.cost:
				count += 1
				bssf = TSPSolution(currentDecision[1])
				foundTour = True
			else:
				for col in range(numCities):
					totalStates += 1
					tempMatrix = currentDecision[0].copy()
					tempScore = currentDecision[3]
					tempRoute = currentDecision[1].copy()
					tempRouteNames = currentDecision[2].copy()
					tempMatrix[col][currentDecision[4]] = math.inf
					tempScore += tempMatrix[currentDecision[4]][col]
					if tempScore > bssf.cost:
						numTrimmed += 1
						continue
					else:
						if cities[col]._name not in tempRouteNames:
							tempRoute.append(cities[col])
							tempRouteNames.append(cities[col]._name)
						tempMatrix = self.infiniteRowsAndColumns(tempMatrix, currentDecision[4], col)
						tempMatrix, tempScore = self.reduce(tempMatrix, numCities, tempScore)
						if tempScore > bssf.cost:
							numTrimmed += 1
							continue
						else:
							priorityQueue.append((tempMatrix, tempRoute, tempRouteNames, tempScore, col, currentDecision[5] + 1, tempScore - ((currentDecision[5] + 1) * LVL_OFFSET))) # TAKE INTO CONSIDERATION DEEPNESS
		if bssf.cost < np.inf:
			# Found a valid route
			foundTour = True
		end_time = time.time()
		results['cost'] = bssf.cost if foundTour else math.inf
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = bssf
		results['max'] = queueMaxSize
		results['total'] = totalStates
		results['pruned'] = numTrimmed + len(priorityQueue)
		return results
		# pass
	"""


	''' <summary>
		This is the entry point for the algorithm you'll write for your group project.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number of solutions found during search, the 
		best solution found.  You may use the other three field however you like.
		algorithm</returns> 
	'''

	def fancy(self, time_allowance=60.0):
		results = {}
		cities = self._scenario.getCities()
		ncities = len(cities)
		curSolution = []
		bssf = math.inf  # USE THE GREEDY TO GET A bssf THAT'S BETTER THAN INF
		start_time = time.time()
		# ************************ ************************
		#                 GET BSSF
		# ************************ ************************
		# TIME: n^3
		# SPACE: n
		for i in range(ncities):  # Loop through every possible starting city, to get the best BSSF w/ greedy
			failure = False
			startingCity = cities[i]
			route = []
			routeNames = []
			route.append(startingCity)
			routeNames.append(startingCity._name)
			failed = False
			greedyCurCity = startingCity
			if len(route) == ncities:
				break
			for i in range(
					ncities - 1):  # Loop through all of the cities once this loop should add a city to route each time.
				minLength = math.inf
				minName = "blank"
				minIndex = .5
				for j in range(
						ncities):  # Loop through all of the cities from the perspective of curCity. This will be used to find min
					dist = greedyCurCity.costTo(cities[j])
					if dist < minLength and cities[j]._name not in routeNames:
						minLength = dist
						minName = cities[j]._name
						minIndex = cities[j]._index
				if minName != "blank":
					routeNames.append(cities[minIndex]._name)
					route.append(cities[minIndex])
					greedyCurCity = cities[minIndex]
					if len(route) == ncities:
						foundTour = True
						break
				else:
					# It failed
					print("IT FAILED")
					failure = True
					break
			if not failure:
				greedyBSSF = TSPSolution(route).cost
			else:
				greedyBSSF = math.inf
			if greedyBSSF < bssf:
				bssf = greedyBSSF
				curSolution = route

		# ************************ ************************
		#              RUN GREEDY 2-OPT
		# ************************ ************************

		# Run it once using the bssf from greedy to find one minima
		firstSwapSolution = self.runSwaps(curSolution, cities, ncities, bssf)

		# Save those results
		bestSolution = firstSwapSolution[1]
		bestBSSF = firstSwapSolution[0]

		# ************************ ************************
		#           RUN SIMULATED ANNEALING
		# ************************ ************************

		# TIME: N^5 logN
		# SPCAE: N^2

		# If the number of cities is small enough run the simulated annealing
		if ncities <= 25:
			numSwaps = 0
			curSolution = bestSolution
			curBssf = bestBSSF
			breakFirstLoop = False
			for i in range(ncities):
				if breakFirstLoop:
					break
				for j in range(ncities):
					if i + 1 < j:
						newRoute = self.optSwap(curSolution, i, j)
						newCost = TSPSolution(newRoute).cost
						if newCost > bestBSSF and newRoute != math.inf:  # Try to increase the route length, while keeping a legal route
							numSwaps += 1
							curSolution = newRoute
							curBssf = newCost
						if numSwaps > 2:  # Only check after a few swaps have happened,
							# otherwise it will imediately fix the swap and won't escape the minimum
							newSwapSol = self.runSwaps(curSolution, cities, ncities, curBssf)
							if newSwapSol[0] < bestBSSF:  # Only look at one improvment.
								bestBSSF = newSwapSol[0]
								bestSolution = newSwapSol[1]
								breakFirstLoop = True
								break

		print("DONE")
		end_time = time.time()
		results['cost'] = bestBSSF
		results['time'] = end_time - start_time
		results['count'] = 0
		results['soln'] = TSPSolution(bestSolution)
		results['max'] = 0
		results['total'] = 0
		results['pruned'] = 0
		return results

	# TIME: N
	# SPACE: N
	def optSwap(self, inpRoute, index1, index2):
		lyst1 = []
		lyst2 = []
		lyst3 = []
		for i in range(len(inpRoute)):
			if i < index1:
				lyst1.append(inpRoute[i])
			if i >= index1 and i <= index2:  # Reverse the in
				lyst2.insert(0, inpRoute[i])
			if i > index2:
				lyst3.append(inpRoute[i])

		return lyst1 + lyst2 + lyst3


	# TIME: N^3 logN
	# SPCAE: N^2
	def runSwaps(self, curSolution, cities, ncities, bssf):  # A greedy impimentation of the two opt

		pq = []
		for i in range(len(curSolution) - 1):
			pq.append((cities[i].costTo(cities[i + 1]), i, i + 1))
		pq.sort(key=lambda tup: tup[0], reverse=True)
		change = True
		whileCounter = 0
		while change:  # Theoretically, this could run n! times
			whileCounter += 1  # However, in our testing it looks more like logn times, then it hits a local minimum
			change = False
			bestChange = 0
			bestChangeRoute = []
			for i in range(ncities):  # These two loops run n^2 times
				for j in range(ncities):
					if i + 1 < j:
						copyRoute = copy.deepcopy(curSolution)
						new_route = self.optSwap(copyRoute, i, j)
						newCost = TSPSolution(new_route).cost
						if (len(pq) > 0):
							currentTempCity = pq.pop()
							new_route2 = self.optSwap(copyRoute, currentTempCity[1], currentTempCity[2])
							newCost2 = TSPSolution(new_route2).cost
						if (newCost2 < newCost):
							newCost = newCost2
							new_route = copy.deepcopy(new_route2)
						if (bssf - newCost) > bestChange:
							bestChange = bssf - newCost
							bestChangeRoute = copy.deepcopy(new_route)
			if (bestChange > 0):
				change = True
				bssf = bssf - bestChange
				curSolution = bestChangeRoute
		print(whileCounter)
		return bssf, curSolution



