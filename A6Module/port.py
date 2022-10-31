import glob
import sys
import time

import serial


def auto_detect_port():
    if "linux" in sys.platform:
        ports = glob.glob("/dev/ttyUSB*")

        if not ports:
            ports = glob.glob("/dev/ttyACM*")
    elif "darwin" in sys.platform:
        ports = glob.glob("/dev/tty.usbserial*")

        if not ports:
            ports = glob.glob("/dev/tty.usbmodem*")
    else:
        raise Exception("Unsupported system")

    if ports:
        return ports[0]
    else:
        raise Exception("No ports found")


def ping_port(port):
    current_time = time.time()

    while time.time() - current_time < 5:
        port.write("AT\r")
        print("Waiting for response...")
        response = port.read()
        if response:
            print(f"Response: {response}")
            break
        time.sleep(0.1)

    raise Exception("No response")


# noinspection PyUnusedLocal
class SerialPort:
    def __init__(self, port=None, auto_detect=True, ping=False, **kwargs):
        if auto_detect:
            try:
                port = auto_detect_port()
            except Exception as e:
                raise e
            else:
                print(f"Auto-detected port. Running on {port}\n")

        if ping:
            ping_port(port)

        _ser = serial.Serial(
            port=port,
            baudrate="115200",
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=0.1,
            xonxoff=False,
            rtscts=False,
            dsrdtr=False,
        )

        self.port = _ser
