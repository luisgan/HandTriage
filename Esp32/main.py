import api
from api import conn
import pulsometro
from pulsometro import Pulso
import machine
from machine import Timer
import ssd1306
import time
idPaciente=2

rtc=machine.RTC()
timestamp=rtc.datetime()
fecha="%04d-%02d-%02d %02d:%02d:%02d"%(timestamp[0:3] + timestamp[4:7])

temporiza = Timer(0)
def desborde (Timer):
    print("_"*45)
    if oledC.datos <= 30 and oledC.datos2 >= 31 or oledC.datos3 >= 10:
        print("BPM={:02} p SpO2={:02}%  Temp={:02} °C ".format(oledC.datos, oledC.datos2, oledC.datos3))
        print("_"*45)
        oledC.pantalla(oledC.datos,oledC.datos2,oledC.datos3)
        api.conn(idPaciente,oledC.datos,oledC.datos2,oledC.datos3,fecha)

        
#__________________________________________________________________
temporiza.init(period=10000,mode=Timer.PERIODIC,callback=desborde)
#_________________________________________________________________
oledC = Pulso()
oledC.muestra()
