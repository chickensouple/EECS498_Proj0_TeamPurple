from joy import *

class RightStrokeAction(Plan):
	def __init__(self, app, *arg, **kw):
		Plan.__init__(self, app, *arg, **kw)
		
	def behavior(self):
		self.app.setSpeed(self.app.motorSpeedSlow)

		self.app.moveMotors(self.app.hipRight, self.app.shoulderRightEnd)

		while (abs(self.app.shoulderMotor.get_pos() - self.app.shoulderRightEnd) > self.app.motorAccuracy):
			yield self.forDuration(0.01)
		while (abs(self.app.hipMotor.get_pos() - self.app.hipRight) > self.app.motorAccuracy):
			yield self.forDuration(0.01)

class LeftStrokeAction(Plan):
	def __init__(self, app, *arg, **kw):
		Plan.__init__(self, app, *arg, **kw)

	def behavior(self):
		self.app.setSpeed(self.app.motorSpeedSlow)
		self.app.moveMotors(self.app.hipLeft, self.app.shoulderLeftEnd)

		while (abs(self.app.shoulderMotor.get_pos() - self.app.shoulderLeftEnd) > self.app.motorAccuracy):
			yield self.forDuration(0.01)
		while (abs(self.app.hipMotor.get_pos() - self.app.hipLeft) > self.app.motorAccuracy):
			yield self.forDuration(0.01)

class RightToLeftTransitionAction(Plan):
	def __init__(self, app, *arg, **kw):
		Plan.__init__(self, app, *arg, **kw)

	def behavior(self):
		self.app.setSpeed(self.app.motorSpeedFast)

		self.app.moveMotors(self.app.hipLeft, self.app.shoulderLeftBegin)
		while (abs(self.app.shoulderMotor.get_pos() - self.app.shoulderLeftBegin) > self.app.motorAccuracy):
			yield self.forDuration(0.01)
		while (abs(self.app.hipMotor.get_pos() - self.app.hipLeft) > self.app.motorAccuracy):
			yield self.forDuration(0.01)

class LeftToRightTransitionAction(Plan):
	def __init__(self, app, *arg, **kw):
		Plan.__init__(self, app, *arg, **kw)

	def behavior(self):
		self.app.setSpeed(self.app.motorSpeedFast)

		self.app.moveMotors(self.app.hipRight, self.app.shoulderRightBegin)
		while (abs(self.app.shoulderMotor.get_pos() - self.app.shoulderRightBegin) > self.app.motorAccuracy):
			yield self.forDuration(0.01)
		while (abs(self.app.hipMotor.get_pos() - self.app.hipRight) > self.app.motorAccuracy):
			yield self.forDuration(0.01)

class RightResetAction(Plan):
	def __init__(self, app, *arg, **kw):
		Plan.__init__(self, app, *arg, **kw)

	def behavior(self):
		self.app.setSpeed(self.app.motorSpeedFast)
		currShoulder = self.app.shoulderMotor.get_pos()

		hipUp = self.app.hipRight * 0.8

		# lift up slightly without moving shoulder
		self.app.moveMotors(hipUp, currShoulder)
		while (abs(self.app.shoulderMotor.get_pos() - currShoulder) > self.app.motorAccuracy):
			yield self.forDuration(0.01)
		while (abs(self.app.hipMotor.get_pos() - hipUp) > self.app.motorAccuracy):
			yield self.forDuration(0.01)

		self.app.moveMotors(hipUp, self.app.shoulderRightBegin)
		while (abs(self.app.shoulderMotor.get_pos() - self.app.shoulderRightBegin) > self.app.motorAccuracy):
			yield self.forDuration(0.01)
		while (abs(self.app.hipMotor.get_pos() - hipUp) > self.app.motorAccuracy):
			yield self.forDuration(0.01)

		self.app.moveMotors(self.app.hipRight, self.app.shoulderRightBegin)
		while (abs(self.app.shoulderMotor.get_pos() - self.app.shoulderRightBegin) > self.app.motorAccuracy):
			yield self.forDuration(0.01)
		while (abs(self.app.hipMotor.get_pos() - self.app.hipRight) > self.app.motorAccuracy):
			yield self.forDuration(0.01)

class LeftResetAction(Plan):
	def __init__(self, app, *arg, **kw):
		Plan.__init__(self, app, *arg, **kw)

	def behavior(self):
		self.app.setSpeed(self.app.motorSpeedFast)
		
		currShoulder = self.app.shoulderMotor.get_pos()
		hipUp = self.app.hipLeft * 0.8

		self.app.moveMotors(hipUp, currShoulder)
		while (abs(self.app.shoulderMotor.get_pos() - currShoulder) > self.app.motorAccuracy):
			yield self.forDuration(0.01)
		while (abs(self.app.hipMotor.get_pos() - hipUp) > self.app.motorAccuracy):
			yield self.forDuration(0.01)

		self.app.moveMotors(hipUp, self.app.shoulderLeftBegin)
		while (abs(self.app.shoulderMotor.get_pos() - self.app.shoulderLeftBegin) > self.app.motorAccuracy):
			yield self.forDuration(0.01)
		while (abs(self.app.hipMotor.get_pos() - hipUp) > self.app.motorAccuracy):
			yield self.forDuration(0.01)

		self.app.moveMotors(self.app.hipLeft, self.app.shoulderLeftBegin)
		while (abs(self.app.shoulderMotor.get_pos() - self.app.shoulderLeftBegin) > self.app.motorAccuracy):
			yield self.forDuration(0.01)
		while (abs(self.app.hipMotor.get_pos() - self.app.hipLeft) > self.app.motorAccuracy):
			yield self.forDuration(0.01)