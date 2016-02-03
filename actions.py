from joy import *

class RightStrokeAction(Plan):
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
	def __init__(self, app, *arg, **kw):
		Plan.__init__(self, app, *arg, **kw)

	def behavior(self):
		self.app.setSpeed(self.app.motorSpeedFast)
		currShoulder = self.app.shoulderMotor.get_pos()

		hipUp = self.app.hipRight * 0.0

		# lift up slightly without moving shoulder
		self.app.moveMotors(hipUp, currShoulder)
		while (abs(self.app.shoulderMotor.get_pos() - currShoulder) > self.app.motorAccuracy):
			yield self.forDuration(0.01)
		while (abs(self.app.hipMotor.get_pos() - hipUp) > self.app.motorAccuracy):
			yield self.forDuration(0.01)

		shoulderRightBegin = self.app.shoulderRightBegin * self.app.strokeLength

		self.app.moveMotors(hipUp, shoulderRightBegin)
		while (abs(self.app.shoulderMotor.get_pos() - shoulderRightBegin) > self.app.motorAccuracy):
			yield self.forDuration(0.01)
		while (abs(self.app.hipMotor.get_pos() - hipUp) > self.app.motorAccuracy):
			yield self.forDuration(0.01)

		self.app.moveMotors(self.app.hipRight, shoulderRightBegin)
		while (abs(self.app.shoulderMotor.get_pos() - shoulderRightBegin) > self.app.motorAccuracy):
			yield self.forDuration(0.01)
		while (abs(self.app.hipMotor.get_pos() - self.app.hipRight) > self.app.motorAccuracy):
			yield self.forDuration(0.01)

class LeftResetAction(Plan):
	def __init__(self, app, *arg, **kw):
		Plan.__init__(self, app, *arg, **kw)

	def behavior(self):
		self.app.setSpeed(self.app.motorSpeedFast)
		
		currShoulder = self.app.shoulderMotor.get_pos()
		hipUp = self.app.hipLeft * 0.0

		self.app.moveMotors(hipUp, currShoulder)
		while (abs(self.app.shoulderMotor.get_pos() - currShoulder) > self.app.motorAccuracy):
			yield self.forDuration(0.01)
		while (abs(self.app.hipMotor.get_pos() - hipUp) > self.app.motorAccuracy):
			yield self.forDuration(0.01)

		shoulderLeftBegin = self.app.shoulderLeftBegin * self.app.strokeLength

		self.app.moveMotors(hipUp, shoulderLeftBegin)
		while (abs(self.app.shoulderMotor.get_pos() - shoulderLeftBegin) > self.app.motorAccuracy):
			yield self.forDuration(0.01)
		while (abs(self.app.hipMotor.get_pos() - hipUp) > self.app.motorAccuracy):
			yield self.forDuration(0.01)

		self.app.moveMotors(self.app.hipLeft, shoulderLeftBegin)
		while (abs(self.app.shoulderMotor.get_pos() - shoulderLeftBegin) > self.app.motorAccuracy):
			yield self.forDuration(0.01)
		while (abs(self.app.hipMotor.get_pos() - self.app.hipLeft) > self.app.motorAccuracy):
			yield self.forDuration(0.01)