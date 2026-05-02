import pygame
from pythonosc.udp_client import SimpleUDPClient

pygame.init()
pygame.joystick.init()

if not pygame.joystick.get_count() == 2:
    print("Please connect two Wiimotes.")
    exit()

wiimote1 = pygame.joystick.Joystick(1)
wiimote1.init()

wiimote2 = pygame.joystick.Joystick(0)
wiimote2.init()

client = SimpleUDPClient("192.168.7.2", 7562)

while True:
    pygame.event.pump()

    x = wiimote1.get_axis(0)
    y = wiimote1.get_axis(1)
    z = wiimote1.get_axis(2)

    a = wiimote1.get_button(0)
    b = wiimote1.get_button(1)

    x2 = wiimote2.get_axis(0)
    y2 = wiimote2.get_axis(1)
    z2 = wiimote2.get_axis(2)

    a2 = wiimote2.get_button(0)
    b2 = wiimote2.get_button(1)

    client.send_message("/wiimote1/accel", [x, y, z])
    client.send_message("/wiimote1/button/a", a)
    client.send_message("/wiimote1/button/b", b)

    client.send_message("/wiimote2/accel", [x2, y2, z2])
    client.send_message("/wiimote2/button/a", a2)
    client.send_message("/wiimote2/button/b", b2)