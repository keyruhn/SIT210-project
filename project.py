# Libraries
import RPi.GPIO as GPIO
import time

# Set the GPIO pins
INTERVAL = 5 
GPIO_ECHO = 17 
GPIO_TRIG = 4 
LED = 26 
pwm = None


def distanceInt():
    print("Printing distance measurement from sensor...")
    GPIO.setmode(GPIO.BCM) #Chose Broadcom chip-specific number. 
    GPIO.setup(GPIO_ECHO, GPIO.IN) #Sets echo as input
    GPIO.setup(GPIO_TRIG, GPIO.OUT) #Sets trig as output
    
    
    
def distanceStart():
    GPIO.output(GPIO_TRIG, True) # Sets trig to HIGH
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIG, False) #Sets trig to low after 0.01ms to LOW
    
    while GPIO.input(GPIO_ECHO) == 0:
        sensor_start = time.time()
    
    
    while GPIO.input(GPIO_ECHO) == 1:
        sensor_end = time.time()
    
    # Time difference between start and end
    sensor_duration = sensor_end - sensor_start
    distance = sensor_duration * 17150 
    distance = round(distance, 2) 
    
    return distance

def ledStart():
    global pwm
    GPIO.setup(LED, GPIO.OUT)
    pwm = GPIO.PWM(LED, 60)
    
    pwm.start(0)
    for i in range(4): #LED flashes 4 times
        
        for i in range(101):
            
            pwm.ChangeDutyCycle(i)
            time.sleep(0.002)
            
        for i in range(100, -1, -1):
            pwm.ChangeDutyCycle(i)
            time.sleep(0.002)
    pwm.stop()


try:
    distanceInt()
    while True:
        distance = distanceStart()
        print("Distance to sensor:{}cm".format(distance))
        if distance < 10:
            ledStart()
        time.sleep(INTERVAL)
except KeyboardInterrupt:
    if pwm != None:
        pwm.stop
    print("Measurement cancelled due to keyboard input")
    GPIO.cleanup()