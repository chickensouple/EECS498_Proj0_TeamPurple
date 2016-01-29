from joy import *
from actions import *
from steps import *
from state import *
import time

# parameters
hipMotorString = "Nx0C"
shoulderMotorString = "Nx0B"

class KayakApp(JoyApp):
	def __init__(self, hipMotor, shoulderMotor, *arg, **kw):
		JoyApp.__init__(self, *arg, **kw)
		self.hipMotorString = hipMotorString
		self.shoulderMotorString = shoulderMotorString

		self.motorAccuracy = 200
		self.hipRight = 4600
		self.hipLeft = -4600
		self.shoulderLeftBegin = -205
		self.shoulderLeftEnd = -2700
		self.shoulderRightBegin = 205
		self.shoulderRightEnd = 2700

		self.motorSpeedFast = 113
		self.motorSpeedSlow = 60

		exec("self.hipMotor = self.robot.at." + hipMotorString)
		exec("self.shoulderMotor = self.robot.at." + shoulderMotorString)

	## GENERAL FUNCTIONS
	def moveMotors(self, hipMotorPos, shoulderMotorPos):
		self.hipMotor.set_pos(hipMotorPos)
		self.shoulderMotor.set_pos(shoulderMotorPos)

	def setSpeed(self, speed):
		self.hipMotor.set_speed(speed)
		self.shoulderMotor.set_speed(speed)

		# make sure the speed was actually set
		while (abs(self.hipMotor.get_moving_speed() - speed) > 10):
			self.hipMotor.set_speed(speed)
		while (abs(self.hipMotor.get_moving_speed() - speed) > 10):
			self.shoulderMotor.set_speed(speed)

	def currState(self):
		hipMotorAngle = self.hipMotor.get_pos()
		hipDifferences = dict()
		hipDifferences[abs(hipMotorAngle - self.hipLeft)] = 0
		hipDifferences[abs(hipMotorAngle - self.hipRight)] = 1

		closestHipAngle = hipDifferences[min(hipDifferences)]

		shoulderMotorAngle = self.shoulderMotor.get_pos()

		if (closestHipAngle == 0):
			# hip left
			shoulderLeftBeginDiff = abs(shoulderMotorAngle - self.shoulderLeftBegin)
			shoulderLeftEndDiff = abs(shoulderMotorAngle - self.shoulderLeftEnd)
			if (shoulderLeftBeginDiff < shoulderLeftEndDiff):
				return State.LEFT_BEGIN
			else:
				return State.LEFT_END
		else:
			# hip right
			shoulderRightBeginDiff = abs(shoulderMotorAngle - self.shoulderRightBegin)
			shoulderRightEndDiff = abs(shoulderMotorAngle - self.shoulderRightEnd)
			if (shoulderRightBeginDiff < shoulderRightEndDiff):
				return State.RIGHT_BEGIN
			else:
				return State.RIGHT_END

	def onStart(self):
		self.rightStrokeAction = RightStrokeAction(self)
		self.leftStrokeAction = LeftStrokeAction(self)
		self.rightToLeftTransitionAction = RightToLeftTransitionAction(self)
		self.leftToRightTransitionAction = LeftToRightTransitionAction(self)
		self.rightResetAction = RightResetAction(self)
		self.leftResetAction = LeftResetAction(self)

		self.rightStrokeStep = RightStrokeStep(self)
		self.leftStrokeStep = LeftStrokeStep(self)
		self.forwardStrokeStep = ForwardStep(self)

	def onEvent(self, evt):
		if evt.type == TIMEREVENT:
			pass

		if evt.type != KEYDOWN:
			return

		if evt.key == K_q:
			self.hipMotor.go_slack()
			self.shoulderMotor.go_slack()
			print("Slack")
		elif evt.key == K_a:
			print("Begin Left")
			self.leftStrokeStep.start()
			print("End Left")
		elif evt.key == K_d:
			print("Begin Right")
			self.rightStrokeStep.start()
			print("End Right")
		elif evt.key == K_w:
			print("Begin Forward")
			self.forwardStrokeStep.start()
			print("End Forward")
		elif evt.key == K_x:
			print "hip: " + str(self.hipMotor.get_pos())
			print "shoulder: " + str(self.shoulderMotor.get_pos())
			print "state: " + str(self.currState())

robot = {"count": 2}
scr = {}

app = KayakApp(hipMotorString, shoulderMotorString, robot=robot, scr=scr)
app.run()
