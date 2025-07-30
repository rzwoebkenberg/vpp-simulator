from abc import ABC, abstractmethod

class DER(ABC):
    @abstractmethod
    def step(self, dt_hr: float):
        pass

    @abstractmethod
    def get_state(self) -> dict:
        pass

class Battery(DER):
    def __init__(self, name, capacity_kwh, max_power_kw):
        self.name = name
        self.capacity_kwh = capacity_kwh
        self.max_power_kw = max_power_kw
        self.soc = 0.5 # 50%
        self.target_power_kw = 0 # positive values for charging, negative values for discharging. common vernacular for power simulation

    def set_target_power(self, target_power_kw):
        #RZW add logging when clipping and improve logic
        if target_power_kw < -self.max_power_kw:
            self.target_power_kw = -self.max_power_kw
        elif target_power_kw > self.max_power_kw:
            self.target_power_kw = self.max_power_kw
        else:
            self.target_power_kw = target_power_kw
    
    def step(self, dt_hr):
        dt_soc = (self.target_power_kw * dt_hr) / self.capacity_kwh
        #RZW add logging when clipping and improve logic
        if self.soc + dt_soc < 0:
            self.soc = 0
        elif self.soc + dt_soc > 1:
            self.soc = 1
        else:
            self.soc += dt_soc

    def get_state(self) -> dict:
        state = {
            "Name": self.name,
            "State of Charge": self.soc,
            "Current Target Power": self.target_power_kw
        }
        return state
        
myBattery = Battery("Ryan's Battery", 2000, 500, -500)
myBattery.set_target_power(100)
while myBattery.get_state()["State of Charge"] < 1:
    myBattery.step(1)
    state = myBattery.get_state()
    print(f"The current state of charge in {state["Name"]} is: {state["State of Charge"]:.1%}") 
    print(f"The current target power in {state["Name"]} is: {state["Current Target Power"]} kW") 