import paho.mqtt.client as mqtt
import elevenlabs
import os
from playsound import playsound

broker = "test.mosquitto.org"
port = 1883

class Handler:
    def __init__(self):
        self.mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    def handle_response(self, audio):
        elevenlabs.save(audio, "response.mp3")

        self.mqttc.connect(broker, port)
        self.mqttc.loop_start()
        msg_info = self.mqttc.publish("robot_buddy/movement", "speechBegin")
        msg_info.wait_for_publish()
        playsound("response.mp3")
        msg_info = self.mqttc.publish("robot_buddy/movement", "speechEnd")
        msg_info.wait_for_publish()
        self.mqttc.disconnect()
        self.mqttc.loop_stop()
        os.remove("response.mp3")

'''if __name__ == '__main__':
    handler = Handler()
    chatbot = ChatBot.Chatbot("chef")
    audio=chatbot.generate_audio("This is a test audio file")
    handler.handle_response(audio)'''
