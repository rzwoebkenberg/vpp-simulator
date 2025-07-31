from models import *

def basic_controller(time_hr, ders):
    for der in ders:
        if isinstance(der, Battery):
            der.set_target_power(100)
        elif isinstance(der, Solar):
            der.set_target_power(300)

class Simulator:
    def __init__(self, der_list, controller=None):
        self.ders = der_list
        self.controller = controller # callable that takes current time and state
        self.time_hr = 0
        self.history = []

    def get_state(self):
        state = {
            "time_hr": self.time_hr,
            "ders": [der.get_state() for der in self.ders]
        }
        return state

    def step(self, dt_hr):
        if self.controller:
            self.controller(self.time_hr, self.ders)

        for der in self.ders:
            der.step(dt_hr)

        self.time_hr += dt_hr
        self.history.append(self.get_state())
        
solar = Solar("Solar A", 300)
battery = Battery("Battery A", 2000, 500)
sim = Simulator([solar, battery], controller=basic_controller)
for _ in range(24):
    sim.step(1)
    print(sim.get_state())