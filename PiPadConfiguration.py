# GENERIC CONF
PiPadConfiguration = {
    'DEVEL_LOG' : False,
    'CYCLE_WAIT_TIME' : 0.2, 
    'led_active_time' : 1, 
    'clacson_active_time' : 0.5
}

# LED
led = {
    'DEVEL_LOG' : False,
    'led_wait_time' : 1,
    'red_pin' : 5,
    'green_pin' : 6,
    'blue_pin' : 13,
    'led_wait_cycle_time' : 0.1
}

# BUTTONS
buttons = {
    'DEVEL_LOG' : False,
    'btn_wait_time' : 0.1,
    'btn1_pin' : 15,
    'btn2_pin' : 14,
    'LED_ON_TIME' : 0.5
}

# STICK
stick = {
    'DEVEL_LOG' : False,
    'btn_wait_time' : 0.1,
    'axis_wait_time' : 0.1,
    'btn_pin' : 16,
    'x_pin' : 1,
    'y_pin' : 0,
    'min' : 1200,
    'max' : 1300
}

# ROTARY ENCODER
rotary = {
    'DEVEL_LOG' : False,
    'btn_wait_time' : 0.1,
    'clock_wait_time' : 0.01,
    'btn_pin' : 27,
    'clock_pin' : 17,
    'dt_pin' : 18
}
