import network
import time
from utime import sleep

class ConexionWiFi():
    def conectarWifi(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if not wlan.isconnected():
            print('Conectando a la red WiFi...')
            wlan.connect("AGDML","%1015Aleribag1402")
            while not wlan.isconnected():
                print("*", end="")
                time.sleep(0.50)
            print("Conexión Exitosa")
        else:
            print("El dispositivo ya esta conectado a la red")