from joy import *

# parameters
hipMotorString = "Nx0C"
shoulderMotorString = "Nx0B"

class State:
	NEUTRAL = 1
	LEFT_NEUTRAL = 2
	LEFT_BEGIN = 3
	LEFT_END = 4
	RIGHT_NEUTRAL = 5
	RIGHT_BEGIN = 6
	RIGHT_END = 7
	INVALID = 8

class KayakApp(JoyApp):

	def __init__(self, hipMotor, shoulderMotor, *arg, **kw):
		JoyApp.__init__(self, *arg, **kw)
		self.hipMotorString = hipMotorString
		self.shoulderMotorString = shoulderMotorString
		self.motorAccuracy = 200

		self.hipRight = 3000
		self.hipLeft = -3000
		self.shoulderRightFront = 4500
		self.shoulderLeftFront = -4500

		exec("self.hipMotor = self.robot.at." + hipMotorString)
		exec("self.shoulderMotor = self.robot.at." + shoulderMotorString)

	## GENERAL FUNCTIONS
	def moveMotors(self, hipMotorPos, shoulderMotorPos):
		self.hipMotor.set_pos(hipMotorPos)
		self.shoulderMotor.set_pos(shoulderMotorPos)
		while(abs(self.hipMotor.get_pos() - hipMotorPos) > self.motorAccuracy):
			continue
		while(abs(self.shoulderMotor.get_pos() - shoulderMotorPos) > self.motorAccuracy):
			continue

	## STATES
	def gotoState(self, state):
		if (state == State.NEUTRAL):
			self.moveMotors(0, 0)
		elif (state == State.LEFT_NEUTRAL):
			self.moveMotors(0, self.shoulderLeftFront)
		elif (state == State.LEFT_BEGIN):
			self.moveMotors(self.hipLeft, self.shoulderLeftFront)
		elif (state == State.LEFT_END):
			self.moveMotors(self.hipLeft, self.shoulderRightFront)
		elif (state == State.RIGHT_NEUTRAL):
			self.moveMotors(0, self.shoulderRightFront)
		elif (state == State.RIGHT_BEGIN):
			self.moveMotors(self.hipRight, self.shoulderRightFront)
		elif (state == State.RIGHT_END):
			self.moveMotors(self.hipRight, self.shoulderLeftFront)


	def currState(self):
		hipMotorAngle = self.hipMotor.get_pos()
		hipDifferences = dict()
		hipDifferences[abs(hipMotorAngle - self.hipLeft)] = 0
		hipDifferences[abs(hipMotorAngle - 0)] = 1
		hipDifferences[abs(hipMotorAngle - self.hipRight)] = 2

		shoulderMotorAngle = self.shoulderMotor.get_pos()
		shoulderDifferences = dict()
		shoulderDifferences[abs(shoulderMotorAngle - self.shoulderRightFront)] = 0
		shoulderDifferences[abs(shoulderMotorAngle - 0)] = 1
		shoulderDifferences[abs(shoulderMotorAngle - self.shoulderLeftFront)] = 2

		closestHipAngle = hipDifferences[min(hipDifferences)]
		closestShoulderAngle = shoulderDifferences[min(shoulderDifferences)]

		if (closestHipAngle == 0):
			# hip left
			if (closestShoulderAngle == 0):
				# shoulder right front
				return State.LEFT_END
			elif (closestShoulderAngle == 1):
				# shoulder center
				return State.INVALID
			else:
				# shoulder left front
				return State.LEFT_BEGIN
		elif (closestHipAngle == 1):
			# hip center
			if (closestShoulderAngle == 0):
				# shoulder right front
				return State.RIGHT_NEUTRAL
			elif (closestShoulderAngle == 1):
				# shoulder center
				return State.NEUTRAL
			else:
				# shoulder left front
				return State.LEFT_NEUTRAL
		else:
			# hip right
			if (closestShoulderAngle == 0):
				# shoulder right front
				return State.RIGHT_BEGIN
			elif (closestShoulderAngle == 1):
				# shoulder center
				return State.INVALID
			else:
				# shoulder left front
				return State.RIGHT_END

	## PATTERNS
	def strokeRight(self, currState, initialCall = True):
		# print("Stroke Right: " + str(currState))
		if (not initialCall):
			self.gotoState(currState)

		if (currState == State.NEUTRAL):
			return self.strokeRight(State.RIGHT_BEGIN, False)
		elif (currState == State.LEFT_NEUTRAL):
			return self.strokeRight(State.RIGHT_NEUTRAL, False)
		elif (currState == State.LEFT_BEGIN):
			return self.strokeRight(State.LEFT_NEUTRAL, False)
		elif (currState == State.LEFT_END):
			return self.strokeRight(State.RIGHT_BEGIN, False)
		elif (currState == State.RIGHT_NEUTRAL):
			return self.strokeRight(State.RIGHT_BEGIN, False)
		elif (currState == State.RIGHT_BEGIN):
			return self.strokeRight(State.RIGHT_END, False)
		elif (currState == State.RIGHT_END):
			if (initialCall):
				return self.strokeRight(State.LEFT_NEUTRAL, False)
			else:
				return

	def strokeLeft(self, currState, initialCall = True):
		if (not initialCall):
			self.gotoState(currState)

		if (currState == State.NEUTRAL):
			return self.strokeLeft(State.LEFT_BEGIN, False)
		elif (currState == State.RIGHT_NEUTRAL):
			return self.strokeLeft(State.LEFT_NEUTRAL, False)
		elif (currState == State.RIGHT_BEGIN):
			return self.strokeLeft(State.RIGHT_NEUTRAL, False)
		elif (currState == State.RIGHT_END):
			return self.strokeLeft(State.LEFT_BEGIN, False)
		elif (currState == State.LEFT_NEUTRAL):
			return self.strokeLeft(State.LEFT_BEGIN, False)
		elif (currState == State.LEFT_BEGIN):
			return self.strokeLeft(State.LEFT_END, False)
		elif (currState == State.LEFT_END):
			if (initialCall):
				return self.strokeLeft(State.RIGHT_NEUTRAL, False)
			else:
				return

	def strokeNeutral(self, currState, initialCall = True):
		if (not initialCall):
			self.gotoState(currState)

		if (currState == State.NEUTRAL):
			return
		elif (currState == State.RIGHT_NEUTRAL):
			return self.strokeNeutral(State.NEUTRAL, False)
		elif (currState == State.RIGHT_BEGIN):
			return self.strokeNeutral(State.RIGHT_NEUTRAL, False)
		elif (currState == State.RIGHT_END):
			return self.strokeNeutral(State.LEFT_NEUTRAL, False)
		elif (currState == State.LEFT_NEUTRAL):
			return self.strokeNeutral(State.NEUTRAL, False)
		elif (currState == State.LEFT_BEGIN):
			return self.strokeNeutral(State.LEFT_NEUTRAL, False)
		elif (currState == State.LEFT_END):
			return self.strokeNeutral(State.RIGHT_NEUTRAL, False)

	def onStart(self):
		pass

	def onEvent(self, evt):
		if evt.type == TIMEREVENT:
			pass

		if evt.type != KEYDOWN:
			return

		if evt.key == K_w:
			print str(self.currState())
			# print "hip: " + str(self.hipMotor.get_pos())
			# print "shoulder: " + str(self.shoulderMotor.get_pos())
		elif evt.key == K_d:
			print "Start right stroke"
			# rightStroke(self.hipMotor, self.shoulderMotor)
			self.strokeRight(self.currState())
			print "End right stroke"
		elif evt.key == K_a:
			print "Start left stroke"
			# leftStroke(self.hipMotor, self.shoulderMotor)
			self.strokeLeft(self.currState())
			print "End left stroke"
		elif evt.key == K_s:
			print "Start neutral position"
			# neutralPosition(self.hipMotor, self.shoulderMotor)
			self.strokeNeutral(self.currState())
			print "End neutral position"
		elif evt.key == K_z:
			self.hipMotor.go_slack()
			self.shoulderMotor.go_slack()
			print "Slack"

robot = {"count": 2}
scr = {}

app = KayakApp(hipMotorString, shoulderMotorString, robot=robot, scr=scr)
app.run()

