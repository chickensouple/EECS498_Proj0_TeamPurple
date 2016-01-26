from joy import *

# parameters
hipMotorString = "Nx0C"
shoulderMotorString = "Nx0B"

motorAccuracy = 200

rightStrokeHipPrepare = 3000
rightStrokeShoulderPrepare = 5400
rightStrokeShoulderTarget = -5400

leftStrokeHipPrepare = -3000
leftStrokeShoulderPrepare = -5400
leftStrokeShoulderTarget = 5400

def moveMotors(hipMotor, shoulderMotor, hipMotorPos, shoulderMotorPos, motorAccuracy):
	hipMotor.set_pos(hipMotorPos)
	shoulderMotor.set_pos(shoulderMotorPos)
	while (abs(hipMotor.get_pos() - hipMotorPos) > motorAccuracy):
		continue
	while (abs(shoulderMotor.get_pos() - shoulderMotorPos) > motorAccuracy):
		continue

def rightStroke(hipMotor, shoulderMotor):
	# preparing for right stroke
	moveMotors(hipMotor, shoulderMotor, rightStrokeHipPrepare, rightStrokeShoulderPrepare, motorAccuracy)
	# actually stroke
	moveMotors(hipMotor, shoulderMotor, rightStrokeHipPrepare, rightStrokeShoulderTarget, motorAccuracy)

def leftStroke(hipMotor, shoulderMotor):
	# preparing for left stroke
	moveMotors(hipMotor, shoulderMotor, leftStrokeHipPrepare, leftStrokeShoulderPrepare, motorAccuracy)
	# actually stroke
	moveMotors(hipMotor, shoulderMotor, leftStrokeHipPrepare, leftStrokeShoulderTarget, motorAccuracy)

def neutralPosition(hipMotor, shoulderMotor):
	moveMotors(hipMotor, shoulderMotor, 0, 0, motorAccuracy)


class KayakApp(JoyApp):
	def __init__(self, hipMotor, shoulderMotor, *arg, **kw):
		JoyApp.__init__(self, *arg, **kw)
		self.hipMotorString = hipMotorString
		self.shoulderMotorString = shoulderMotorString
		exec("self.hipMotor = self.robot.at." + hipMotorString)
		exec("self.shoulderMotor = self.robot.at." + shoulderMotorString)

	def onStart(self):
		pass

	def onEvent(self, evt):
		if evt.type == TIMEREVENT:
			pass

		if evt.type != KEYDOWN:
			return

		if evt.key == K_w:
			print "w"

			print "hip: " + str(self.hipMotor.get_pos())
			print "shoulder: " + str(self.shoulderMotor.get_pos())
		elif evt.key == K_d:
			print "Start right stroke"
			rightStroke(self.hipMotor, self.shoulderMotor)
			print "End right stroke"
		elif evt.key == K_a:
			print "Start left stroke"
			leftStroke(self.hipMotor, self.shoulderMotor)
			print "End left stroke"
		elif evt.key == K_s:
			print "Start neutral position"
			neutralPosition(self.hipMotor, self.shoulderMotor)
			print "End neutral position"
robot = {"count": 2}
scr = {}

app = KayakApp(hipMotorString, shoulderMotorString, robot=robot, scr=scr)
app.run()

