from machine import sleep, SoftI2C, Pin, I2C, ADC # Importamos el módulo machine
from utime import ticks_diff, ticks_us
from max30102 import MAX30102, MAX30105_PULSE_AMP_MEDIUM
import utime
import time #Importamos el módulo de tiempo time https://docs.python.org/es/3/library/time.html
from ssd1306 import SSD1306_I2C  # Importamos el módulo de funcionamiento de la OLED 
import framebuf # Módulo para visualizar imagenes en pbm

led = Pin(2,Pin.OUT)
class Pulso():
    def __init__ (self):
        self.datos=0
        self.datos2=0
        self.datos3=0
            
    def muestra (self):
        i2c = SoftI2C(sda=Pin(19),  
                      scl=Pin(23),  
                      freq=400000)  
        sensor = MAX30102(i2c=i2c)
        print(sensor)
        if sensor.i2c_address not in i2c.scan():
            print("Sensor no encontrado.")
            return
        
        elif not (sensor.check_part_id()):
            print("ID de dispositivo I2C no correspondiente a MAX30102 o MAX30105.")
            return
        
        else:
            print("Sensor conectado y reconocido.")
        
        print("Configurando el sensor con la configuración predeterminada.", '\n')
        sensor.setup_sensor()
        sensor.set_sample_rate(400)
        sensor.set_fifo_average(8)
        sensor.set_active_leds_amplitude(MAX30105_PULSE_AMP_MEDIUM)
        sleep(1)
        dato3 =(sensor.read_temperature()) # ("Leyendo temperatura en °C.", '\n')
        self.datos3 = dato3
        compute_frequency = True
        print("Iniciando la adquisición de datos de los registros RED e IR...", '\n')
        sleep(1)
        t_start = ticks_us()
        samples_n = 0
        
        while True:
            sensor.check()
            if sensor.available():
                red_reading = sensor.pop_red_from_storage()
                ir_reading = sensor.pop_ir_from_storage() #("Sensor_R",red_reading, "Sensor_IR", ir_reading)
                f_conversion=60/17500
                dato = red_reading*f_conversion
                self.datos=dato #("BPM",dato)
                utime.sleep(2)    
                
                dato2 = ir_reading*f_conversion
                self.datos2=dato2 #("SpO2",dato2)
                utime.sleep(2)                
                
                if compute_frequency:
                    if ticks_diff(ticks_us(), t_start) >= 999999:
                        f_HZ = samples_n
                        samples_n = 0 #("Adquiriendo frecuencia = ", f_HZ)
                        t_start = ticks_us()
                    else:
                        samples_n = samples_n + 1
                        
                        
    def pantalla(self,ritmoCardiaco,concOxigeno,temperatura):
        ancho = 128  # Definimos el ancho de la OLED
        alto = 64    # Definimos el alto de la OLED

        i2c = I2C(0, scl=Pin(22), sda=Pin(21))  #Definimos los pines de la OLED SCL y SDA para ssd1306 y sh1106(otra)
        oled = SSD1306_I2C(ancho, alto, i2c)

        def buscar_icono(ruta):
            dibujo = open(ruta, "rb")  # Abrir en modo lectura de bits https://python-intermedio.readthedocs.io/es/latest/open_function.html
            dibujo.readline() # metodo para ubicarse en la primera linea de los bist
            xy = dibujo.readline() # ubicarnos en la segunda linea
            x = int(xy.split()[0])  # split  devuelve una lista de los elementos de la variable solo 2 elemetos
            y = int(xy.split()[1])
            icono = bytearray(dibujo.read())  # guardar en matriz de bites
            dibujo.close()
            return framebuf.FrameBuffer(icono, x, y, framebuf.MONO_HLSB)  #Utilizamos el metodo MONO_HLSB
        #print(i2c.scan())

        oled.blit(buscar_icono("Logoicn.pbm"), 0, 0) # ruta y sitio de ubicación del directorio
        oled.show()  #mostrar en la oled
        time.sleep(3) # Espera de 3 segundos
        oled.fill(0)
        oled.show()
         
        oled.text('_____________', 5, 0)
        oled.text('Areandina', 5, 15)
        oled.text('Miguel Zabala', 5, 30)
        oled.text('Luis Barragan', 5, 45)
        oled.text('_____________', 5, 60)
        oled.show()
        time.sleep(4)
         
        #oled.fill(1)
        #oled.show()
        #time.sleep(2)
        oled.fill(0)
        oled.show()
        
        oled.text("_____________",10,0)
        oled.text("RC:"+str(ritmoCardiaco),10,10)
        oled.text("CO:"+str(concOxigeno), 10, 20)
        oled.text("TP:"+str(temperatura), 10, 30)
        oled.text("_____________", 10, 40)
        oled.show()
        #time.sleep(4)
