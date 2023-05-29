import esp, time, esp32, machine, network
import sysfont
from ST7735 import TFT, TFTColor
from machine import SPI, Pin, PWM, Timer
from umqtt.simple import MQTTClient

spi = SPI(1, baudrate=20000000,polarity=0,phase=0,sck=Pin(7),mosi=Pin(6),miso=Pin(2))
tft=TFT(spi,10,0,1)
tft.initr()
tft.rgb(True)
tft.fill(TFTColor(0xA6, 0x64, 0xA0))
broker_address = '211.81.51.133'# MQTT服务器地址
broker_port = '1885'# MQTT服务器端口
client_id = 'mqttx_e12d5d83'# MQTT设备id
user_name = 'iot016'# mqtt 设备用户名
password = 'pwd2023'# mqtt 设备密码
publish_topic = 'espsend'# 推送主题
subscribe_topic = 'espreceive'# 订阅主题
esp32_topic = 'esptopic'# ESP32之间通信用的主题
SSID = 'Jormun'
PASSWORD = '20011204'
mqtt_client = None

def picture(n1,n2,n3):
    i=1
    j=0
    str1=str('Display '+str(n1)+' photos, cycle through '+str(n2)+' times, each photo will display for '+str(n3)+' seconds. ')
    word(str1)
    time.sleep(2)
    while True:
        if j < n1*n2:
            while i<n1+1:
                f=open('./img/img'+str(i)+'.bmp', 'rb')
                if f.read(2) == b'BM':
                    dummy = f.read(8)
                    offset = int.from_bytes(f.read(4), 'little')
                    hdrsize = int.from_bytes(f.read(4), 'little')
                    width = int.from_bytes(f.read(4), 'little')
                    height = int.from_bytes(f.read(4), 'little')
                    if int.from_bytes(f.read(2), 'little') == 1:
                        depth = int.from_bytes(f.read(2), 'little')
                        if depth == 24 and int.from_bytes(f.read(4), 'little') == 0:
                            rowsize = (width * 3 + 3) & ~3
                            if height < 0:
                                height = -height
                                flip = False
                            else:
                                flip = True
                            w, h = width, height
                            tft._setwindowloc((0,0),(w - 1,h - 1))
                            for row in range(h):
                                if flip:
                                     pos = offset + (height - 1 - row) * rowsize
                                else:
                                    pos = offset + row * rowsize
                                if f.tell() != pos:
                                    dummy = f.seek(pos)
                                for col in range(w):
                                    bgr = f.read(3)
                                    tft._pushcolor(TFTColor(bgr[2],bgr[1],bgr[0]))
                i += 1
                j += 1
                if i > n1:
                    i = 1
                if j == n1*n2:
                    time.sleep(n3)
                    word('End of image presentation. ')
                    time.sleep(1)
                    break
                else:
                    time.sleep(n3)
                    continue
                spi.deinit()
        else:
            break
        
def word(aString):
    tft.fill(TFTColor(0xA6, 0x64, 0xA0))
    tft.setvscroll(1, 1)
    aPos=[0,4]
    aColor=TFTColor(0xFF, 0xFF, 0xFF)
    aFont= sysfont.sysfont
    tft.text(aPos,aString,aColor,aFont,aSize=1)
    
def led(et):
    e=0
    ex = 0
    led=Pin(8,Pin.OUT)
    key=Pin(9,Pin.IN)
    word('Keyint-Ledout mode. ')
    while True:
        deshake(key)
        if e == 0:
            while True:
                if key.value() == 0:
                    ex += 1
                    led.value(0)
                    time.sleep_ms(100)
                    if ex > 10*et:
                        e=1
                        break
                else:
                    ex = 0
                    led.value(1)
                    time.sleep_ms(100)
        else:
            word('Exit Keyint-Ledout mode. ')
            time.sleep(1)
            break

