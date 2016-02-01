from joy import *

class WaitForPos(Plan):
	def __init__(self,app,motors,*arg,**kw):
		Plan.__init__(self,app,*arg,**kw)
		self.m = motors
		self.goal = []

	def withGoals( self, *goals ):
		assert len(self.m) == len(goals)
		self.goal = goals
		return self

	def behavior(self):
		assert len(self.m) == len(self.goal)
		bad = -1
		while bad:
			bad = 0
			for m,g in zip(self.m, self.goal):
				if (m.get_pos() -g)>self.app.motorAccuracy:
					bad += 1
			yield self.forDuration(0.05)

class RightStrokeAction(Plan):
	def __init__(self, app, *arg, **kw):
		Plan.__init__(self, app, *arg, **kw)
		
	def behavior(self):
		self.app.setSpeed(self.app.motorSpeedSlow)

		shoulderRightEnd = self.app.shoulderRightEnd * self.app.strokeLength
		self.app.moveMotors(self.app.hipRight, shoulderRightEnd)
		
		yield self.app.waitForPos.withGoals(shoulderRightEnd, self.app.hipRight)

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
			progress("Shoulder %s" % self.app.shoulderMotor.get_pos())
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