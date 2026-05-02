if starting:
	diagnostics.debug("Started")
    
vJoy[0].setButton(0, wiimote[0].buttons.button_down(WiimoteButtons.A))
vJoy[0].setButton(1, wiimote[0].buttons.button_down(WiimoteButtons.B))

# Acceleration
accel = wiimote[0].acceleration

vJoy[0].x = int(accel.x * 16000)
vJoy[0].y = int(accel.y * 16000)
vJoy[0].z = int(accel.z * 16000)

# Acceleration
accel = wiimote[1].acceleration

vJoy[1].x = int(accel.x * 16000)
vJoy[1].y = int(accel.y * 16000)
vJoy[1].z = int(accel.z * 16000)