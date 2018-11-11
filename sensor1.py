import paho.mqtt.client as mqtt
import Adafruit_DHT as dht
import RPi.GPIO as gpio
import time


# Informações do Cayene Devices
user = 'e339abe0-e51d-11e8-810f-075d38a26cc9'
password = '1a1df1781b467d043e5fca8f7ea8fe8a81366ccb'
client_id = 'e3950af0-e520-11e8-8cb9-732fc93af22b'
server = 'mqtt.mydevices.com'
port = 1883


# Configurando Relé
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpio.setup(32, gpio.OUT)

def getDHT11():
    vlrDHT11 = dht.read_retry(dht.DHT11, 4)
    print(vlrDHT11[1])
    return vlrDHT11[1]

def liga_relé():
    gpio.output(32, 1)

def desliga_relé():
    gpio.output(32, 0)

status = 3
def mensagens(client, userdata, msg):
    m = msg.topic.split('/')
    p = msg.payload.decode().split(',')
    print('topic: {}'.format(m))
    print('decode: {}'.format(p))
    client.publish(publish_botao, p[1])
    global status
    status = p[1]

publish_0 = 'v1/' + user + '/things/' + client_id + '/data/0'
publish_1 = 'v1/' + user + '/things/' + client_id + '/data/1'
subscribe_botao = 'v1/' + user + '/things/' + client_id + '/cmd/2'
publish_botao = 'v1/' + user + '/things/' + client_id + '/data/2'


# Conectando com o servidor do Cayene
client = mqtt.Client(client_id)
client.username_pw_set(user, password)
client.connect(server, port)
client.on_message = mensagens
client.subscribe(subscribe_botao)

client.loop_start()

i = 1
while True:
    client.publish(publish_0, i)
    client.publish(publish_1, getDHT11()) # valor do temperatura DHT11
    print('status: ', status)
    if status == '1' and getDHT11() < 30:
        liga_relé()
    else:
        desliga_relé()
    time.sleep(3)
    i += 1
