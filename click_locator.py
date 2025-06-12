import pynput.mouse
import time

time.sleep(5)
mouse = pynput.mouse.Controller()
print(mouse.position)
