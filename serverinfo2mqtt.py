#!/usr/bin/env python

import configparser
import paho.mqtt.client as mqtt
import psutil

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")

    topic  = config['config']['topic']
    disk  = config['config']['disk']
    temperature  = config['config']['temperature']
    username  = config['mqtt-server']['username']
    password  = config['mqtt-server']['password']
    mqtt_host = config['mqtt-server']['host']
    mqtt_port = int(config['mqtt-server']['port'])
    client_id = config['mqtt-server']['client_id']
    ca_certs  = config['mqtt-server']['ca_certs']

    mqtt_client = mqtt.Client(client_id=client_id)
    mqtt_client.username_pw_set(username, password=password)
    mqtt_client.tls_set(ca_certs=ca_certs)
    mqtt_client.connect(mqtt_host, mqtt_port, 60)

    attributes = "{"
    attributes += "\"cpu-usage\": {},".format(psutil.cpu_percent())
    attributes += "\"cpu-temp\": {},".format(max([x.current for x in psutil.sensors_temperatures()[temperature]]))
    attributes += "\"mem-usage\": {},".format(psutil.virtual_memory().percent)
    attributes += "\"swap-usage\": {},".format(psutil.swap_memory().percent)
    attributes += "\"disk-usage\": {}".format(psutil.disk_usage(disk).percent)
    attributes += "}"

    mqtt_client.publish(topic, payload=attributes)

    mqtt_client.disconnect()
