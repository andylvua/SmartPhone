import time


class GSMModule:
    def __init__(self, _ser, pin=None):
        self.ser = _ser.port

        self.in_waiting = 0
        self.last_read = time.time()

        if not self.check_sim():
            raise Exception("No SIM card")

        if pin:
            if not self.check_pin():
                self.enter_pin(pin)
                time.sleep(1)
                self.read()
                if not self.check_pin():
                    raise Exception("Incorrect PIN")

        if not self.check_pin():
            raise Exception("PIN required, please specify corresponding argument")

        if not self.check_network():
            raise Exception("No network")

    def check_sim(self):
        self.write("AT+CPIN?\r")
        response = self.read().decode()

        return "+CME ERROR:10" not in response

    def check_pin(self):
        self.write("AT+CPIN?\r")
        response = self.read().decode()

        return "+CPIN:READY" in response

    def enter_pin(self, pin):
        self.write(f"AT+CPIN=\"{pin}\"\r")

    def check_network(self):
        self.write("AT+CREG?\r")
        response = self.read().decode()

        return "1" in response or "5" in response

    def write(self, data):
        self.ser.write(data.encode())

    def flush(self):
        self.ser.flush()

    def read(self):
        return self.ser.readall()

    def close(self):
        self.ser.close()

    def turn_off(self):
        self.write("AT+CPOF\r")

    def accept_call(self):
        self.write("ATA\r")
        time.sleep(0.1)

        self.last_read = time.time()
        while time.time() - self.last_read < 5:
            response = self.read().decode()
            if "CONNECT" in response:
                print("Call accepted")
                return

        print("Something went wrong. Call not accepted")

    def hang_up(self):
        self.write("ATH\r")

    def call(self, number):
        self.write("ATD" + number + ";\r")

        self.in_waiting = 1
        print("Waiting for call...")

        while True:
            response = self.read().decode()

            if "NO CARRIER" in response:
                return "NO CARRIER"

            if "BUSY" in response:
                return "BUSY"

            if "NO ANSWER" in response:
                return "NO ANSWER"

            if "+CIEV: \"SOUNDER\",0" in response:
                print("Call accepted")

            if "+CIEV: \"SOUNDER\",1" in response:
                print("Calling...")

            if "+CIEV: \"CALL\",0" in response:
                return "Call ended"

    def send_sms(self, number, message):
        self.write(f"AT+CMGF=1\r")
        time.sleep(0.1)
        assert "OK" in self.read().decode()

        self.write(f"AT+CMGS=\"{number}\"\r")
        time.sleep(0.1)
        assert ">" in self.read().decode()

        self.write(f"{message}\x1A")

        self.last_read = time.time()
        while time.time() - self.last_read < 5:
            response = self.read().decode()
            if "OK" in response:
                print("SMS sent")
                break

        self.write("AT+CMGF=0\r")
        return

    def wait_for_call(self):
        print("Waiting for call...")
        while True:
            response = self.read().decode()
            if "RING" in response:

                accept = input("Incoming call. Accept? (y/n) ")

                if accept == "y":
                    self.accept_call()

                    hang_up = input("Call accepted. When you're done, press H to hang up: ")

                    if hang_up == "H":
                        self.hang_up()
                        return
                    else:
                        return
                else:
                    self.hang_up()
                    return
