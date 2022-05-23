import tkinter as tk
import tkinter.messagebox
from tkinter import *

from scservo_sdk import *
from scan_motors import *
from servo import *

class GUI:
    def __init__(self, motors):
        self.motors = motors

        numberOfMotors = len(motors)

        self.root = tk.Tk()

        if numberOfMotors == 0:
            tkinter.messagebox.showinfo(
                "Error! ", "No Servo Motors detected! Exiting...")
            self.on_exit()
            exit()

        self.HEIGHT = numberOfMotors * 200 + 50
        self.WIDTH = 1000

        size = f"{self.WIDTH}x{self.HEIGHT}"

        self.root.geometry(size)
        self.root.resizable(width=False, height=False)

        self.root.title('SERVO MOTOR CONTROLLED BY PYTHON')
        self.root.configure(bg="#008f96")

        button = tk.Button(self.root, text="Quit", width=6,
                           height=3, command=self.on_exit)
        button.place(x=945, y=self.HEIGHT - 60)

        self.positionLabels = []
        self.positionSliders = []
        self.setPositionButtons = []

        self.speedLabels = []
        self.speedSliders = []
        self.setSpeedButtons = []

        for index in range(numberOfMotors):

            position, speed = motors[index].get_current_position_speed()

            title = tk.Label(self.root, text=str(motors[index].id), bg="#008f96")
            title.config(font=("Courier", 44))
            title.place(x=80, y=200*index+60)

            self.positionLabels.append(
                tk.Label(self.root, text="POSITION:", bg="#008f96"))
            self.positionLabels[index].place(x=200, y=200*index+50)

            self.positionSliders.append(Scale(self.root, variable=IntVar(value=position), from_=MIN_GOAL_POSITION, to=MAX_GOAL_POSITION,
                                              orient=HORIZONTAL, length=550))
            self.positionSliders[index].place(x=280, y=200*index+33)

            self.createPositionButton(index)

            self.speedLabels.append(
                tk.Label(self.root, text="SPEED:", bg="#008f96"))
            self.speedLabels[index].place(x=200, y=200*index+120)

            self.speedSliders.append(Scale(self.root, variable=IntVar(value=speed), from_=MIN_SPEED, to=MAX_SPEED,
                                           orient=HORIZONTAL, length=550))
            self.speedSliders[index].place(x=280, y=200*index+103)

            self.createSpeedButton(index)

        self.root.mainloop()

    def on_exit(self):
        self.root.destroy()

    def createSpeedButton(self, index):
        self.setSpeedButtons.append(tk.Button(
            self.root,
            text="SET",
            command=lambda: self.setSpeed(index),
            width=10,
            height=2,
            bg="#979996",
            fg="black",))
        self.setSpeedButtons[index].place(x=880, y=200*index+104)

    def createPositionButton(self, index):
        self.setPositionButtons.append(tk.Button(
            self.root,
            text="SET",
            command=lambda: self.setPosition(index),
            width=10,
            height=2,
            bg="#979996",
            fg="black",))
        self.setPositionButtons[index].place(x=880, y=200*index+34)

    def setPosition(self, index):
        goalPosition = self.positionSliders[index].get()
        self.motors[index].set_position(goalPosition)

    def setSpeed(self, index):
        goalSpeed = self.speedSliders[index].get()
        self.motors[index].set_moving_speed(goalSpeed)




if __name__ == '__main__':

    servo_motors = get_servo_motors()

    GUI(servo_motors)

    for motor in servo_motors:
        motor.reset_torque()
