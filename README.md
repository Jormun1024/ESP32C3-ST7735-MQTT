# ESP32C3-ST7735-MQTT<br/>
Peiyang University 电子系统设计2 验收实验<br/>
使用WeAct的ESP32C3开发版驱动ST7735液晶屏并连接MQTT服务器实现一定功能<br/>
实验必做功能（满分80）<br/>
• 1个按键输入、1个LED输出<br/>
• 液晶屏显示自己的照片（证件照，需要预存在自己的开发板）<br/>
• WLAN连接到MQTT服务器，注册账户并可以收发消息<br/>
• 液晶屏显示英文字符串（由MQTT服务器下发）<br/>
• 单一程序运行时具备上述功能，不需要切换程序<br/>
实验选做功能（20分）<br/>
• 3个人一组，可以通过MQTT互相收发消息<br/>
• 支持更多传感器输入和数据上传<br/>
• 按键输入支持摩尔斯电码<br/>
• 具有不低于上述功能开发难度的其他功能<br/>
• 根据难度和创意给分<br/>
本人使用的是Thonny IDE，其中，main.py&jormun.py在Thonny IDE中使用，而photo_resize.py是在Spyder IDE中使用，用于修改图片格式及分辨率<br/>
通过摩斯电码向上位机发送消息功能存在str变为nonetype的问题，由于ESP32被老师回收，无法debug<br/>
