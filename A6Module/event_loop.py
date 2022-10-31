import threading


class EventLoop:
    def __init__(self, _module):
        self.module = _module
        self.running = True

    def run(self):
        print("Available commands: call, sms, wait, hang, off, exit")
        while self.running:
            command = input("Enter command: ")
            if command == "call":
                number = input("Enter number: ")
                self.module.call(number)
            elif command == "sms":
                number = input("Enter number: ")
                message = input("Enter message: ")
                self.module.send_sms(number, message)
            elif command == "wait":
                threading.Thread(target=self.module.wait_for_call).start()
            elif command == "hang":
                self.module.hang_up()
            elif command == "off":
                self.module.turn_off()
                self.running = False
            elif command == "exit":
                self.running = False
            elif command == "help":
                print("Available commands: call, sms, wait, hang, off, exit")
            else:
                print("Unknown command")
