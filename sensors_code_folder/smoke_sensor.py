#!/usr/bin/env python
import PCF8591 as ADC
import RPi.GPIO as GPIO
import time
import math
#GPIO.setwarnings(False)
DO = 17
Buzz = 18
GPIO.setmode(GPIO.BCM)


def setup():
    ADC.setup(0x48)
    GPIO.setup(DO, GPIO.IN)
    #GPIO.setup(Buzz, GPIO.OUT)
    #GPIO.output(Buzz, 1)  # 高电平不响，低电平触发报警蜂鸣


def Print(x):
    if x == 1:
        print
        ''
        print
        '   *********'
        print
        '   * Safe~ *'
        print
        '   *********'
        print
        ''
    if x == 0:
        print
        ''
        print
        '   ***************'
        print
        '   * Danger Gas! *'
        print
        '   ***************'
        print
        ''


def loop():
    status = 1
    count = 0
    while True:
        
        print
        'ADC.read(0)==', ADC.read(0)  # 有烟雾时，该值增大

        tmp = GPIO.input(DO);
        print
        'tmp==', tmp
        # 无烟雾时为高电平，tmp=1,打印safe，有烟雾时为低电平，打印Danger Gas！
        if tmp != status:
            Print(tmp)
            status = tmp
        if status == 0:
            count += 1
            if count % 2 == 0:
                GPIO.output(Buzz, 0)  # 检测到烟雾后，报警声为断续蜂鸣声，低电平为响
            else:
                GPIO.output(Buzz, 1)  # 高电平不响
        else:
            #GPIO.output(Buzz, 1)
            count = 0

        time.sleep(0.2)


def destroy():
    GPIO.output(Buzz, 1)
    GPIO.cleanup()


if __name__ == '__main__':
    try:
        setup()
        loop()
        
    except KeyboardInterrupt:
        destroy()


