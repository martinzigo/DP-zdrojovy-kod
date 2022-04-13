import Adafruit_DHT
import subprocess
sensor = Adafruit_DHT.DHT11
pin = 4

while True:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    temperature = '{0:0.2f}'.format(temperature)
    humidity = '{0:0.2f}'.format(humidity)
    reading = "{"+"\"temperature\":{0},\"humidity\":{1}".format(temperature, humidity)+"}"
    bashCommand = "mosquitto_pub -V 5 -h 192.168.137.83 -t meranie --cafile <certifikat CA> --cert <certifikát klienta> --key <kľúč klienta> -p 8883 -d -m {0}".format(reading)
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)

