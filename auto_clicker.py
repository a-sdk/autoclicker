import time
import math
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, Key, KeyCode

# Farming Buku: 140 detik 
# Farming Chip Defender: 150 detik
# EP - 8: 180 detik
total_sanity = int(input('Sanity Amount: '))
sanity_cost = int(input('Sanity Cost: '))
operation_delay = int(input('Duration: '))
# Define click sequence: (x, y, delay)
click_sequence = [
    (1374, 817, 8.0),  # Build squad
    (1338, 583, operation_delay),  # Start operation, delay based on operation
    (1155, 643, 8.0),  # Claim result
]

# Config
button = Button.left
start_key = Key.f7
pause_key = Key.f8
exit_key = Key.f9
max_loops = math.floor(total_sanity/sanity_cost)  # Number of times to repeat the sequence, based on sanity consumption

mouse = Controller()

class AutoClicker(threading.Thread):
    def __init__(self, sequence, max_loops):
        super().__init__()
        self.sequence = sequence
        self.max_loops = max_loops
        self.clicking = False
        self.active = True
        self.paused = False

    def start_click(self):
        print("[INFO] Clicker Started.")
        print(f"[INFO] Clicker will run {max_loops} time(s)")
        self.clicking = True

    def stop_click(self):
        print("[INFO] Clicker Stopped.")
        self.clicking = False
        
    def pause(self):
        print("[INFO] Clicker Paused.")
        self.paused = True

    def resume(self):
        print("[INFO] Clicker Resumed.")
        self.paused = False

    def exit(self):
        print("[INFO] Clicker Exiting...")
        self.clicking = False
        self.active = False

    def run(self):
        # Interruptible delay
        def interruptible_sleep(seconds, check_interval=0.1):
            slept = 0
            while slept < seconds:
                if not self.clicking or not self.active:
                    break
                while self.paused:  # wait if paused
                    time.sleep(0.1)
                time.sleep(check_interval)
                slept += check_interval
            
        loop_count = 0
        while self.active and loop_count < self.max_loops:
            if self.clicking:
                print(f"[INFO] Starting loop {loop_count + 1}")
                for x, y, delay in self.sequence:
                    if not self.active:  # ONLY check if user stopped everything
                        break
                    mouse.position = (x, y)
                    mouse.click(button)
                    print(f"[INFO] Clicked at ({x}, {y}), waiting {delay}s")
                    interruptible_sleep(delay)
                loop_count += 1
                print(f"[INFO] Finished loop {loop_count}/{self.max_loops}")
            else:
                time.sleep(0.1)

        self.stop_click()
        print("[INFO] Looping finished or user stopped the clicker.")


clicker = AutoClicker(click_sequence, max_loops)
clicker.start()

def on_press(key):
    if key == start_key:
        if clicker.clicking:
            clicker.stop_click()
        else:
            clicker.start_click()
    elif key == pause_key:
        if not clicker.paused:
            clicker.pause()
        else:
            clicker.resume()
    elif key == exit_key:
        clicker.exit()
        return False


print("[INFO] Press F7 to start. Press F8 to pause/resume. Press F9 to exit.")

with Listener(on_press=on_press) as listener:
    listener.join()
