from models import *

myBattery = Battery("Li-On Battery", 2000, 500)
myBattery.set_target_power(100)
print(myBattery.get_state())
myBattery.step(1)
print(myBattery.get_state())

mySolar = Solar("Rooftop PV", 300)
mySolar.set_target_power(350)
print(mySolar.get_state())
mySolar.step(1)
print(mySolar.get_state())