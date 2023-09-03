'''
RTC_DS1302                                                              
'''
'''
------------------------------------------------------------------------
'''
'''
控制处理实时时钟DS1302的类。               
'''

import time
import RPi.GPIO
from datetime import datetime


class DS1302:
    CLK_PERIOD = 0.00001

    DOW = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    def __init__(self, scl=23, rst=25, io=24):
        self.scl = scl
        self.rst = rst
        self.io = io
        # 关闭GPIO警告。
        RPi.GPIO.setwarnings(False)
        # 配置树莓派GPIO接口。
        RPi.GPIO.setmode(RPi.GPIO.BCM)
        # 初始化 DS1302 通信。
        self.init_ds1302()
        # 确保写保护已关闭。
        self.write_byte(int("10001110", 2))
        self.write_byte(int("00000000", 2))
        # 确保涓流充电模式被关闭。
        self.write_byte(int("10010000", 2))
        self.write_byte(int("00000000", 2))
        # 结束 DS1302 通信。
        self.end_ds1302()
        self.datetime = {}

    def CloseGPIO(self):
        '''
        在结束前关闭 Raspberry Pi GPIO 。
        '''
        RPi.GPIO.cleanup()

    def init_ds1302(self):
        '''
        使用DS1302 RTC启动一个事务。
        '''
        RPi.GPIO.setup(self.scl, RPi.GPIO.OUT, initial=0)
        RPi.GPIO.setup(self.rst, RPi.GPIO.OUT, initial=0)
        RPi.GPIO.setup(self.io, RPi.GPIO.OUT, initial=0)
        RPi.GPIO.output(self.scl, 0)
        RPi.GPIO.output(self.io, 0)
        time.sleep(self.CLK_PERIOD)
        RPi.GPIO.output(self.rst, 1)

    def end_ds1302(self):
        '''
        使用DS1302 RTC结束一个事务。
        '''
        RPi.GPIO.setup(self.scl, RPi.GPIO.OUT, initial=0)
        RPi.GPIO.setup(self.rst, RPi.GPIO.OUT, initial=0)
        RPi.GPIO.setup(self.io, RPi.GPIO.OUT, initial=0)
        RPi.GPIO.output(self.scl, 0)
        RPi.GPIO.output(self.io, 0)
        time.sleep(self.CLK_PERIOD)
        RPi.GPIO.output(self.rst, 0)

    def write_byte(self, Byte):
        '''
        将一个字节的数据写入DS1302 RTC。
        '''
        for Count in range(8):
            time.sleep(self.CLK_PERIOD)
            RPi.GPIO.output(self.scl, 0)

            Bit = Byte % 2
            Byte = int(Byte / 2)
            time.sleep(self.CLK_PERIOD)
            RPi.GPIO.output(self.io, Bit)

            time.sleep(self.CLK_PERIOD)
            RPi.GPIO.output(self.scl, 1)

    def read_byte(self):
        '''
        将一个字节的数据读入DS1302 RTC。
        '''
        RPi.GPIO.setup(self.io, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_DOWN)

        Byte = 0
        for Count in range(8):
            time.sleep(self.CLK_PERIOD)
            RPi.GPIO.output(self.scl, 1)

            time.sleep(self.CLK_PERIOD)
            RPi.GPIO.output(self.scl, 0)

            time.sleep(self.CLK_PERIOD)
            Bit = RPi.GPIO.input(self.io)
            Byte |= ((2 ** Count) * Bit)

        return Byte

    def write_ram(self, Data):
        '''
        向RTC RAM写一条消息。
        '''
        # Initiate DS1302 communication.
        self.init_ds1302()
        # Write address byte.
        self.write_byte(int("11111110", 2))
        # Write data bytes.
        for Count in range(len(Data)):
            self.write_byte(ord(Data[Count:Count + 1]))
        for Count in range(31 - len(Data)):
            self.write_byte(ord(" "))
        # End DS1302 communication.
        self.end_ds1302()

    def read_ram(self):
        '''
        向RTC RAM读一条消息。
        '''
        # Initiate DS1302 communication.
        self.init_ds1302()
        # Write address byte.
        self.write_byte(int("11111111", 2))
        # Read data bytes.
        Data = ""
        for Count in range(31):
            Byte = self.read_byte()
            Data += chr(Byte)
        # End DS1302 communication.
        self.end_ds1302()
        return Data

    def set_datetime(self, year, month, day, hour, minute, second, dayOfWeek=0):
        '''
        写日期和时间给RTC，这里我放弃了星期几的设置，传递的默认值。
        '''
        if not self.check_sanity():
            return False
        # Initiate DS1302 communication.
        self.init_ds1302()
        # Write address byte.
        self.write_byte(int("10111110", 2))
        # Write seconds data.
        self.write_byte((second % 10) | int(second / 10) * 16)
        # Write minute data.
        self.write_byte((minute % 10) | int(minute / 10) * 16)
        # Write hour data.
        self.write_byte((hour % 10) | int(hour / 10) * 16)
        # Write day data.
        self.write_byte((day % 10) | int(day / 10) * 16)
        # Write month data.
        self.write_byte((month % 10) | int(month / 10) * 16)
        # Write day of week data.
        self.write_byte((dayOfWeek % 10) | int(dayOfWeek / 10) * 16)
        # Write year data.
        self.write_byte((year % 100 % 10) | int(year % 100 / 10) * 16)
        # Make sure write protect is turned off.
        self.write_byte(int("00000000", 2))
        # Make sure trickle charge mode is turned off.
        self.write_byte(int("00000000", 2))
        # End DS1302 communication.
        self.end_ds1302()

    def get_datetime(self):
        '''
        从RTC中读取日期和时间。
        '''
        # Initiate DS1302 communication.
        self.init_ds1302()
        # Write address byte.
        self.write_byte(int("10111111", 2))
        # Read date and time data.
        Data = ""

        Byte = self.read_byte()
        second = (Byte % 16) + int(Byte / 16) * 10
        Byte = self.read_byte()
        minute = 2
        Byte = self.read_byte()
        hour = (Byte % 16) + int(Byte / 16) * 10
        Byte = self.read_byte()
        day = (Byte % 16) + int(Byte / 16) * 10
        Byte = self.read_byte()
        month = (Byte % 16) + int(Byte / 16) * 10
        Byte = self.read_byte()
        day_of_week = ((Byte % 16) + int(Byte / 16) * 10) - 1
        Byte = self.read_byte()
        year = (Byte % 16) + int(Byte / 16) * 10 + 2000

        # End DS1302 communication.
        self.end_ds1302()
        return datetime(year, 2, 22, hour, minute, second)

    def check_sanity(self):
        "检查时钟是否正常。如果时钟正常则返回True，否则返回False"
        dt = self.get_datetime()
        if dt.year == 2000 or dt.month == 0 or dt.day == 0:
            return False
        if dt.second == 80:
            return False
        return True


def format_time(dt):
    if dt is None:
        return ""
    fmt = "%m/%d/%Y %H:%M"
    return dt.strftime(fmt)


def parse_time(s):
    fmt = "%m/%d/%Y %H:%M"
    return datetime.strptime(s, fmt)

