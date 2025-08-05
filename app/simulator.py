from models import *
import csv, os, time, math

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

solar = Solar("Solar A", 3000)
battery = Battery("Battery A", 2000, 500)
sim = Simulator([solar, battery], controller=basic_controller)
if os.path.exists('../bin/history.csv'):
    os.remove('../bin/history.csv')
else:
    os.mkdir('../bin')
history_file = os.path.join('../bin',f'history.csv')

with open(history_file, 'w', newline = '') as f:
    csv_writer = csv.writer(f)
    headers = ["time_hr", "der_name", "actual_power_kw", "target_power_kw", "soc_percent"]
    csv_writer.writerow(headers)
    for _ in range(24):
        sim.step(1)
        state = sim.get_state()
        for der in state["ders"]:
            row = [
                state["time_hr"],
                der.get("Name", ""),
                der.get("Current Actual Power", ""), # only Solar will have this
                der.get("Current Target Power", ""),
                f"{der.get('State of Charge', ''):.2f}" if der.get("State of Charge") is not None else ""  # only Battery will have this
            ]
            csv_writer.writerow(row)