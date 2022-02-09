import pyfirmata
import time
if __name__ == '__main__':
    board = pyfirmata.Arduino('COM5')
    print("Communication Successfully started")

    def boring():
        while True:
            board.digital[2].write(1)
            time.sleep(1)
            board.digital[2].write(0)
            time.sleep(1)
            board.digital[2].write(1)
            time.sleep(3)

    def crazy():

        while True:
            board.digital[2].write(1)
            time.sleep(0.3)
            board.digital[2].write(0)
            time.sleep(0.3)

crazy()