def deshake(key):
    cur_value = key.value()
    active = 0
    while active < 10:
        if key.value() != cur_value:
            active += 1
        else:
            active = 0
        time.sleep_ms(10)
        
def breathe():
    word('Led breathing mode. ')
    led=Pin(8,Pin.OUT)
    key=Pin(9,Pin.IN)
    while True:
        led.value(1)
        time.sleep(1)
        led.value(0)
        time.sleep(1)
        if key.value() == 0:
            word('Exit Led breathing mode. ')
            time.sleep(1)
            break

def presstoexit(et):
    ex=0
    led=Pin(8,Pin.OUT)
    key=Pin(9,Pin.IN)
    while True:
        if key.value() == 0:
            ex += 1
            led.value(0)
            time.sleep_ms(100)
            if ex > 10*et:
                e=1
                break
        else:
            ex=0
            continue

def connectwifi(ssid, passwd):
    global wlan
    word('Connecting to WiFi...')
    wlan = network.WLAN(network.STA_IF)  # create a wlan object
    wlan.active(True)  # Activate the network interface
    wlan.disconnect()  # Disconnect the last connected WiFi
    wlan.connect(ssid, passwd)  # connect wifi
    while (wlan.ifconfig()[0] == '0.0.0.0'):
        time.sleep(1)
    wlan_info = wlan.ifconfig()
    word("IP address: " + wlan_info[0])
    time.sleep(1)
    word("Subnet mask: " + wlan_info[1])
    time.sleep(1)
    word("Gateway: " + wlan_info[2])
    time.sleep(1)
    word("DNS: " + wlan_info[3])
    time.sleep(1)

def sub_cb(topic, msg):
    print("接收到数据", (topic, msg))
    global recmsg
    recmsg=str(msg)

def mymqtt():
    led=Pin(8,Pin.OUT)
    key=Pin(9,Pin.IN)
    try:
        connectwifi(SSID, PASSWORD)
        mqtt_client = MQTTClient(client_id=client_id, server=broker_address, port=broker_port, user=user_name,
                                 password=password, keepalive=60)
        mqtt_client.set_callback(sub_cb)
        mqtt_client.connect()
        mqtt_client.subscribe(subscribe_topic)
#         mqtt_client.subscribe(esp32_topic)
        mqtt_client.publish(topic=publish_topic, msg="Jormun Connects Successfully", retain=False, qos=1)
        word("Connect Successfully")
        time.sleep(1)
        word("mqtt_client 1: %s" % mqtt_client.client_id)
        while True:
            mqtt_client.publish(topic=esp32_topic, msg='Jormun is online', retain=False, qos=1)
            time.sleep(1)
            mqtt_client.wait_msg()  # wait message
            mqtt_client.publish(topic=publish_topic, msg='Jormun Receives Successfully', retain=False, qos=1)
            mqtt_client.publish(topic=esp32_topic, msg='Jormun Receives Successfully', retain=False, qos=1)
            word("Receive Successfully")
            time.sleep(1)
            word(recmsg[2:-1])
            time.sleep(1)
            if recmsg[2:-1] == 'led':
                led(5)
                continue
            elif recmsg[2:-1] == 'breathe':
                breathe()
                continue
            elif recmsg[2:-1] == 'picture':
                picture(8,2,1)
                continue
            elif recmsg[2:-1] == 'led on':
                led.value(0)
                continue
            elif recmsg[2:-1] == 'led off':
                led.value(1)
                continue
            elif recmsg[2:-1] == 'morse code':
                s = keymorse(5)
                morse2str(s)
                ledmorse(s)
                continue
            elif recmsg[2:-1] == 'offline':
                word('offline')
                time.sleep(2)
                esp_restart()
                continue
    except Exception as ex_results:
        print('exception1', ex_results)
    finally:
        if (mqtt_client is not None):
            mqtt_client.disconnect()
        wlan.disconnect()
        wlan.active(False)
        
