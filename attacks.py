from enigma import Enigma

if __name__ == "__main__":
    # The attacker can import the class Enigma and use it
    e = Enigma()
    ptx = e.decrypt("somethingsecret")
    print(ptx)