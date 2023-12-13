import math
from tkinter import *

FPS = 60
g_force = 9.8


class Ball():
    """Класс задает как будут выглядеть шары, где они будут находиться и как себя вести"""
    def __init__(self):
        self.color = 'silver'
        self.radius = 100
        self.x1 = 280
        self.y1 = 500
        self.x2 = 480
        self.y2 = 500
        self.x3 = 680
        self.y3 = 500
        self.x4 = 880
        self.y4 = 500
        self.x5 = 1080
        self.y5 = 500
        self.image1 = None
        self.image2 = None
        self.image3 = None
        self.image4 = None
        self.image5 = None

    def draw(self):
        global canvas
        self.image1 = canvas.create_oval(self.x1 - self.radius, self.y1 - self.radius, self.x1 + self.radius,
                                         self.y1 + self.radius, fill=self.color)
        self.image2 = canvas.create_oval(self.x2 - self.radius, self.y2 - self.radius, self.x2 + self.radius,
                                         self.y2 + self.radius, fill=self.color)
        self.image3 = canvas.create_oval(self.x3 - self.radius, self.y3 - self.radius, self.x3 + self.radius,
                                         self.y3 + self.radius, fill=self.color)
        self.image4 = canvas.create_oval(self.x4 - self.radius, self.y4 - self.radius, self.x4 + self.radius,
                                         self.y4 + self.radius, fill=self.color)
        self.image5 = canvas.create_oval(self.x5 - self.radius, self.y5 - self.radius, self.x5 + self.radius,
                                         self.y5 + self.radius, fill=self.color)


class Strings():
    """Класс отрисовывает нити, которые соединяют подвес и шары"""
    def __init__(self):
        obj = Ball()
        self.color = 'black'
        self.x_ending1 = obj.x1   # это значение - x координата нижней части нити
        self.y_ending1 = obj.y1   # это значение - y координата нижней части нити
        self.x_begining1 = 280   # это значение - x координата верхней части нити
        self.y_begining1 = 150   # это значение - y координата верхней части нити
        self.x_ending2 = obj.x2
        self.y_ending2 = obj.y2
        self.x_begining2 = 480
        self.y_begining2 = 150
        self.x_ending3 = obj.x3
        self.y_ending3 = obj.y3
        self.x_begining3 = 680
        self.y_begining3 = 150
        self.x_ending4 = obj.x4
        self.y_ending4 = obj.y4
        self.x_begining4 = 880
        self.y_begining4 = 150
        self.x_ending5 = obj.x5
        self.y_ending5 = obj.y5
        self.x_begining5 = 1080
        self.y_begining5 = 150

    def draw(self):
        global canvas
        canvas.create_polygon((self.x_begining1 - 5, self.y_begining1), (self.x_begining1 + 5, self.y_begining1),
                              (self.x_ending1 + 5, self.y_ending1), (self.x_ending1 - 5, self.y_ending1),
                              fill=self.color)


root = Tk()

root['bg'] = 'black'
root.title('Newton Cradle')
root.geometry('1400x750')
root.resizable(width=False, height=False)

canvas = Canvas(root, width=1400, height=650)
canvas.pack(side=TOP)

frame = Frame(root, bg='grey', width=1400, height=100)
frame.pack(side=BOTTOM)

strings = Strings().draw()

balls = Ball().draw()

canvas.create_rectangle(180, 50, 1180, 150, fill='black')   # Отрисовка подвеса

root.mainloop()
