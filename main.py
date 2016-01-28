from joy import *
import time

# parameters
hipMotorString = "Nx0C"
shoulderMotorString = "Nx0B"

class RightStrokePlan(Plan):
	def __init__(self, app, *arg, **kw):
		Plan.__init__(self, app, *arg, **kw)
		
	def behavior(self):
		self.app.setSpeed(20)

		# targetPos = self.app.shoulderRightBegin
		# n = 20
		# totalTime = 0.5
		# distance = self.app.shoulderRightEnd - self.app.shoulderRightBegin

		# deltaTime = totalTime / n
		# deltaDistance = distance / n

		# T0 = self.app.now
		# print("deltaTime: " + str(deltaTime))
		# for i in range(n):
		# 	targetPos += deltaDistance
		# 	self.app.moveMotors(self.app.hipRight, targetPos)
		# 	print("Target pos: " + str(targetPos))
		# 	yield self.forDuration(deltaTime)

		self.app.moveMotors(self.app.hipRight, self.app.shoulderRightEnd)
		while (abs(self.app.shoulderMotor.get_pos() - self.app.shoulderRightEnd) > self.app.motorAccuracy):
			yield self.forDuration(0.05)
		while (abs(self.app.hipMotor.get_pos() - self.app.hipRight) > self.app.motorAccuracy):
			yield self.forDuration(0.05)

class LeftStrokePlan(Plan):
	def __init__(self, app, *arg, **kw):
		Plan.__init__(self, app, *arg, **kw)

	def behavior(self):
		self.app.setSpeed(20)
		self.app.moveMotors(self.app.hipLeft, self.app.shoulderLeftEnd)

		while (abs(self.app.shoulderMotor.get_pos() - self.app.shoulderLeftEnd) > self.app.motorAccuracy):
			yield self.forDuration(0.05)
		while (abs(self.app.hipMotor.get_pos() - self.app.hipLeft) > self.app.motorAccuracy):
			yield self.forDuration(0.05)

class RightToLeftTransitionPlan(Plan):
	def __init__(self, app, *arg, **kw):
		Plan.__init__(self, app, *arg, **kw)

	def behavior(self):
		self.app.setSpeed(101)

		self.app.moveMotors(self.app.hipLeft, self.app.shoulderLeftBegin)
		while (abs(self.app.shoulderMotor.get_pos() - self.app.shoulderLeftBegin) > self.app.motorAccuracy):
			yield self.forDuration(0.05)
		while (abs(self.app.hipMotor.get_pos() - self.app.hipLeft) > self.app.motorAccuracy):
			yield self.forDuration(0.05)

class LeftToRightTransitionPlan(Plan):
	def __init__(self, app, *arg, **kw):
		Plan.__init__(self, app, *arg, **kw)

	def behavior(self):
		pass

class RightResetPlan(Plan):
	def __init__(self, app, *arg, **kw):
		Plan.__init__(self, app, *arg, **kw)

	def behavior(self):
		pass

class LeftResetPlan(Plan):
	def __init__(self, app, *arg, **kw):
		Plan.__init__(self, app, *arg, **kw)

	def behavior(self):
		pass

class KayakApp(JoyApp):
	def __init__(self, hipMotor, shoulderMotor, *arg, **kw):
		JoyApp.__init__(self, *arg, **kw)
		self.hipMotorString = hipMotorString
		self.shoulderMotorString = shoulderMotorString

		self.motorAccuracy = 150
		self.hipRight = 4200
		self.hipLeft = -4200
		self.shoulderLeftBegin = 1000
		self.shoulderLeftEnd = -2700
		self.shoulderRightBegin = -1000
		self.shoulderRightEnd = 2700

		exec("self.hipMotor = self.robot.at." + hipMotorString)
		exec("self.shoulderMotor = self.robot.at." + shoulderMotorString)

	def moveMotors(self, hipMotorPos, shoulderMotorPos):
		self.hipMotor.set_pos(hipMotorPos)
		self.shoulderMotor.set_pos(shoulderMotorPos)

	def setSpeed(self, speed):
		self.hipMotor.set_speed(speed)
		self.shoulderMotor.set_speed(speed)

	def onStart(self):
		self.rightStrokePlan = RightStrokePlan(self)
		self.leftStrokePlan = LeftStrokePlan(self)
		self.rightToLeftTransitionPlan = RightToLeftTransitionPlan(self)
		self.leftToRightTransitionPlan = LeftToRightTransitionPlan(self)
		self.rightResetPlan = RightResetPlan(self)
		self.leftResetPlan = LeftResetPlan(self)

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
			# self.moveMotors(self.hipLeft, self.shoulderLeftBegin)
			self.leftStrokePlan.start()
			print("End Left")
		elif evt.key == K_d:
			print("Begin Right")
			# self.moveMotors(self.hipRight, self.shoulderRightBegin)
			self.rightStrokePlan.start()
			print("End Right")
		elif evt.key == K_x:
			print "hip: " + str(self.hipMotor.get_pos())
			print "shoulder: " + str(self.shoulderMotor.get_pos())
			self.rightToLeftTransitionPlan.start()

		# if evt.key == K_q:
		# 	self.hipMotor.go_slack()
		# 	self.shoulderMotor.go_slack()
		# 	print("Slack")
		# elif evt.key == K_d:
		# 	print("Begin Right")
		# 	self.moveMotors(self.hipRight, self.shoulderRightBegin)
		# 	yield self.forDuration(0.5)
		# 	self.rightStrokePlan.start()
		# 	print("End Right")

		# if evt.key == K_x:
		# 	print "state: " + str(self.currState())
		# 	print "hip: " + str(self.hipMotor.get_pos())
		# 	print "shoulder: " + str(self.shoulderMotor.get_pos())
		# elif evt.key == K_w:
		# 	print "Start Forward Stroke"
		# 	self.strokeForward(self.currState())
		# 	print "End Forward Stroke"
		# elif evt.key == K_d:
		# 	print "Start right stroke"
		# 	self.strokeRight(self.currState())
		# 	print "End right stroke"
		# elif evt.key == K_a:
		# 	print "Start left stroke"
		# 	self.strokeLeft(self.currState())
		# 	print "End left stroke"
		# elif evt.key == K_s:
		# 	print "Start neutral position"
		# 	self.strokeNeutral(self.currState())
		# 	print "End neutral position"
		# elif evt.key == K_c:
		# 	print "Start Right Back Stroke"
		# 	self.strokeRightBack(self.currState())
		# 	print "End Right Back Stroke"
		# elif evt.key == K_z:
		# 	print "Start Left Back Stroke"
		# 	self.strokeLeftBack(self.currState())
		# 	print "End Left Back Stroke"
		# elif evt.key == K_q:
		# 	self.hipMotor.go_slack()
		# 	self.shoulderMotor.go_slack()
		# 	print "Slack"

robot = {"count": 2}
scr = {}

app = KayakApp(hipMotorString, shoulderMotorString, robot=robot, scr=scr)
app.run()
