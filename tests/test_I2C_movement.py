import smbus
import time

# Remplacer 0 par 1 si nouveau Raspberry
bus = smbus.SMBus(1)
address = 0x12

print ("Send Move Forward")
bus.write_byte(address, 1)

time.sleep(5)

print("Send Move Backward")
bus.write_byte(address, 2)

time.sleep(5)

print("Send Move to Left")
bus.write_byte(address, 3)

time.sleep(5)

print("Send Move to Right")
bus.write_byte(address, 4)

time.sleep(5)

print("Stop")
bus.write_byte(address, 0)
