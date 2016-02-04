from joy import *

# The functions in this file are the lowest type of action that can be done. 
# They merely move the robot between two states on the state transition diagram
# see the "State Diagram" section in the Code Documentation for more details

class RightStrokeAction(Plan):
	""" Moves the robot from Right Begin State to Right End State 
		And waits for the motors to be within motorAccuracy of the target position
		This plan will move the motors at a slow speed
	"""
	def __init__(self, app, *arg, **kw):
		Plan.__init__(self, app, *arg, **kw)
		
	def behavior(self):
		self.app.setSpeed(self.app.motorSpeedSlow)

		shoulderRightEnd = self.app.shoulderRightEnd * self.app.strokeLength
		self.app.moveMotors(self.app.hipRight, shoulderRightEnd)

		while (abs(self.app.shoulderMotor.get_pos() - shoulderRightEnd) > self.app.motorAccuracy):
			yield self.forDuration(0.01)
		while (abs(self.app.hipMotor.get_pos() - self.app.hipRight) > self.app.motorAccuracy):
			yield self.forDuration(0.01)

class LeftStrokeAction(Plan):
	""" Moves the robot from Left Begin State to Left End State 
		And waits for the motors to be within motorAccuracy of the target position
		This plan will move the motors at a slow speed
	"""
	def __init__(self, app, *arg, **kw):
		Plan.__init__(self, app, *arg, **kw)

	def behavior(self):
		self.app.setSpeed(self.app.motorSpeedSlow)

		shoulderLeftEnd = self.app.shoulderLeftEnd * self.app.strokeLength
		self.app.moveMotors(self.app.hipLeft, shoulderLeftEnd)

		while (abs(self.app.shoulderMotor.get_pos() - shoulderLeftEnd) > self.app.motorAccuracy):
			yield self.forDuration(0.01)
		while (abs(self.app.hipMotor.get_pos() - self.app.hipLeft) > self.app.motorAccuracy):
			yield self.forDuration(0.01)

class RightToLeftTransitionAction(Plan):
	""" Moves Robot from Right End State to Left Begin State 
		And waits for the motors to be within motorAccuracy of the target position
		This plan will move the motors at a fast speed
	"""
	def __init__(self, app, *arg, **kw):
		Plan.__init__(self, app, *arg, **kw)

	def behavior(self):
		self.app.setSpeed(self.app.motorSpeedFast)

		shoulderLeftBegin = self.app.shoulderLeftBegin * self.app.strokeLength

		self.app.moveMotors(self.app.hipLeft, shoulderLeftBegin)
		while (abs(self.app.shoulderMotor.get_pos() - shoulderLeftBegin) > self.app.motorAccuracy):
			yield self.forDuration(0.01)
		while (abs(self.app.hipMotor.get_pos() - self.app.hipLeft) > self.app.motorAccuracy):
			yield self.forDuration(0.01)

class LeftToRightTransitionAction(Plan):
	""" Moves Robot from Left End State to Right Begin State 
		And waits for the motors to be within motorAccuracy of the target position
		This plan will move the motors at a fast speed
	"""
	def __init__(self, app, *arg, **kw):
		Plan.__init__(self, app, *arg, **kw)

	def behavior(self):
		self.app.setSpeed(self.app.motorSpeedFast)

		shoulderRightBegin = self.app.shoulderRightBegin * self.app.strokeLength

		self.app.moveMotors(self.app.hipRight, shoulderRightBegin)
		while (abs(self.app.shoulderMotor.get_pos() - shoulderRightBegin) > self.app.motorAccuracy):
			yield self.forDuration(0.01)
		while (abs(self.app.hipMotor.get_pos() - self.app.hipRight) > self.app.motorAccuracy):
			yield self.forDuration(0.01)

class RightResetAction(Plan):
	""" Moves Robot from Right End State to Right Begin State 
		And waits for the motors to be within motorAccuracy of the target position
		This plan will move the motors at a fast speed
	"""
	def __init__(self, app, *arg, **kw):
		Plan.__init__(self, app, *arg, **kw)

	def behavior(self):
		self.app.setSpeed(self.app.motorSpeedFast)

		currShoulder = self.app.shoulderMotor.get_pos()

		# hip up is how far we should move the hip off the ground
		# the smaller the scalar hipRight is multiplied, the higher it lefts up
		# when it is 0, the hip is straight up
		hipUp = self.app.hipRight * 0.0

		# lift up hip motor
		self.app.moveMotors(hipUp, currShoulder)
		while (abs(self.app.shoulderMotor.get_pos() - currShoulder) > self.app.motorAccuracy):
			yield self.forDuration(0.01)
		while (abs(self.app.hipMotor.get_pos() - hipUp) > self.app.motorAccuracy):
			yield self.forDuration(0.01)

		shoulderRightBegin = self.app.shoulderRightBegin * self.app.strokeLength

		# move shoulder motor
		self.app.moveMotors(hipUp, shoulderRightBegin)
		while (abs(self.app.shoulderMotor.get_pos() - shoulderRightBegin) > self.app.motorAccuracy):
			yield self.forDuration(0.01)
		while (abs(self.app.hipMotor.get_pos() - hipUp) > self.app.motorAccuracy):
			yield self.forDuration(0.01)

		# lower hip motor
		self.app.moveMotors(self.app.hipRight, shoulderRightBegin)
		while (abs(self.app.shoulderMotor.get_pos() - shoulderRightBegin) > self.app.motorAccuracy):
			yield self.forDuration(0.01)
		while (abs(self.app.hipMotor.get_pos() - self.app.hipRight) > self.app.motorAccuracy):
			yield self.forDuration(0.01)

class LeftResetAction(Plan):
	""" Moves Robot from Left End State to Left Begin State 
		And waits for the motors to be within motorAccuracy of the target position
		This plan will move the motors at a fast speed
	"""
	def __init__(self, app, *arg, **kw):
		Plan.__init__(self, app, *arg, **kw)

	def behavior(self):
		self.app.setSpeed(self.app.motorSpeedFast)
		
		currShoulder = self.app.shoulderMotor.get_pos()

		# hip up is how far we should move the hip off the ground
		# the smaller the scalar hipLeft is multiplied, the higher it lefts up
		# when it is 0, the hip is straight up
		hipUp = self.app.hipLeft * 0.0

		# lift up hip motor
		self.app.moveMotors(hipUp, currShoulder)
		while (abs(self.app.shoulderMotor.get_pos() - currShoulder) > self.app.motorAccuracy):
			yield self.forDuration(0.01)
		while (abs(self.app.hipMotor.get_pos() - hipUp) > self.app.motorAccuracy):
			yield self.forDuration(0.01)

		shoulderLeftBegin = self.app.shoulderLeftBegin * self.app.strokeLength

		# move shoulder motor
		self.app.moveMotors(hipUp, shoulderLeftBegin)
		while (abs(self.app.shoulderMotor.get_pos() - shoulderLeftBegin) > self.app.motorAccuracy):
			yield self.forDuration(0.01)
		while (abs(self.app.hipMotor.get_pos() - hipUp) > self.app.motorAccuracy):
			yield self.forDuration(0.01)

		# lower hip motor
		self.app.moveMotors(self.app.hipLeft, shoulderLeftBegin)
		while (abs(self.app.shoulderMotor.get_pos() - shoulderLeftBegin) > self.app.motorAccuracy):
			yield self.forDuration(0.01)
		while (abs(self.app.hipMotor.get_pos() - self.app.hipLeft) > self.app.motorAccuracy):
			yield self.forDuration(0.01)