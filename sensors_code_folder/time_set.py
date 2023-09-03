#!/usr/bin/env python
from datetime import datetime
import time

import ds1302  # 导入模块ds1302

rtc = ds1302.DS1302()  # 通过模块ds1302中的类DS1302()创建一个实例rtc


def setup():
    ''' 写入初始时间 '''
    print
    ''
    print
    ''
    print
    rtc.get_datetime()
    print
    ''
    print
    ''
    #a = raw_input("Do you want to setup date and time?(y/n) ")
    #if a == 'y' or a == 'Y':
        date = raw_input("Input date:(YYYY MM DD) ")
        time = raw_input("Input time:(HH MM SS) ")
        date = date.split()
        time = time.split()
        print
        ''
        print
        ''

        rtc.set_datetime(int(date[0]), int(date[1]), int(date[2]), \
                         int(time[0]), int(time[1]), int(time[2]))

        dt = rtc.get_datetime()
        print
        "You set the date and time to:", dt


def loop():
    ''' 显示实时时间 '''
    while True:
        a = rtc.get_datetime()
        print
        a
        time.sleep(1)


def destory():
    GPIO.cleanup()  # Release resource


if __name__ == '__main__':  # Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destory()


