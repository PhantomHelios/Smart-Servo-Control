import sys, os
import glob
import serial
from servo import Servo
from scservo_sdk import *                 # Uses SCServo SDK library

SCS_MOVING_STATUS_THRESHOLD = 10

BAUDRATE                = 1000000           # SCServo default baudrate : 1000000
PROTOCOL_END            = 1                # SCServo bit end(STS/SMS=0, SCS=1)

ID_RANGE = 100

packetHandler = PacketHandler(PROTOCOL_END)

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
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
    

def get_serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result



def get_servo_motors():
    
    available_ports =  get_serial_ports()
    servo_motors = []

    for port in available_ports:
        
        portHandler = PortHandler(port)
        
        # Open port
        if portHandler.openPort():
            print(f"Succeeded to open the port at {port}")
        else:
            continue

        # Set port baudrate
        if portHandler.setBaudRate(BAUDRATE):
            print("Succeeded to change the baudrate")
        else:
            continue

        # Try to ping the SCServo
        # Get SCServo model number
        for id in range(ID_RANGE+1):
            scs_model_number, scs_comm_result, scs_error = packetHandler.ping(portHandler, id)
            if scs_comm_result == COMM_SUCCESS:
                print("[ID:%03d] ping Succeeded. SCServo model number : %d" % (id, scs_model_number))
                
                servo_motor = Servo(id, port, portHandler, packetHandler)
                
                servo_motors.append(servo_motor)


    return servo_motors


'''
if __name__ == '__main__':
    
    servo_motors = get_servo_motors()
    
    for motor in servo_motors:
        
        goal_position = 300
        
        motor.set_position(goal_position)
        motor.set_moving_speed(200)
        
        while (abs(goal_position - motor.current_position) > SCS_MOVING_STATUS_THRESHOLD):
            
            current_position, current_speed = motor.get_current_position_speed()
            
            print("[ID:%03d] GoalPos:%03d PresPos:%03d PresSpd:%03d" 
              % (motor.id, goal_position, current_position, SCS_TOHOST(current_speed, 15)))
        
        
        motor.reset_torque()

    
    for motor in servo_motors:
        motor.port_handler.closePort()

'''
