import logging
import eventlet
import json
from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap

eventlet.monkey_patch()

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = ''
app.config['MQTT_CLEAN_SESSION'] = True
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_LAST_WILL_QOS'] = 0

# Parametre pre základnú konfiguráciu
app.config['MQTT_BROKER_PORT'] = 1883

# Parametre pre používateľské meno a heslo
#app.config['MQTT_BROKER_PORT'] = 1883
#app.config['MQTT_USERNAME'] = ''                      
#app.config['MQTT_PASSWORD'] = ''                   

# Parametre pre TLS certifikáty

#app.config['MQTT_BROKER_PORT'] = 8883
#app.config['MQTT_TLS_ENABLED'] = True
#app.config['MQTT_TLS_CA_CERTS'] = '/etc/mosquitto/certs/ca.crt'
#app.config['MQTT_TLS_CERTFILE'] = '/etc/mosquitto/certs/client.crt'
#app.config['MQTT_TLS_KEYFILE'] = '/etc/mosquitto/certs/client.key'


mqtt = Mqtt(app)
socketio = SocketIO(app)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('publish')
def handle_publish(json_str):
    data = json.loads(json_str)
    mqtt.publish(data['topic'], data['message'], data['qos'])


@socketio.on('subscribe')
def handle_subscribe(json_str):
    data = json.loads(json_str)
    mqtt.subscribe(data['topic'], data['qos'])


@socketio.on('unsubscribe_all')
def handle_unsubscribe_all():
    mqtt.unsubscribe_all()


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=json.loads(message.payload.decode()),
        qos=message.qos,
    )
    socketio.emit('mqtt_message', data=data)



@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    pass


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, use_reloader=False, debug=True)
