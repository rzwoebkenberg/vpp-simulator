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

class Solar(DER):
    def __init__(self, name, max_power_kw):
        self.name = name
        self.max_power_kw = max_power_kw
        self.target_power_kw = 0
        self.actual_power_kw = 0

    def update_irradiance(self, irradiance: float):
        self.max_power_kw = self.max_power_kw * irradiance
        
    def set_target_power(self, target_power_kw):
        #RZW add logging when clipping and improve logic
        if target_power_kw < 0:
            self.target_power_kw = 0
        elif target_power_kw > self.max_power_kw:
            self.target_power_kw = self.max_power_kw
        else:
            self.target_power_kw = target_power_kw

    def step(self, dt_hr):
        self.actual_power_kw = min(self.target_power_kw, self.max_power_kw)

    def get_state(self) -> dict:
        state = {
            "Name": self.name,
            "Current Target Power": self.target_power_kw,
            "Current Actual Power": self.actual_power_kw
        }
        return state