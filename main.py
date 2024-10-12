import logging

from enigma import Enigma


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    machine = Enigma()
    while True:
        m = input("Provide input: ")
        print(machine.encrypt(m))