from joy import *
from state import *
import timeit

# This functions in this file build off the lower level motions defined in actions.py
# It will chain together appropriate state transitions to form a higher level motion such as "Do an entire right stroke"
# See the "High Level Motions" section in the Code Documentation for more details

class RightStrokeStep(Plan):
	""" Does the RightStrokeStep as described in the Code Documentation """
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
	""" Does the LeftStrokeStep as described in the Code Documentation """
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
	""" Does the ForwardStrokeStep as described in the Code Documentation """
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