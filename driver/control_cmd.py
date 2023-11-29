from driver.DXL_motor_control import DXL_Conmunication

DEVICE_NAME = "/dev/ttyUSB0"
B_RATE      = 57600
   
class ControlCmd:
    def __init__(self):
        self.dynamixel = DXL_Conmunication(DEVICE_NAME, B_RATE)
        self.dynamixel.activateDXLConnection()
        motor0 = self.dynamixel.createMotor('motor0', motor_number=0)
        motor1 = self.dynamixel.createMotor('motor1', motor_number=1)
        motor2 = self.dynamixel.createMotor('motor2', motor_number=2)
        motor3 = self.dynamixel.createMotor('motor3', motor_number=3)
        motor4 = self.dynamixel.createMotor('motor4', motor_number=4)
        motor5 = self.dynamixel.createMotor('motor5', motor_number=5)
        motor6 = self.dynamixel.createMotor('motor6', motor_number=6)
        motor7 = self.dynamixel.createMotor('motor7', motor_number=7)
        motor8 = self.dynamixel.createMotor('motor8', motor_number=8)
        motor9 = self.dynamixel.createMotor('motor9', motor_number=9)

        self.motor_list = [ motor0, motor1, motor2, motor3, motor4, 
                            motor5, motor6, motor7, motor8, motor9]
        
        self.motor_position = { "motor0":0, "motor1":0, "motor2":0, "motor3":0, "motor4":0,
                                "motor5":0, "motor6":0, "motor7":0, "motor8":0, "motor9":0}
        
        self.dynamixel.rebootAllMotor()
        self.dynamixel.updateMotorData()

    def disable_all_motor(self):
        for motor in self.motor_list:
            motor.disableMotor()
        self.dynamixel.closeHandler()

    def read_motor_data(self):
        for motor in self.motor_list:
            position, ret = motor.directReadData(132, 4)
            print("motor id:", motor.DXL_ID, "motor position:", position)
            while abs(position) > 4095:
                position = position - (position/abs(position)) * 4095
            # if position > 4095:
            #     print(position, "+")
            #     position -= 
            # elif position < -4095:
            #     print(position, "-")
            #     position += 2147483647
            self.motor_position[motor.name] = int(position)
            print("motor id:", motor.DXL_ID, "motor position:", position)
        return self.motor_position


if __name__ == "__main__":
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    
    controlcmd = ControlCmd()

    while True:
        print("Press any key to continue! (or press ESC to quit!)")
        if getch() == chr(0x1b):
            break
        all_servo_position = controlcmd.read_motor_data()
        print(all_servo_position)
    controlcmd.disable_all_motor()
