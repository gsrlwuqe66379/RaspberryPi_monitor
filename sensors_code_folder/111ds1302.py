import RPi.GPIO as GPIO
from pin_dic import pin_dic
from datetime import datetime
import operator
import time

class DS1302(object):
    
    def __init__(self,pin_clk,pin_dat,pin_rst):
        self.pin_clk = pin_clk
        self.pin_dat = pin_dat
        self.pin_rst = pin_rst
        
        self.period = 0.00001
        self.init_dsl302()
        
        # 确定写保护关闭.
        self.write_byte(int("10001110", 2))
        self.write_byte(int("00000000", 2))
        
        # 关闭涓流模式.
        self.write_byte(int("10010000", 2))
        self.write_byte(int("00000000", 2))
        # DS1302 通信终止.
        self.end_ds1302()
        
        
    # DS1302 通信初始化    clk=0 dat=0 rst=1
    def init_dsl302(self):
        GPIO.setup(self.pin_clk,GPIO.OUT,initial=0)
        GPIO.setup(self.pin_dat,GPIO.OUT,initial=0)
        GPIO.setup(self.pin_rst,GPIO.OUT,initial=0)
        
        GPIO.output(self.pin_clk,0)
        GPIO.output(self.pin_dat,0)
        time.sleep(self.period)
        GPIO.output(self.pin_rst,1)
    
    # DS1302 通信结束  clk=0 dat=0 rst=0
    def end_ds1302(self):
        GPIO.setup(self.pin_clk, GPIO.OUT, initial=0)
        GPIO.setup(self.pin_rst, GPIO.OUT, initial=0)
        GPIO.setup(self.pin_dat, GPIO.OUT, initial=0)
        GPIO.output(self.pin_clk, 0)
        GPIO.output(self.pin_dat, 0)
        time.sleep(self.period)
        GPIO.output(self.pin_rst, 0)

    # 写入 一个字节
    def write_byte(self,Byte):
       # 循环写入每个bit
        for Count in range(8):
            time.sleep(self.period)
            GPIO.output(self.pin_clk, 0)
            
            # 获取一个bit数据
            Bit = operator.mod(Byte, 2)
            Byte = operator.floordiv(Byte, 2)
            
            # 将数据送入 io
            time.sleep(self.period)
            GPIO.output(self.pin_dat, Bit)
            
            # clk 上升沿 将数据写入
            time.sleep(self.period)
            GPIO.output(self.pin_clk, 1)
      
    
    # 读取一个字节
    def read_byte(self):
        
        # 设置IO为输入
        GPIO.setup(self.pin_dat, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        Byte = 0
        for Count in range(8):
        
            # 产生一个上升脉冲
            time.sleep(self.period)
            GPIO.output(self.pin_clk, 1)
            time.sleep(self.period)
            GPIO.output(self.pin_clk, 0)
            time.sleep(self.period)
            
            # 读取1bit数据
            Bit = GPIO.input(self.pin_dat)
            Byte |= ((2 ** Count) * Bit)
        
        return Byte

    # 向DS1302的RAM里面写数据
    def write_RAM(self, Data):
        # DS1302 通信初始化.
        self.init_dsl302()
        # 写地址.
        self.write_byte(int("11111110", 2))
        # 写数据共有31个字节的RAM空间.
        for Count in range(len(Data)):
            self.write_byte(ord(Data[Count:Count + 1]))
        
        # 剩余部分写空格
        for Count in range(31 - len(Data)):
            self.write_byte(ord(" "))
        # 通信结束.
        self.end_ds1302()
    
    # 从 ds1302的RAM 中读取数据
    def ReadRAM(self):
        
        # 初始化 DS1302 通信.
        self.init_dsl302()
        # 写地址.
        self.write_byte(int("11111111", 2))
        # 读数据.
        Data = ""
        for Count in range(31):
            Byte = self.read_byte()
            Data += chr(Byte)
        # 通信结束.
        self.end_ds1302()
        return Data
 
    # 向DS1302 中写时间
    def write_DateTime(self,dt):
        # DS1302 通信初始化.
        self.init_dsl302()
        
        # 写地址.
        self.write_byte(int("10111110", 2))
        
        # 写秒.
        Second = dt.second
        self.write_byte(operator.mod(Second, 10) | operator.floordiv(Second, 10) * 16)
        
        # 写分.
        Minute = dt.minute
        self.write_byte(operator.mod(Minute, 10) | operator.floordiv(Minute, 10) * 16)
        
        # 写小时.
        Hour = dt.hour
        self.write_byte(operator.mod(Hour, 10) | operator.floordiv(Hour, 10) * 16)
        
        # 写日期.
        Day = dt.day
        self.write_byte(operator.mod(Day, 10) | operator.floordiv(Day, 10) * 16)
        
        # 写月.
        Month = dt.month
        self.write_byte(operator.mod(Month, 10) | operator.floordiv(Month, 10) * 16)
        
        # 写星期.
        DayOfWeek = int(dt.strftime("%w"))
        if DayOfWeek ==0:
            DayOfWeek = 7
        self.write_byte(operator.mod(DayOfWeek, 10) | operator.floordiv(DayOfWeek, 10) * 16)
        
        # 写年.
        Year = dt.year
        Year = operator.mod(Year, 100)
        self.write_byte(operator.mod(Year, 10) | operator.floordiv(Year, 10) * 16)
  
        # 写保护关闭.
        self.write_byte(int("00000000", 2))
        # 涓流充电模式关闭.
        self.write_byte(int("00000000", 2))
        # End DS1302 communication.
        self.end_ds1302()
    
    def read_DateTime(self):
        
        # DS1302 通信初始化.
        self.init_dsl302()
        # 写地址.
        self.write_byte(int("10111111", 2))
        # Read date and time data.
        Data = ""
        
        # 读秒
        Byte = self.read_byte()
        second = operator.mod(Byte, 16) + operator.floordiv(Byte, 16) * 10
        
        # 读分
        Byte = self.read_byte()
        minute = operator.mod(Byte, 16) + operator.floordiv(Byte, 16) * 10
        
        # 读小时
        Byte = self.read_byte()
        hour = operator.mod(Byte, 16) + operator.floordiv(Byte, 16) * 10
        
        # 读日
        Byte = self.read_byte()
        day = operator.mod(Byte, 16) + operator.floordiv(Byte, 16) * 10
        
        # 读月
        Byte = self.read_byte()
        month = operator.mod(Byte, 16) + operator.floordiv(Byte, 16) * 10
        
        # 读星期 不用操作
        Byte = self.read_byte()
        
        # 读年
        Byte = self.read_byte()
        year = operator.mod(Byte, 16) + operator.floordiv(Byte, 16) * 10
        year = year+2000
        
        self.end_ds1302()
        
        if year == 2000 or month > 12 or month<1 or day < 1 or day > 31:
            return False
            
        if second > 59:
            return False
        
        return datetime(year,month,day,hour,minute,second)

if __name__ == "__main__":
    
    pin_clk = pin_dic['G4']
    pin_dat = pin_dic['G5']
    pin_rst = pin_dic['G6']
    
    GPIO.setmode(GPIO.BOARD)
    
    m_ds1302 = DS1302(pin_clk,pin_dat,pin_rst)
    write_dt = datetime(2021,11,6,10,25,00)
    m_ds1302.write_DateTime(write_dt)
    print(write_dt)
    try:
        while True:
            dt = m_ds1302.read_DateTime()
            
            if not dt:
                continue
            else:
                str_time = dt.strftime("%a %Y-%m-%d  %H:%M:%S")
                print("\r%s"%(str_time),end="")
            
        
        
            time.sleep(1)
        
    except KeyboardInterrupt:
        print('\n Ctrl + C QUIT')
    
    finally:
    
        GPIO.cleanup()
    
    
        
        
        
        
        
    
    
        
        
        
        