# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
def connWlan():
    import wifi
    from wifi import ConexionWiFi
    wf = ConexionWiFi()
    wlan= wf.conectarWifi()
  
def settime():
    import machine
    import utime
    from ntptime import time
    #____________________________________________________________________________________________________________
    # OBTENCIÓN DESDE INTERNET DE NTP - NETWORK TIME PROTOCOL (pool.ntp.org)
    import ntptime
    ntptime.settime()
    #____________________________________________________________________________________________________________
    # SINCRONIZACION DEL RELOJ INTERNO E IMPRESION DE FECHA Y HORA
    from machine import RTC
    (year, month, day, weekday, hour, minute, second, milisecond) = RTC().datetime()                
    #Ejemplo: Zona Horaria GMT corregida para Ecuador: GMT-5 = hour-5
    RTC().init((year, month, day, weekday, hour-5, minute, second, milisecond))
    #rtc=machine.RTC()
    #timestamp=rtc.datetime()
    #fecha="%04d-%02d-%02d %02d:%02d:%02d"%(timestamp[0:3] + timestamp[4:7])
    #print(fecha)
    
connWlan()
settime()
