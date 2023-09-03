import time
import datetime
import psycopg2
from random import choice, randint
import RPi.GPIO as GPIO
from pin_dic import pin_dic
import time

conn = psycopg2.connect(
                        database="postgres",
                        user="postgres",
                        password="11111111",
                        host="192.168.1.106",
                        port="5432")
                        
cursor = conn.cursor()


class DHT11(object):
    
    def __init__(self,pin_D):
        self._pin = pin_D
        
        
    def collect_input(self):

        unchanged_count = 0

        # 信号持续的最大长度，用来判断数据传输是否结束
        max_unchanged_count = 100

        last = -1
        data = []
        while True:
            # 不断采集数据
            current = GPIO.input(self._pin)
            data.append(current)
            
            # 记录信号持续的时间
            # 如果有变化就开启一段新的记录
            if last != current:
                unchanged_count = 0
                last = current
            # 没有变化时长+1
            else:
                unchanged_count += 1
                if unchanged_count > max_unchanged_count:
                    break

        return data

    # 从收集的信号中获取数据位高电平的持续时间
    def get_high_state_lengths_data(self, data):
        
        # 设置5个状态 分别是 初始延时 起始位低电平 起始位高电平 数据位低电平 数据位高电平
        STATE_DELAY_H = 1
        STATE_START_L = 2
        STATE_START_H = 3
        STATE_DATA_L = 4
        STATE_DATA_H = 5

        state = STATE_DELAY_H

        lengths = [] # 记录每个数据周期中高电平持续时间
        current_length = 0 # 记录前一个状态的持续时间

        for i in range(len(data)):
            current = data[i]
            current_length += 1
            
            # 等待的高电平
            if state == STATE_DELAY_H:
                if current == GPIO.LOW:
                    state = STATE_START_L
                    continue
                else:
                    continue
            
            # 起始的低电平        
            if state == STATE_START_L:
                if current == GPIO.HIGH:
                    state = STATE_START_H
                    continue
                else:
                    continue
                    
            # 起始的高电平
            if state == STATE_START_H:
                if current == GPIO.LOW:
                    state = STATE_DATA_L
                    continue
                else:
                    continue
                    
            # 数据的低电平        
            if state == STATE_DATA_L:
                if current == GPIO.HIGH:
                    current_length = 0
                    state = STATE_DATA_H
                    continue
                else:
                    continue
            
            # 数据的高电平
            if state == STATE_DATA_H:
                if current == GPIO.LOW:
                    lengths.append(current_length)
                    state = STATE_DATA_L
                    continue
                else:
                    continue

        return lengths
    
    
    # 通过记录的数据高电平的持续时长来进行0、1解码
    def calculate_bits(self,high_state_lengths_data):
        # 找到最长和最短的时长
        shortest_pull_up = 1000
        longest_pull_up = 0

        for i in range(0, len(high_state_lengths_data)):
            length = high_state_lengths_data[i]
            if length < shortest_pull_up:
                shortest_pull_up = length
            if length > longest_pull_up:
                longest_pull_up = length

        # 用中间值作为阈值
        halfway = (longest_pull_up + shortest_pull_up) / 2
        bits = []
        
        # 大于阈值判定为1 ，否则判定为0
        for i in range(0, len(high_state_lengths_data)):
            bit = False
            if high_state_lengths_data[i] > halfway:
                bit = True
            bits.append(bit)

        return bits
    
    # 每8个bit一组 将bit转换成字节（byte）
    def bits_to_bytes(self, bits):
        the_bytes = []
        byte = 0

        for i in range(0, len(bits)):
            byte = byte << 1
            if (bits[i]):
                byte = byte | 1
            else:
                byte = byte | 0
            if ((i + 1) % 8 == 0):
                the_bytes.append(byte)
                byte = 0

        return the_bytes
    
        
            
    # 计算校验值 前四个字节相加取低8位作为校验码
    def calculate_checksum(self, the_bytes):
        return (the_bytes[0] + the_bytes[1] + the_bytes[2] + the_bytes[3]) & 255
    
    # 读取温度、湿度
    def read_DHT(self):
        
        # 设置为输出引脚
        GPIO. setup (self._pin , GPIO.OUT)
        
        # 输出高电平
        GPIO.output(self._pin, GPIO.HIGH)
        time.sleep(0.05)
        
        # 输出低电平
        GPIO.output(self._pin, GPIO.LOW)
        time.sleep(0.02)
        
        # 放弃总线控制权，设置为输入引脚，上拉模式
        GPIO.setup(self._pin, GPIO.IN, GPIO.PUD_UP)
        
        # 收集从数据线上传来的数据
        data = self.collect_input()
        
        # 从收集的信号中获取数据位，高电平持续时间
        high_state_lengths_data = self.get_high_state_lengths_data(data)
        
        # 数据应当有40位，即有40段高电平 包括4字节数据和一字节校验不对的话退出
        if len(high_state_lengths_data) != 40:
            return False,0
            
        # 根据上升脉冲的长度计算二进制bit
        bits = self.calculate_bits(high_state_lengths_data)

        # 将二进制bit变换为字节
        the_bytes = self.bits_to_bytes(bits)

        # 进行校验 校验失败 返回错误信息
        checksum = self.calculate_checksum(the_bytes)
        if the_bytes[4] != checksum:
            return False,0

        # 四个字节0-3 分别是湿度的整数、湿度的小数、温度的整数、温度的小数
        temperature = the_bytes[2] + float(the_bytes[3]) / 10
        humidity = the_bytes[0] + float(the_bytes[1]) / 10
        
        # 正确接收返回接收正确标志以及计算得到的温度湿度值
        return True, [temperature, humidity]


def insert_batch(a):
    
    t = time.time()
    #ti = now.strftime("%H-%M-%S")
    #print(ti)
    values = []
    #name = "TEMPUTRUE&WETNESS".split(" ")
    for i in range(1):
        values.append("({},{})".format(a[0], a[1]))
    sql = "insert into record (temperature, wet) values " + ",".join(values)
    cursor.execute(sql)
    #print( " Data update !" )
    conn.commit()
    


if __name__ == "__main__":
    # 设置引脚及工作方式
    pin_dht=  pin_dic['G16']
    GPIO.setmode(GPIO.BOARD)
    
    m_DHT11 =  DHT11(pin_dht)
    

    try: 
        while True:
            flag, result = m_DHT11.read_DHT()        
            
            if flag:
                #print(datetime.datetime.today())
                print("温度: %-3.1f C  湿度: %-3.1f %% " %(result[0],result[1]))
                insert_batch(result)
                time.sleep(60)
            else:
                print("ERROR")                
                 time.sleep(5)    
    except KeyboardInterrupt:
        print('\n Ctrl + C QUIT')
        # 关闭游标
        cursor.close()
        # 关闭数据库连接
        conn.close()
    finally:
        GPIO.cleanup()   

    
    
    

