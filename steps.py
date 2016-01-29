from joy import *
from state import *

class RightStrokeStep(Plan):
	def __init__(self, app, *arg, **kw):
		Plan.__init__(self, app, *arg, **kw)

	def behavior(self):
		currState = self.app.currState()

		if (currState == State.RIGHT_BEGIN):
			yield self.app.rightStrokeAction
		elif (currState == State.RIGHT_END):
			yield self.app.rightResetAction
			yield self.app.rightStrokeAction
		elif (currState == State.LEFT_BEGIN):
			yield self.app.rightResetAction
			yield self.app.rightStrokeAction
		elif (currState == State.LEFT_END):
			yield self.app.leftToRightTransitionAction
			yield self.app.rightStrokeAction

class LeftStrokeStep(Plan):
	def __init__(self, app, *arg, **kw):
		Plan.__init__(self, app, *arg, **kw)

	def behavior(self):
		currState = self.app.currState()

		if (currState == State.RIGHT_BEGIN):
			yield self.app.leftResetAction
			yield self.app.leftStrokeAction
		elif (currState == State.RIGHT_END):
			yield self.app.rightToLeftTransitionAction
			yield self.app.leftStrokeAction
		elif (currState == State.LEFT_BEGIN):
			yield self.app.leftStrokeAction
		elif (currState == State.LEFT_END):
			yield self.app.leftResetAction
			yield self.app.leftStrokeAction

class ForwardStep(Plan):
	def __init__(self, app, *arg, **kw):
		Plan.__init__(self, app, *arg, **kw)

	def behavior(self):
		currState = self.app.currState()

		if (currState == State.RIGHT_BEGIN or currState == State.LEFT_END):
			yield self.app.rightStrokeStep
			yield self.app.leftStrokeStep
		elif (currState == State.RIGHT_END or currState == State.LEFT_BEGIN):
			yield self.app.leftStrokeStep
			yield self.app.rightStrokeStep