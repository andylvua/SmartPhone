from A6Module import GSMModule, SerialPort, EventLoop

if __name__ == "__main__":
    module = GSMModule(SerialPort(auto_detect=True))

    loop = EventLoop(module)

    try:
        loop.run()
    except KeyboardInterrupt:
        pass
    finally:
        module.close()
