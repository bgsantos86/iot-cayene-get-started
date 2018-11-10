import paho.mqtt.client as mqtt
import Adafruit_DHT as dht
import RPi.GPIO as gpio
import time

def getDHT11():
    umid, temp = dht.read_retry(dht.DHT11, 4)
    print('Temp: {0:.1f}      Umid: {1:.1f}'.format(temp, umid))
    client.publish(publish_1, temp)

def liga_relé():
    gpio.output(32, 1)

def desliga_relé():
    gpio.output(32, 0)

def mensagens(client, userdatan ,msg):
    m = msg.topic.split('/')
    p = msg.payload.decode().split(',')
    print(m)
    print(p)
    client.publish(publish_botao, p[1])
    if p[1] == '1':
        liga_relé()
    else:
        desliga_relé()

# Informações do Cayene Devices
user = 'e339abe0-e51d-11e8-810f-075d38a26cc9'
password = '1a1df1781b467d043e5fca8f7ea8fe8a81366ccb'
client_id = 'e3950af0-e520-11e8-8cb9-732fc93af22b'
server = 'mqtt.mydevices.com'
port = 1883

publish_0 = 'v1/' + user + '/things/' + client_id + '/data/0'
publish_1 = 'v1/' + user + '/things/' + client_id + '/data/1'
subscribe_botao = 'v1/' + user + '/things/' + client_id + '/cmd/2'
publish_botao = 'v1/' + user + '/things/' + client_id + '/data/2'

# Configurando Relé
gpio.setmode(gpio.BOARD)
gpio.setup(32, gpio.OUT)

# Conecatando com o servidor do Cayene
client = mqtt.Client(client_id)
client.username_pw_set(user, password)
client.connect(server, port)
client.on_message = mensagens
client.subscribe(subscribe_botao)

client.loop_start()

i = 1
while True:
    client.publish(publish_0, i)
    getDHT11()
    time.sleep(2)
    i += 1