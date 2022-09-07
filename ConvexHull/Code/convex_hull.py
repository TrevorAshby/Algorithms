from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF, QObject
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))



import time
import math

# Some global color constants that might be useful
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# Global variable that controls the speed of the recursion automation, in seconds
#
PAUSE = 0.25

#
# This is the class you have to complete.
#

######################
# Time Complexity O(1)
# Space Complexity O(1)
######################
def findSlope(leftMostPoint, point):
	rise = point.y() - leftMostPoint.y()
	run = point.x() - leftMostPoint.x()
	slope = rise / run
	return slope



class ConvexHullSolver(QObject):

# Class constructor
	def __init__( self):
		super().__init__()
		self.pause = False
		
# Some helper methods that make calls to the GUI, allowing us to send updates
# to be displayed.

	def showTangent(self, line, color):
		self.view.addLines(line,color)
		if self.pause:
			time.sleep(PAUSE)

	def eraseTangent(self, line):
		self.view.clearLines(line)

	def blinkTangent(self,line,color):
		self.showTangent(line,color)
		self.eraseTangent(line)

	def showHull(self, polygon, color):
		self.view.addLines(polygon,color)
		if self.pause:
			time.sleep(PAUSE)
		
	def eraseHull(self,polygon):
		self.view.clearLines(polygon)
		
	def showText(self,text):
		self.view.displayStatusText(text)


	################################
	# Time Complexity O(nlogn)
	# Space Complexity O(nlogn)
	################################
	def solver(self, points):
		# do recursion until only 3 or less points are left
		if len(points) == 3:
			rightmostPoint = points[len(points)-1]
			#########################
			# Time Complexity O(n)
			# Space Complexity O(n)
			#########################
			sortedPoints = [points[0]] + sorted(points[1:], reverse=True, key=lambda p: findSlope(points[0], p))
			return sortedPoints, rightmostPoint
		elif len(points) == 2:
			rightmostPoint = points[len(points) - 1]
			return points, rightmostPoint

		# split points into two halves, left and right
		########################
		# Time Complexity O(n)
		# Space Complexity O(n)
		########################
		left = [left for left in points[0:math.floor(len(points)/2)]]
		right = [right for right in points[math.floor(len(points)/2):len(points)]]

		# recursively run both halves
		left_half, rightmostPoint_left = self.solver(left)
		right_half, rightmostPoint_right = self.solver(right)

		#########################
		# Time Complexity O(n)
		# Space Complexity O(n)
		#########################
		if (len(left_half) <= 3):
			left_half = [left_half[0]] + sorted(left_half[1:], reverse=True, key=lambda p: findSlope(left_half[0], p))

		if (len(right_half) <= 3):
			right_half = [right_half[0]] + sorted(right_half[1:], reverse=True, key=lambda p: findSlope(right_half[0], p))


		# set the left/right most points
		leftMost_left = left_half[0]
		leftMost_right = right_half[0]

		# begin merging the Hulls
		# top
		slope = findSlope(rightmostPoint_left, leftMost_right)
		topLine_right = leftMost_right
		topLine_left = rightmostPoint_left

		leftPos = left_half.index(rightmostPoint_left)
		rightPos = right_half.index(leftMost_right)
		numChanges = 3
		########################
		# Time Complexity O(n)
		# Space Complexity O(n)
		########################
		while(numChanges > 0):
			leftChange = True
			while(leftChange):
				if (findSlope(topLine_left, topLine_right) > findSlope(left_half[leftPos - 1], topLine_right)):
					topLine_left = left_half[leftPos - 1]
					leftPos -= 1
					numChanges += 1
				else:
					leftChange = False
					numChanges -= 1

			rightChange = True
			while(rightChange):
				if (findSlope(topLine_left, topLine_right) < findSlope(topLine_left, right_half[(rightPos + 1) % len(right_half)])):
					topLine_right = right_half[(rightPos + 1) % len(right_half)]
					rightPos += 1
					numChanges += 1
				else:
					rightChange = False
					numChanges -= 1

		# bot
		leftPos = left_half.index(rightmostPoint_left)
		rightPos = right_half.index(leftMost_right)
		botLine_right = leftMost_right
		botLine_left = rightmostPoint_left
		numChanges = 3
		########################
		# Time Complexity O(n)
		# Space Complexity O(n)
		########################
		while(numChanges > 0):
			leftChange = True
			while(leftChange):
				if (findSlope(botLine_left, botLine_right) < findSlope(left_half[(leftPos + 1) % len(left_half)], botLine_right)):
					botLine_left = left_half[(leftPos + 1) % len(left_half)]
					leftPos += 1
					numChanges += 1
				else:
					leftChange = False
					numChanges -= 1

			rightChange = True
			while(rightChange):
				if (findSlope(botLine_left, botLine_right) > findSlope(botLine_left, right_half[rightPos - 1])):
					botLine_right = right_half[rightPos - 1]
					rightPos -= 1
					numChanges += 1
				else:
					rightChange = False
					numChanges -= 1

		points_to_return = []
		########################
		# Time Complexity O(n)
		# Space Complexity O(n)
		########################
		for i in range(len(left_half)):
			if (left_half[i % len(left_half)] == topLine_left):
				points_to_return.append(left_half[i % len(left_half)])
				break
			else:
				points_to_return.append(left_half[i % len(left_half)])
		########################
		# Time Complexity O(n)
		# Space Complexity O(n)
		########################
		for i in range(len(right_half)):
			j = i + right_half.index(topLine_right)
			if (right_half[j % len(right_half)] == botLine_right):
				points_to_return.append(right_half[j % len(right_half)])
				break
			else:
				points_to_return.append(right_half[j % len(right_half)])
		########################
		# Time Complexity O(n)
		# Space Complexity O(n)
		########################
		for i in range(len(left_half)):
			j = i + left_half.index(botLine_left)
			if (j > len(left_half)):
				break
			if (left_half[j % len(left_half)] == left_half[0]):
				break
			else:
				points_to_return.append(left_half[j % len(left_half)])

		return points_to_return, rightmostPoint_right



# This is the method that gets called by the GUI and actually executes
# the finding of the hull
	def compute_hull( self, points, pause, view):
		self.pause = pause
		self.view = view
		assert( type(points) == list and type(points[0]) == QPointF )

		t1 = time.time()
		# TODO: SORT THE POINTS BY INCREASING X-VALUE

		##########################
		# Time Complexity O(nlogn)
		# Space Complexity O(n)
		##########################
		points = sorted(points, key=lambda k: k.x())
		t2 = time.time()

		t3 = time.time()
		# this is a dummy polygon of the first 3 unsorted points
		# polygon = [QLineF(points[i],points[(i+1)%3]) for i in range(3)]
		returnedPoints, rightMostPoint = self.solver(points)
		polygon = [QLineF(returnedPoints[i], returnedPoints[(i + 1) % len(returnedPoints)]) for i in range(len(returnedPoints))]
		# TODO: REPLACE THE LINE ABOVE WITH A CALL TO YOUR DIVIDE-AND-CONQUER CONVEX HULL SOLVER
		t4 = time.time()
		self.showHull(polygon, RED)
		# when passing lines to the display, pass a list of QLineF objects.  Each QLineF
		# object can be created with two QPointF objects corresponding to the endpoints
		self.showText('Time Elapsed (QuickSort): {:3.14f}'.format(t2-t1) + '  Time Elapsed (Convex Hull): {:3.14f} sec'.format(t4-t3))






