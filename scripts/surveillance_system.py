import os
import RPi.GPIO as GPIO
import time
import telepot

motion = False
motionrunning = True
count = 0

GPIO.setmode(GPIO.BCM)          #refering to pin number after 'GPIO' not the real boardpin number
GPIO.setwarnings(False)         #if there are warnings that the pin is used
GPIO.setup(18, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

bot = telepot.Bot('BOT_ID')

def switch_ON():
    GPIO.output(18, GPIO.LOW)

def switch_OFF():
    GPIO.output(18, GPIO.HIGH)

def motion_detection():
    if GPIO.input(23) == GPIO.LOW:
        global motion
        motion = True
    else:
        motion = False

def send_MSG():
    bot.sendMessage(ID, 'Hallo - Bewegung detektiert http://10.8.0.2:8081')

def send_MSG_VPN(status):
    bot.sendMessage(ID, 'VPN {} erreichbar'.format(status))

def check_Cam():
    camact=os.system('ping 192.168.14.60 -c4 | grep "4 received, 0% packet loss"')  #True camact = 0
    if camact != 0:
        time.sleep(60)
        camact=os.system('ping 192.168.14.60 -c4 | grep "4 received, 0% packet loss"')
        if camact != 0:
            print ('Cam not reachable',  camact)
            os.system('sudo dhcpd -cf /etc/dhcp/dhcpd.conf')
            camact=os.system('ping 192.168.14.60 -c4 | grep "4 received, 0% packet loss"')
            print ('DHCP-started camact',  camact)
        else:
            print('Cam is reachable')
    else:
        print('Cam is reachable')

def check_motion():
    motionstat=os.system('sudo systemctl status motion.service | grep "Active: active"')

    if motionstat == 0:
        global motionrunning
        motionrunning = True
    else:
        motionrunning = False

def stop_motion():
    print('stop motion')
    os.system('sudo systemctl stop motion.service')
    check_motion()

def start_motion():
    print('start motion')
    os.system('sudo systemctl start motion.service')
    check_motion()

def vpn_reachable():
    global count
    vpn_on=os.system('ping -I tun0 10.8.0.1 -c1 | grep "1 received, 0% packet loss"')
    while vpn_on != 0:
        if count == 0:
            send_MSG_VPN(status = 'nicht')
        vpn_on=os.system('ping -I tun0 10.8.0.1 -c4 | grep "4 received, 0% packet loss"')
        count = vpn_on + count
    if count == 0:
        send_MSG_VPN(status = 'ist')
    count += 1
    print('VPN connection secured')

#GPIO.add.event_detect(23, GPIO.RISING, bouncetime=300)

while True:
    vpn_reachable()
    motion_detection()
    if motion == True:
        print ('motion detected',  motion)
        switch_ON()
        check_motion()
        if motionrunning == False:
            start_motion()
        check_Cam()
        send_MSG()
        time.sleep(180) #adapt to 180s - 3min
        while motion == True:
            print ('still motion detected')
            motion_detection()
        switch_OFF()
        stop_motion()
    else:
        time.sleep(2)
        print ('No motion detected',  motion)

