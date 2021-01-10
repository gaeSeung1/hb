import RPi.GPIO as GPIO
import time
import pigpio
pi = pigpio.pi() # Connect to local Pi.

pin_IR = 16
pin_servo_open = 20
pin_servo_lock = 21
pin_switch = 26

bpm_list = [0,0,0,0,0]
step_list = [0,0,0,0,0]

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_IR,GPIO.IN)
GPIO.setwarnings(False)
GPIO.setup(pin_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

IR_cnt = 0
switch_cnt = 0
lock_switch = 0

#open_init
#servo
pi.set_servo_pulsewidth(pin_servo_open, 800)
pi.set_servo_pulsewidth(pin_servo_lock, 800)
time.sleep(1)

try:
    while True:
        file1 = open("BPM_output.txt", 'r')
        data1 = file.read()
        file2 = open("STEP_output.txt", 'r')
        data2 = file.read()
        file3 = open("STEP_offset.txt", 'r')
        data3 = file.read()
        try:
            y = float(data1)
            step = int(data2) - int(data3) #step - offset
        except:
            pass
        bpm_list.pop(0)
        bpm_list.append(y)
        step_list.pop(0)
        step_list.append(step)
        
        AVG_bpm = sum(bpm_list)/len(bpm_list)
        AVG_step = sum(step_list)/len(step_list)
        #print(AVG)
        #lock
        if lock_switch == 0:
            #IR detected
            if GPIO.input(pin_IR) == 1:
                IR_cnt += 1
            
            #servo
            if IR_cnt >= 10:
                print("lock", IR_cnt)

                pi.set_servo_pulsewidth(pin_servo_lock, 1800)
                pi.set_servo_pulsewidth(pin_servo_open, 800)
                time.sleep(1)

                lock_switch = 1
                IR_cnt = 0

        #open
        #print(switch_cnt)
        elif lock_switch == 1:
            if AVG_bpm >= 100 or step_AVG > 1000:
                print("open", switch_cnt)

                pi.set_servo_pulsewidth(pin_servo_lock, 800)
                time.sleep(0.5)

                pi.set_servo_pulsewidth(pin_servo_open, 1800)
                time.sleep(0.5)

                pi.set_servo_pulsewidth(pin_servo_open, 800)
                time.sleep(0.5)

                lock_switch = 0
                switch_cnt = 0

        #pedometer
        time.sleep(0.1)
        print(IR_cnt, switch_cnt, lock_switch)

except KeyboardInterrupt:
    # switch servo off
    pi.set_servo_pulsewidth(pin_servo_lock, 0)
    pi.set_servo_pulsewidth(pin_servo_open, 0)
    pi.stop()

GPIO.cleanup