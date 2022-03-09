import pyb

p = pyb.Pin(pyb.Pin.board.PA7,pyb.Pin.OUT_PP)
t = pyb.Timer(3, freq = 50)
tch = t.channel(2,pyb.Timer.PWM, pin=p)
if __name__ == '__main__':
    while True:
        pwm = int(input('Input PWM: '))
        if pwm > 0:
            tch.pulse_width_percent(pwm)
        elif pwm == 0:
            break
    print('End')
