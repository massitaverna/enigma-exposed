import logging
import os

from lib import Enigma


if __name__ == "__main__":
    log_level = os.environ.get("LOG_LEVEL", logging.INFO)
    logging.basicConfig(level=log_level)

    machine = Enigma()
    while True:
        m = input("Provide input: ")
        print(machine.encrypt(m))