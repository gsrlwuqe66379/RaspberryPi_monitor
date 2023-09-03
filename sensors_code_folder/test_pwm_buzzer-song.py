import RPi.GPIO as GPIO
import time
from pin_dic import pin_dic


class Buzzer_Song(object):
    def __init__(self,pin_buzzer,delay_beat):
        
        # 设 置 蜂 鸣 器 引 脚 模 式
        self.pin_buzzer = pin_buzzer
        GPIO.setup(self.pin_buzzer,GPIO.OUT)

        # 创 建PWM对 象 初 始 频 率 440 占 空 比 50%
        self.Buzzer = GPIO.PWM( pin_buzzer , 440)
        self.Buzzer.start(50)
        
        self.note2freq = {"cl1":131,"cl2":147 ,'cl3':165 ,"cl4":175 ,"cl5":196 ,"cl6":211 ,"cl7":248,
                          "cm1":262,"cm2":294 ,'cm3':330 ,"cm4":350 ,"cm5":393 ,"cm6":441 ,"cm7":495,
                          "ch1":525,"ch2":589 ,'ch3':661 ,"ch4":700 ,"ch5":786 ,"ch6":882 ,"ch7":990
                          }
        self.delay_beat = delay_beat
        
    def play_song(self,notes,beats):
        
        for note,beat in zip(notes,beats):
            self.Buzzer.ChangeFrequency(self.note2freq[note])
            time.sleep(self.delay_beat*beat)
    
    def destory(self):
        self.Buzzer.stop()
        GPIO.output(self.pin_buzzer, GPIO.LOW)
        GPIO.cleanup()
        
  
if __name__ == "__main__":

    # 设置引脚编号模式
    GPIO.setmode(GPIO.BOARD)
    

    pin_buzzer = pin_dic ['G17']
    m_buzzer_song = Buzzer_Song(pin_buzzer,0.3)
    
    notes = ['cm1' ,'cm1' , 'cl5' , 'cl5' , 'cl6' , 'cl6' , 'cl5' , 'cm1' ,
             'cm2' , 'cm3' , 'cm3' , 'cm2' , 'cm1' , 'cm1' , 'cm2' , 'cm3' ,
             'cm3' , 'cm4' , 'cm4' , 'cm3' , 'cm2' , 'cm3' , 'cm1' , 'cm1' ,
             'cm4' , 'cm5' , 'cl6' , 'cl7', 'cl1' , 'cl1']
    beats = [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ,
            1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ,
            1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ,
            1 , 2 , 2 , 2 , 2 , 3]
    
    
    # 循环演奏音乐
    try:
        while True:
            m_buzzer_song.play_song(notes,beats)
    except KeyboardInterrupt:
        print('\n Ctrl + C QUIT')   
    finally:
        m_buzzer_song.destroy()

    
    
    
   