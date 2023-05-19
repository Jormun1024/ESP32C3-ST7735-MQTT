import esp, time, esp32, machine, network
import jormun, sysfont
from ST7735 import TFT, TFTColor
from machine import SPI, Pin, PWM, Timer
from umqtt.simple import MQTTClient

broker_address = '211.81.51.133'# MQTT服务器地址
broker_port = '1885'# MQTT服务器端口
client_id = 'mqttx_5c929375'# MQTT设备id
user_name = 'iot016'# mqtt 设备用户名
password = 'pwd2023'# mqtt 设备密码
publish_topic = 'espsend'# 推送主题
subscribe_topic = 'espreceive'# 订阅主题
SSID = 'Jormun'
PASSWORD = '20011204'
wlan = network.WLAN(network.STA_IF)
mqtt_client = None
spi = SPI(1, baudrate=20000000,polarity=0,phase=0,sck=Pin(7),mosi=Pin(6),miso=Pin(2))
tft=TFT(spi,10,0,1)
tft.initr()
tft.rgb(True)
mqtt_client = None
aString="""A Blessing For The Living. A Flower Branch For the Dead. With The Sword Of Justice. A Punishment Of Death To Evildoers. And We Will Arrive At The Altar Of The Saints. I swear on the name of Santa Maria to smite the unrighteous with my hammer!"""
#给予生者施舍，给予死者鲜花，为正义握剑，给恶徒死的制裁，并且我们会加入圣者的行列，向圣母玛利亚起誓，对一切不义予以铁锤的制裁！

jormun.breathe()#点按boot按键退出呼吸灯模式
jormun.led(5)#长按5秒退出按键输入LED输出模式
jormun.breathe()
jormun.picture(3,2,1)#3张图片，循环显示2次，每张显示1秒
jormun.breathe()
jormun.word(aString)
jormun.presstoexit(2)
jormun.breathe()
jormun.mymqtt()