def enmorsecode(x):#返回对应的摩斯码
    dic = {'A': '._', 'B': '_...', 'C': '_._.', 'D': '_..', 'E': '.',
           'F': '.._.','G': '__.', 'H': '....', 'I': '..', 'J': '.___',
           'K': '_._', 'L': '._..','M': '__', 'N': '_.', 'O': '___',
           'P': '.__.', 'Q': '__._', 'R': '._.','S': '...', 'T': '_', 
           'U': '.._', 'V': '..._', 'W': '.__', 'X': '_.._','Y': '_.__',
           'Z': '__..',
           '1': '.____', '2': '..___', '3': '...__', '4': '...._', '5': '.....',
           '6': '_....', '7': '__...', '8': '___..', '9': '____.', '0': '_____',
           ' ': ' ', ',': '__..__', '.': '._._._', ':': '___...', '?': '..__._',
           '-': '_..._', '/': '_.._.', '(': '_.__.',')':'_.__._', '!': '_._.__'}
    if x in dic:
        return dic[x]
 
def demorsecode(x):#返回对应的字符串
    dic = {'._': 'A', '_...': 'B', '_._.': 'C', '_..': 'D', '.': 'E',
           '.._.': 'F','__.': 'G', '....': 'H', '..': 'I', '.___': 'J',
           '_._': 'K', '._..': 'L','__': 'M', '_.': 'N', '___': 'O', 
           '.__.': 'P', '__._': 'Q', '._.': 'R','...': 'S', '_': 'T',
           '.._': 'U', '..._': 'V', '.__': 'W', '_.._': 'X','_.__': 'Y',
           '__..': 'Z',
           '.____': '1', '..___': '2', '...__': '3', '...._': '4', '.....': '5',
           '_....': '6', '__...': '7', '___..': '8', '____.': '9', '_____': '0',
           ' ': ' ', '__..__': ',', '._._._': '.', '___...': ':', '..__._': '?',
           '_..._': '-', '_.._.': '/', '_.__.': '(','_.__._':')', '_._.__': '!',}
    if x in dic:
        return dic[x]

def str2morse(s):#字符串转为摩斯密码串
    s = s.upper()#将小写字母转换为大写字母
    num = len(s)
    encode = ''
    i = 0
    word(s)
    for i in range(num):
        encode += str(enmorsecode(s[i])) + '|'
    ledmorse(encode)
    return encode

def morse2str(s):#摩斯密码串转为字符串
    decode = ''
    f = s.split('|')
    for i in range(len(f)-1):
        decode += str(demorsecode(f[i]))
    word(decode)
    return decode
     
def ledmorse(s):
    led=Pin(8,Pin.OUT)
    for i in range(len(s)):
        if s[i] == ' ':
            led.value(0)
            time.sleep_ms(500)
            led.value(1)
            time.sleep(1)
            print(' ')
            continue
        elif s[i] == '.':
            led.value(0)
            time.sleep(1)
            led.value(1)
            time.sleep(1)
            print('.')
            continue
        elif s[i] == '_':
            led.value(0)
            time.sleep(2)
            led.value(1)
            time.sleep(1)
            print('_')
            continue
        elif s[i] == '|':
            led.value(0)
            time.sleep(3)
            led.value(1)
            time.sleep(1)
            print('|')
            continue
        else:
            led.value(1)
            time.sleep(1)
            continue
        
def keymorse(et):
    e = 0
    s = ''
    ex = 0
    key=Pin(9,Pin.IN)
    while e == 0:
        if key.value() == 0:
            ex += 1
            led.value(0)
            time.sleep_ms(100)
            if ex > 2 and ex < 8:
                s += ' '
                continue
            elif ex > 7 and ex < 15:
                s += '.'
                continue
            elif ex > 14 and ex < 25:
                s += '_'
                continue
            elif ex > 24 and ex < 10*et:
                s += '|'
                continue
            elif ex > 10*et:
                e=1
                break
        else:
            ex = 0
            led.value(1)
            time.sleep_ms(100)
    return s