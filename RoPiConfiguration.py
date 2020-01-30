# configuration
RoPiConfiguration = {
    'DEVEL_LOG' : False,
    'remote_address' : '192.168.1.118'
}

# motor
motor = {
    'DEVEL_LOG' : True,
    'AUTO_TIME' : 0.3,
    'ACCELERATION_TIME' : 0.05,
    'motor_wait_time' : 3,
    'motor_acceleration_time' : 1,
    'motor_back_left_pin' : 4,
    'motor_back_right_pin' : 27,
    'motor_front_left_pin' : 17,
    'motor_front_right_pin' : 22
}

# servo
servo = {
    'DEVEL_LOG' : False,
    'servo_wait_time' : 3,
    'servo_reset_time' : 0.5,
    'angle1' : 90,
    'angle2' : 90,
    'frequency' : 50,
    'servo_1_pin' : 18,
    'servo_2_pin' : 12
}

# distance
distance = {
    'DEVEL_LOG' : False,
    'distance_wait_time' : 2,
    'SAFETY_DISTANCE' : 10, # cm
    'SPEED_OF_SOUND' : 17150, # 34300/2
    'TRIG_SPAN' : .00001, # sec
    'SENSORS_OFF_SPAN' : .5, # sec
    'trig_1_pin' : 23,
    'echo_1_pin' : 24,
    'trig_2_pin' : 26,
    'echo_2_pin' : 25
}

# track
track = {
    'DEVEL_LOG' : False,
    'color' : 0,
    'track_wait_time' : 0.3, 
    'track_1_pin' : 20,
    'track_2_pin' : 21
}

# led
led = {
    'DEVEL_LOG' : False,
    'led_wait_time' : 1,
    'red_pin' : 16,
    'green_pin' :  5,
    'blue_pin' :  6
}

# screen
screen = {
    'DEVEL_LOG' : False,
    'lcd_columns' : 16,
    'lcd_rows' : 2,
    'lcd_backlight' : 4,
    'lcd_rs' : 10,
    'lcd_en' : 9,
    'lcd_d4' : 19,
    'lcd_d5' : 8,
    'lcd_d6' : 7,
    'lcd_d7' : 11
}

# buzzer
buzzer = {
    'DEVEL_LOG' : False,
    'quiet' : True, 
    'buzzer_wait_time' : 1, 
    'buzzer_pin' : 13
}
