import urequests
import json
#import ussl as ssl 
import time
from utime import sleep

def conn(idPaciente,ritmoCardiaco,concOxigeno,temperatura,fecha):
    print("Iniciando el modulo....")
    #url = "http://192.168.50.24/eps/api.php"
    url = 'http://201.244.164.221:8888/api.php'

    payload = {
      "idPaciente": idPaciente,
      "RitmoCardiaco": ritmoCardiaco,
      "ConcOxigeno": concOxigeno,
      "Temperatura": temperatura,
      "fechaLectura": fecha
    }
    data = (json.dumps(payload)).encode()
    headers = {'X-AIO-Key': 'xxxxxxxxxxxxxxxxxxx',
                'Content-Type': 'application/json'}

    print("Enviando petición HTTPS...",end="")
    #response=urequests.get(url)
    response = urequests.post(url, data=data, headers=headers)
    #print(r.status_code)
    print(response.text);
    #sleep(5)
