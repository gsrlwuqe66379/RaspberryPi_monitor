import smbus
import time
class PCF8591(object):
    # 初始化输入器件的物理地址Address，以及I2C的通道编号
    def __init__(self,Address=0x48,bus_id=1):
        self.bus_id = bus_id
        self.Address = Address
        self.bus = smbus.SMBus(self.bus_id)
    
    # 读取对一个模拟通道的输入进行采样 chn为通道号 
    def AD_read(self,chn):
        
        # 写控制字
        if chn ==0:
            self.bus.write_byte(self.Address,0x00)
        if chn ==1:
            self.bus.write_byte(self.Address,0x01)
        if chn ==2:
            self.bus.write_byte(self.Address,0x02)
        if chn ==3:
            self.bus.write_byte(self.Address,0x03)
        
        # 读数据 如果通道号不在0-3之间那么会继续读上一个通道的数据
        return self.bus.read_byte(self.Address)
    
    # 进行DA输出，val为输入的数字量    
    def DA_write(self,val):
        # val的取值应当在0-255之间
        temp = int(val)
        if temp>255:
            temp =255
        if temp<0:
            temp=0
        # 写控制字 写数据    
        self.bus.write_byte_data(self.Address, 0x40, temp)   

if __name__ == "__main__":
    
    m_AD_DA = PCF8591(Address=0x48,bus_id=1)
   
    # # 测试滑动变阻器
    # m_AD_DA.AD_read(3)
    
    # try:
        # while True:
            # AD_in = m_AD_DA.AD_read(10)
            # V_in = float(AD_in)*5.0/255.0
            # print('AIN3 = %d  V = %.2f'%(AD_in,V_in))
            # time.sleep(1)
            
    # # 测试光敏电阻
    # m_AD_DA.AD_read(0)
    
    # try:
        # while True:
            # AD_in = m_AD_DA.AD_read(10)
            # if AD_in>100:
                # str_flag = "dark"
            # else:
                # str_flag = "light"
            
            # print('AIN0 = %d  %s'%( AD_in,str_flag))
            
            # time.sleep(1)
    
    # 测试DA
    count = 0
    try:
        while True:
            m_AD_DA.DA_write(count)
            time.sleep(1)
            count = count+25
            if count>255:
                count = 0
            print("AOUT = %d V = %.2f"%(count,count*5.0/255.0))

  
    except KeyboardInterrupt:
        print('\n Ctrl + C QUIT')   
        
    
    
    
    
    
    
    
        
    