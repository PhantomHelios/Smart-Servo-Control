from scservo_sdk import *                 # Uses SCServo SDK library

# Control table address
ADDR_SCS_TORQUE_ENABLE     = 40
ADDR_SCS_GOAL_POSITION     = 42
ADDR_SCS_GOAL_SPEED        = 46
ADDR_SCS_PRESENT_POSITION  = 56

MIN_GOAL_POSITION = 20
MAX_GOAL_POSITION = 1000

MIN_SPEED = 0
MAX_SPEED = 2000


class Servo:
    def __init__(self, id, port, port_handler, packet_handler):
        self.port = port
        self.id = id
        self.port_handler = port_handler
        self.packet_handler = packet_handler
        self.current_position = 500
        self.current_speed = 0
    
    
    def get_current_position_speed(self):
        scs_present_position_speed, scs_comm_result, scs_error = self.packet_handler.read4ByteTxRx(self.port_handler, self.id, ADDR_SCS_PRESENT_POSITION)
        if scs_comm_result != COMM_SUCCESS:
            print(self.packet_handler.getTxRxResult(scs_comm_result))
        elif scs_error != 0:
            print(self.packet_handler.getRxPacketError(scs_error))
                      
        self.current_position = SCS_LOWORD(scs_present_position_speed)
        self.current_speed = SCS_HIWORD(scs_present_position_speed)
        
        return self.current_position, self.current_speed
    
    
    def set_position(self, goal_position):
        
        if not MIN_GOAL_POSITION <= goal_position <= MAX_GOAL_POSITION:
            return
        
        scs_comm_result, scs_error = self.packet_handler.write2ByteTxRx(self.port_handler, self.id, ADDR_SCS_GOAL_POSITION, goal_position)
        if scs_comm_result != COMM_SUCCESS:
            print("%s" % self.packet_handler.getTxRxResult(scs_comm_result))
        elif scs_error != 0:
            print("%s" % self.packet_handler.getRxPacketError(scs_error))
    
    
    def set_moving_speed(self, speed):
        scs_comm_result, scs_error = self.packet_handler.write2ByteTxRx(self.port_handler, self.id, ADDR_SCS_GOAL_SPEED, speed)
        if scs_comm_result != COMM_SUCCESS:
            print("%s" % self.packet_handler.getTxRxResult(scs_comm_result))
        elif scs_error != 0:
            print("%s" % self.packet_handler.getRxPacketError(scs_error))
    
    
    def reset_torque(self):
        scs_comm_result, scs_error = self.packet_handler.write1ByteTxRx(self.port_handler, self.id, ADDR_SCS_TORQUE_ENABLE, 0)
        if scs_comm_result != COMM_SUCCESS:
            print("%s" % self.packetscs_comm_result, scs_error = self.packet_handler.getTxRxResult(scs_comm_result))
        elif scs_error != 0:
            print("%s" % self.packetscs_comm_result, scs_error = self.packet_handler.getRxPacketError(scs_error))