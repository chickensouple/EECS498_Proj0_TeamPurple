from joy import *

# parameters
hipMotorString = "Nx0C"
shoulderMotorString = "Nx0B"

class State:
	NEUTRAL = 1
	LEFT_BEGIN_NEUTRAL = 2
	LEFT_BEGIN = 3
	LEFT_END = 4
	LEFT_END_NEUTRAL = 5
	RIGHT_BEGIN_NEUTRAL = 6
	RIGHT_BEGIN = 7
	RIGHT_END = 8
	RIGHT_END_NEUTRAL = 9
	INVALID = 10


class KayakApp(JoyApp):
	def __init__(self, hipMotor, shoulderMotor, *arg, **kw):
		JoyApp.__init__(self, *arg, **kw)
		self.hipMotorString = hipMotorString
		self.shoulderMotorString = shoulderMotorString
		self.motorAccuracy = 150

		self.hipRight = 4600
		self.hipLeft = -4600
		self.shoulderLeftBegin = 205
		self.shoulderLeftEnd = 2700
		self.shoulderRightBegin = -205
		self.shoulderRightEnd = -2700

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
		elif (state == State.LEFT_BEGIN_NEUTRAL):
			self.moveMotors(0, self.shoulderLeftBegin)
		elif (state == State.LEFT_BEGIN):
			self.moveMotors(self.hipLeft, self.shoulderLeftBegin)
		elif (state == State.LEFT_END):
			self.moveMotors(self.hipLeft, self.shoulderLeftEnd)
		elif (state == State.LEFT_END_NEUTRAL):
			self.moveMotors(0, self.shoulderLeftEnd)
		elif (state == State.RIGHT_BEGIN_NEUTRAL):
			self.moveMotors(0, self.shoulderRightBegin)
		elif (state == State.RIGHT_BEGIN):
			self.moveMotors(self.hipRight, self.shoulderRightBegin)
		elif (state == State.RIGHT_END):
			self.moveMotors(self.hipRight, self.shoulderRightEnd)
		elif (state == State.RIGHT_END_NEUTRAL):
			self.moveMotors(0, self.shoulderRightEnd)

	def currState(self):
		hipMotorAngle = self.hipMotor.get_pos()
		hipDifferences = dict()
		hipDifferences[abs(hipMotorAngle - self.hipLeft)] = 0
		hipDifferences[abs(hipMotorAngle - 0)] = 1
		hipDifferences[abs(hipMotorAngle - self.hipRight)] = 2

		shoulderMotorAngle = self.shoulderMotor.get_pos()
		shoulderRightBeginDiff = abs(shoulderMotorAngle - self.shoulderRightBegin)
		shoulderRightEndDiff = abs(shoulderMotorAngle - self.shoulderRightEnd)
		shoulderLeftBeginDiff = abs(shoulderMotorAngle - self.shoulderLeftBegin)
		shoulderLeftEndDiff = abs(shoulderMotorAngle - self.shoulderLeftEnd)

		closestHipAngle = hipDifferences[min(hipDifferences)]

		if (closestHipAngle == 0):
			# hip left
			if (shoulderLeftBeginDiff < shoulderLeftEndDiff):
				return State.LEFT_BEGIN
			else:
				return State.LEFT_END
		elif (closestHipAngle == 2):
			# hip right
			if (shoulderRightBeginDiff < shoulderRightEndDiff):
				return State.RIGHT_BEGIN
			else:
				return State.RIGHT_END
		else:
			# hip center
			shoulderDifferences = dict()
			shoulderDifferences[shoulderRightBeginDiff] = 0
			shoulderDifferences[shoulderRightEndDiff] = 1
			shoulderDifferences[shoulderLeftBeginDiff] = 2
			shoulderDifferences[shoulderLeftEndDiff] = 3
			shoulderDifferences[abs(shoulderMotorAngle)] = 4

			closestShoulderAngle = shoulderDifferences[min(shoulderDifferences)]

			return {
				0 : State.RIGHT_BEGIN_NEUTRAL,
				1 : State.RIGHT_END_NEUTRAL,
				2 : State.LEFT_BEGIN_NEUTRAL,
				3 : State.LEFT_END_NEUTRAL,
				4 : State.NEUTRAL
			}.get(closestShoulderAngle, State.INVALID)

	## PATTERNS
	def strokeRight(self, currState, initialCall = True):
		if (not initialCall):
			self.gotoState(currState)

		if (currState == State.NEUTRAL):
			return self.strokeRight(State.RIGHT_BEGIN_NEUTRAL, False)
		elif (currState == State.LEFT_BEGIN_NEUTRAL):
			return self.strokeRight(State.RIGHT_BEGIN_NEUTRAL, False)
		elif (currState == State.LEFT_BEGIN):
			return self.strokeRight(State.LEFT_BEGIN_NEUTRAL, False)
		elif (currState == State.LEFT_END):
			return self.strokeRight(State.LEFT_END_NEUTRAL, False)
		elif (currState == State.LEFT_END_NEUTRAL):
			# return self.strokeRight(State.RIGHT_BEGIN_NEUTRAL, False)
			return self.strokeRight(State.RIGHT_BEGIN, False)
		elif (currState == State.RIGHT_BEGIN_NEUTRAL):
			return self.strokeRight(State.RIGHT_BEGIN, False)
		elif (currState == State.RIGHT_BEGIN):
			return self.strokeRight(State.RIGHT_END, False)
		elif (currState == State.RIGHT_END):
			if (initialCall):
				return self.strokeRight(State.RIGHT_END_NEUTRAL, False)
			else:
				return
		elif (currState == State.RIGHT_END_NEUTRAL):
			return self.strokeRight(State.LEFT_BEGIN, False)

	def strokeLeft(self, currState, initialCall = True):
		if (not initialCall):
			self.gotoState(currState)

		if (currState == State.NEUTRAL):
			return self.strokeLeft(State.LEFT_BEGIN_NEUTRAL, False)
		elif (currState == State.RIGHT_BEGIN_NEUTRAL):
			return self.strokeLeft(State.LEFT_BEGIN_NEUTRAL, False)
		elif (currState == State.RIGHT_BEGIN):
			return self.strokeLeft(State.RIGHT_BEGIN_NEUTRAL, False)
		elif (currState == State.RIGHT_END):
			return self.strokeLeft(State.RIGHT_END_NEUTRAL, False)
		elif (currState == State.RIGHT_END_NEUTRAL):
			# return self.strokeLeft(State.LEFT_BEGIN_NEUTRAL, False)
			return self.strokeLeft(State.LEFT_BEGIN, False)
		elif (currState == State.LEFT_BEGIN_NEUTRAL):
			return self.strokeLeft(State.LEFT_BEGIN, False)
		elif (currState == State.LEFT_BEGIN):
			return self.strokeLeft(State.LEFT_END, False)
		elif (currState == State.LEFT_END):
			if (initialCall):
				return self.strokeLeft(State.LEFT_END_NEUTRAL, False)
			else:
				return
		elif (currState == State.LEFT_END_NEUTRAL):
			return self.strokeLeft(State.RIGHT_BEGIN, False)

	def strokeNeutral(self, currState, initialCall = True):
		self.gotoState(State.NEUTRAL)

	# Higher Level Patterns
	# def strokeForward(self, currState):


	def onStart(self):
		pass

	def onEvent(self, evt):
		if evt.type == TIMEREVENT:
			pass

		if evt.type != KEYDOWN:
			return

		if evt.key == K_w:
			print "state: " + str(self.currState())
			print "hip: " + str(self.hipMotor.get_pos())
			print "shoulder: " + str(self.shoulderMotor.get_pos())
		elif evt.key == K_d:
			print "Start right stroke"
			self.strokeRight(self.currState())
			print "End right stroke"
		elif evt.key == K_a:
			print "Start left stroke"
			self.strokeLeft(self.currState())
			print "End left stroke"
		elif evt.key == K_s:
			print "Start neutral position"
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

