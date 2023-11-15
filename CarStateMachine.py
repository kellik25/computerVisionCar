import time
from hub import port
import motor
import uasyncio as asyncio
from BLELibrary2 import Listen


class Car():
    def __init__(self):
        self.message = "Stop"
        self.states = [1,2,3,4]
        self.motors =[port.A, port.B]
        self.state = 1
        self.tasks = [self.task1(),self.task2(),self.task3(), self.task4(),self.task5(),]
        try:   
            self.p = Listen('Fred', verbose = True)
            if self.p.connect_up():
                print('p connected')
                time.sleep(2)
        except Exception as e:
            print(e)
    async def task1(self):
        #stop
        while True:
            if self.state == 1:
                for m in self.motors: 
                    motor.stop(m)
            await asyncio.sleep(0.1)
    async def task2(self):
        #forward
        while True:
            if self.state == 2:
                pwm = 5000  # from -10,000 to 10,000
                motor.set_duty_cycle(port.A,pwm)
                motor.set_duty_cycle(port.B,-pwm)
            await asyncio.sleep(0.1)
    async def task3(self):
        #turn left
        while True:
            if self.state == 3:
                pwm = 5000
                motor.set_duty_cycle(port.A,pwm)
                motor.set_duty_cycle(port.B,0)
            await asyncio.sleep(0.1)
    async def task4(self):
        #turn right
        while True:
            if self.state == 4:
                pwm = 5000
                motor.set_duty_cycle(port.A,0)
                motor.set_duty_cycle(port.B,-pwm)
            await asyncio.sleep(0.1)
    async def task5(self):
        while self.p.is_connected:
            if self.p.is_any:
                self.message=self.p.read()
            print(self.message)
            if self.message == "Forward":
                self.state = 2
            elif self.message == "Left":
                self.state = 3
            elif self.message == "Right":
                self.state = 4
            elif self.message == "Stop":
                self.state = 1
            else:
                self.state = 1
            print(self.state)
            await asyncio.sleep(0.1)
    async def run(self, duration):
        for t in self.tasks:
            asyncio.create_task(t)
        await asyncio.sleep(duration)
def main():
    try:
        car = Car()
        asyncio.run(car.run(60))
    except Exception as e:
        print(e)
    finally:
        print('resetting')
        #stop motors
main()
        
            
        
        
    
