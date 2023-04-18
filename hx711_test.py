import time
from machine import freq
#freq(160000000)

from hx711 import HX711

driver = HX711(d_out=0, pd_sck=1)
x = - 295
divide = 442.4
w = 0
repeatNum = 5

while True:
    w = 0
    for i in range(repeatNum):
        w = w + driver.read()
    average = w/repeatNum
    weight = round((average - (95020 + x*divide))/divide)
    print(weight)
    time.sleep_ms(1000)
    
driver.power_off()