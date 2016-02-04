from joy import *
from actions import *
from steps import *
from state import *
import time

# parameters
hipMotorNum = 0x0c
shoulderMotorNum = 0x0b

class KayakApp(JoyApp):
	""" Main app to run the program that controls our robot """
	def __init__(self, *arg, **kw):
		cfg = dict(
			nodeNames = { 
				hipMotorNum : 'hip',
				shoulderMotorNum : 'shoulder'
		})
		JoyApp.__init__(self, cfg=cfg, *arg, **kw)

		self.motorAccuracy = 300
		self.hipRight = 1300
		self.hipLeft = -1600
		self.shoulderLeftBegin = 3000
		self.shoulderLeftEnd = -3000
		self.shoulderRightBegin = -3000
		self.shoulderRightEnd = 3000

		self.strokeLength = 1.0

		self.motorSpeedFast = 113
		self.motorSpeedSlow = 90

		self.hipMotor = self.robot.at.hip
 		self.shoulderMotor = self.robot.at.shoulder

	## GENERAL FUNCTIONS
	def moveMotors(self, hipMotorPos, shoulderMotorPos):
		""" Sends a command to the hip and shoulder motor in centidegrees """
		self.hipMotor.set_pos(hipMotorPos)
		self.shoulderMotor.set_pos(shoulderMotorPos)

	def setSpeed(self, speed):
		""" Sets the speed of the servo motors on a range of [0, 113] """
		self.hipMotor.set_speed(speed)
		self.shoulderMotor.set_speed(speed)

		# make sure the speed was actually set
		while (abs(self.hipMotor.get_moving_speed() - speed) > 10):
			self.hipMotor.set_speed(speed)
		while (abs(self.hipMotor.get_moving_speed() - speed) > 10):
			self.shoulderMotor.set_speed(speed)

	def currState(self):
		""" 
			This looks at the current angles the robot's motors are at and returns
			what the closest state to it is as defined by the state transition diagram
		"""
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
		elif evt.key == K_y:
			self.strokeLength = 0.2
		elif evt.key == K_u:
			self.strokeLength = 0.4
		elif evt.key == K_i:
			self.strokeLength = 0.6
		elif evt.key == K_o:
			self.strokeLength = 0.8
		elif evt.key == K_p:
			self.strokeLength = 1.0


robot = {"count": 2}
scr = {}

app = KayakApp(robot=robot, scr=scr)
app.run()
