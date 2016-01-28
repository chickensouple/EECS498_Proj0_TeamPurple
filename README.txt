RUNNING THE PROGRAM:
Type "make" in your terminal
While running
Type "x" to get current position of motors and current state
Type "w" to do two strokes to go forward (hopefully without turning)
Type "s" to go to a netural position
Type "a" to left stroke (turns you to the right)
Type "d" to right stroke (turns you to the left)


MODIFYING PARAMETERS
there are parameters at the top of the file

# class PaddleMotion(Plan):
#     def moveMotors(self, hipMotorPos, shoulderMotorPos):
# 	   self.app.robot.hipMotor.set_pos(hipMotorPos)
# 	   self.app.robot.shoulderMotor.set_pos(shoulderMotorPos)

# 	def behavior(self):
# 		T0 = self.app.now
# 		self.moveMotors(0,3000)
# 		while abs(self.app.robot.hipMotor.get_pos()-3000)>200:
# 			self.moveMotors(0,30 * (self.app.now-T0))
# 			yield self.forDuration(0.05)

#         self.moveMotors(3000,3000)
# 		yield self.forDuration(0.1)
#         self.moveMotors(0,3000)
# 		yield self.forDuration(0.1)


