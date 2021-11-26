import serial
import time
import Adafruit_BBIO.GPIO as GPIO


LED_USR0 = "USR0"
LED_USR1 = "USR1"
LED_USR2 = "USR2"
LED_USR3 = "USR3"

GPIO.setup(LED_USR0, GPIO.OUT)
GPIO.setup(LED_USR1, GPIO.OUT)
GPIO.setup(LED_USR2, GPIO.OUT)
GPIO.setup(LED_USR3, GPIO.OUT)

LED0_ON_ADV_MSG = "10:09:42:6C:65:75:49:4F:20:4C:45:44:20:30:20:4F:4E:"
LED1_ON_ADV_MSG = "10:09:42:6C:65:75:49:4F:20:4C:45:44:20:31:20:4F:4E:"
LED2_ON_ADV_MSG = "10:09:42:6C:65:75:49:4F:20:4C:45:44:20:32:20:4F:4E:"
LED3_ON_ADV_MSG = "10:09:42:6C:65:75:49:4F:20:4C:45:44:20:33:20:4F:4E:"

# Turn off all LEDs
GPIO.output(LED_USR0, GPIO.LOW)
time.sleep(0.1)
GPIO.output(LED_USR1, GPIO.LOW)
time.sleep(0.1)
GPIO.output(LED_USR2, GPIO.LOW)
time.sleep(0.1)
GPIO.output(LED_USR3, GPIO.LOW)
time.sleep(0.1)

print("\nBlueIO BeagleBone Example!\n\n")
connecting_to_dongle = 0
com_input = ""

start_input = 0
valid_input = 0
while start_input == 0:
    com_input = input(
        "Enter Com port of Dongle (default for BeagleBone: '/dev/ttyACM0'):\n>>"
    )
    print("\nComport to use: " + com_input)
    input_continue = input(
        "If your happy with your choice just press Enter to continue the script. Else type E to exit or R to redo your choice. \n>>"
    )
    if input_continue.upper() == "E":
        start_input = 1
    elif input_continue.upper() == "":
        start_input = 1
    elif input_continue.upper() == "R":
        valid_input = 0
        start_input = 0
if input_continue.upper() == "E":
    print("Exiting script...")
    exit()

console = None

while 1:
    try:
        print("Please wait...")
        time.sleep(0.5)
        console.write(str.encode("AT+DUAL"))
        console.write("\r".encode())
        time.sleep(0.5)
        print("Starting Advertising...")
        console.write(str.encode("AT+ADVSTART"))
        console.write("\r".encode())
        time.sleep(0.5)
        led_turn = 0
        # Turn off all LEDs
        GPIO.output(LED_USR0, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(LED_USR1, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(LED_USR2, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(LED_USR3, GPIO.LOW)
        time.sleep(0.1)
        while True:
            if led_turn == 0:
                print("\nTurning LED USR0 ON")
                console.write(str.encode("AT+ADVRESP="))
                console.write(LED0_ON_ADV_MSG.encode())
                console.write("\r".encode())
                GPIO.output(LED_USR0, GPIO.HIGH)
                GPIO.output(LED_USR1, GPIO.LOW)
                GPIO.output(LED_USR2, GPIO.LOW)
                GPIO.output(LED_USR3, GPIO.LOW)
                led_turn = led_turn + 1
            elif led_turn == 1:
                print("\nTurning LED USR1 ON")
                console.write(str.encode("AT+ADVRESP="))
                console.write(LED1_ON_ADV_MSG.encode())
                console.write("\r".encode())
                GPIO.output(LED_USR0, GPIO.LOW)
                GPIO.output(LED_USR1, GPIO.HIGH)
                GPIO.output(LED_USR2, GPIO.LOW)
                GPIO.output(LED_USR3, GPIO.LOW)
                led_turn = led_turn + 1
            elif led_turn == 2:
                print("\nTurning LED USR2 ON")
                console.write(str.encode("AT+ADVRESP="))
                console.write(LED2_ON_ADV_MSG.encode())
                console.write("\r".encode())
                GPIO.output(LED_USR0, GPIO.LOW)
                GPIO.output(LED_USR1, GPIO.LOW)
                GPIO.output(LED_USR2, GPIO.HIGH)
                GPIO.output(LED_USR3, GPIO.LOW)
                led_turn = led_turn + 1
            elif led_turn == 3:
                print("\nTurning LED USR3 ON")
                console.write(str.encode("AT+ADVRESP="))
                console.write(LED3_ON_ADV_MSG.encode())
                console.write("\r".encode())
                GPIO.output(LED_USR0, GPIO.LOW)
                GPIO.output(LED_USR1, GPIO.LOW)
                GPIO.output(LED_USR2, GPIO.LOW)
                GPIO.output(LED_USR3, GPIO.HIGH)
                led_turn = 0

            time.sleep(8)

    except KeyboardInterrupt:
        GPIO.output(LED_USR0, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(LED_USR1, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(LED_USR2, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(LED_USR3, GPIO.LOW)
        time.sleep(0.1)
        print("Exiting script...")
        exit()
    except:
        print("\n\nDongle not connected.\n")
        connecting_to_dongle = 0
        while connecting_to_dongle == 0:
            try:
                print("Trying to connect to dongle...")
                console = serial.Serial(
                    port=com_input,
                    baudrate=57600,
                    parity="N",
                    stopbits=1,
                    bytesize=8,
                    timeout=0,
                )
                if console.is_open.__bool__():
                    connecting_to_dongle = 1
                    print("\n\nConnected to Dongle in port: " + com_input + ".\n")
            except:
                print(
                    "Dongle not found. Retrying connection to port: "
                    + com_input
                    + "..."
                )
                time.sleep(5)
