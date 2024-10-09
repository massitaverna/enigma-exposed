from enigma import Enigma


if __name__ == "__main__":
    machine = Enigma()
    while True:
        m = input("Provide input: ")
        print(machine.encrypt(m))