import pygame
import mido
import threading
import time
from pythonosc.udp_client import SimpleUDPClient

#using midi for ir data
print(mido.get_input_names())

pygame.init()
pygame.joystick.init()

if not pygame.joystick.get_count() == 2:
    print("Please connect two Wiimotes.")
    exit()

wiimote1 = pygame.joystick.Joystick(0)
wiimote1.init()

wiimote2 = pygame.joystick.Joystick(1)
wiimote2.init()


ir = {
    1: {"x":0, "y": 0},
    2: {"x":0, "y": 0},
}

cc_map = {
    33: "x",
    34: "y",
}

def read_port(port_name, label):
    with mido.open_input(port_name) as port:
        print(f"Opened {label}: {port_name}")
        for msg in port:
            if msg.type == "control_change":
                wiimote = msg.channel + 1  # channel 0 = MIDI channel 1

                #print(f"Wiimote {wiimote}: CC{msg.control} = {msg.value}")

                if wiimote not in ir:
                    continue

                name = cc_map.get(msg.control)
                if name is None:
                    continue

                value = msg.value
                ir[wiimote][name] = value


port = mido.get_input_names()[0]  # Adjust if needed


threading.Thread(target=read_port, args=(port, "wii1"), daemon=True).start()


client = SimpleUDPClient("192.168.6.2", 7562)

last_send_time = 0
SEND_INTERVAL = 1 / 60  # 60 Hz

while True:
    pygame.event.pump()


    a = wiimote1.get_button(0)
    b = wiimote1.get_button(1)

    x2 = wiimote2.get_axis(0)
    y2 = wiimote2.get_axis(1)

    now = time.time()
    if now - last_send_time >= SEND_INTERVAL:
        try:
            client.send_message("/wiimote1/button/a", a)
            client.send_message("/wiimote1/button/b", b)

            client.send_message("/wiimote2/accel", [x2, y2])

            client.send_message("/wiimote1/ir", [ir[1]["x"], ir[1]["y"]])
            client.send_message("/wiimote2/ir", [ir[2]["x"], ir[2]["y"]])
        except BlockingIOError:
            pass  # Ignore send errors if the buffer is full

        last_send_time = now