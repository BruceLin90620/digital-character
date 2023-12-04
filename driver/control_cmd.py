from DXL_motor_control import DXL_Conmunication
import time
import sys, tty, termios
import traceback
import json 

# Keyboard interrupt 
# fd = sys.stdin.fileno()
# old_settings = termios.tcgetattr(fd)
# def getch():
#     try:
#         tty.setraw(sys.stdin.fileno())
#         ch = sys.stdin.read(1)
#     finally:
#         termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
#     return ch


# main control command
DEVICE_NAME = "/dev/ttyUSB0"
B_RATE      = 57600
LED_ADDR_LEN = (65,1)
LED_ON = 1
LED_OFF = 0


class ControlCmd:
    def __init__(self):

        self.record_path = 'output.txt'

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
        
        # self.motor_list = [motor1]
        
        self.motor_position = { "motor0":0, "motor1":0, "motor2":0, "motor3":0, "motor4":0,
                                "motor5":0, "motor6":0, "motor7":0, "motor8":0, "motor9":0}
        
        # self.motor_position = {"motor1":0}
        
        self.dynamixel.rebootAllMotor()
        self.dynamixel.updateMotorData()

    def enable_all_motor(self):
        for motor in self.motor_list:
            motor.enableMotor()

    def disable_all_motor(self):
        for motor in self.motor_list:
            motor.disableMotor()
        self.dynamixel.closeHandler()

    def read_motor_data(self):
        for motor in self.motor_list:
            position, _ = motor.directReadData(132, 4)
            # print("motor id:", motor.DXL_ID, "motor position:", position)
            # while abs(position) > 4095:
            # print("motor position:", position)
            if (position) > 4294000000:
                # print("motor position:", position)
                position = position - 4294967295 
                # print("motor position:", position)
            elif (position) > 4095:
                # print("motor position:", position)
                position = position - 4095
                # print("motor position:", position)

            elif (position) < -4095:
                position = position + 4095
            # print("motor position:", position)
            #     position = position - (position/abs(position)) * 4095

            position = int(position*360/4095)
            if position > 180:
                position -= 360
            self.motor_position[motor.name] = position

        return self.motor_position
    
    def motor_led_control(self, state = LED_OFF):
        for motor in self.motor_list:
            led_on = motor.directWriteData(state, *LED_ADDR_LEN)
            
        return led_on
    
    def start_record_action_points(self):
        print("start record the action points....")
        with open(self.record_path, 'w') as f:

            while True:
                print("Press any key to record the action points! (or press ESC to finish recording!)")
                if getch() == chr(0x1b):
                    break
                all_servo_position = controlcmd.read_motor_data()
                print("recording:", all_servo_position)
                f.write(json.dumps(all_servo_position)+'\n')
        print("finish recording!")


    # def stop_record_motor_data(self):
    #     pass

    def replay_motor_data(self):
        for motor in self.motor_list:
            motor.switchMode('position')

        self.enable_all_motor()

        with open(self.record_path) as f: 
            one_action_point = f.readline()
            while one_action_point:
                
                one_action_point = json.loads(one_action_point) 
                print(one_action_point)

                for motor in self.motor_list:
                    motor.setPosition(one_action_point[motor.name])

                time.sleep(1)
                one_action_point = f.readline()





if __name__ == "__main__":
    controlcmd = ControlCmd()

    # while True:
    #     print("Press any key to continue! (or press ESC to quit!)")
    #     if getch() == chr(0x1b):
    #         break
    #     all_servo_position = controlcmd.read_motor_data()
    #     print(all_servo_position)
    # controlcmd.disable_all_motor()

    command_dict = {
        "record":controlcmd.start_record_action_points,
        "replay":controlcmd.replay_motor_data,
        "disable":controlcmd.disable_all_motor,

    }


    while True:
        try:
            cmd = input("CMD : ")
            if cmd in command_dict:
                command_dict[cmd]()
            elif cmd == "exit":
                break
        except Exception as e:
            traceback.print_exc()
            break
