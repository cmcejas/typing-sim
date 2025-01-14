import tkinter as tk
import time
import pyautogui
import random
from threading import Thread

# Typing function with errors and delays
def realistic_typing(text, error_rate):
    total_chars = len(text.replace(" ", ""))  # Total characters to type (excluding spaces)
    start_time = time.time()
    typed_chars = 0

    for line in text.splitlines():
        for char in line:
            if stop_typing:
                print("Typing stopped by user.")
                return

            # Use updated global WPM value after confirmation
            current_wpm = global_wpm
            typing_delay = current_wpm / (current_wpm *200*random.uniform(.8,1.1))  # Delay per character based on WPM (5 characters per word)
            
            # Check for an error and simulate a typo
            if random.random() < error_rate:  # Simulate a typo with error_rate probability
                typo_char = random_typo(char)
                if typo_char:
                    type_character(typo_char)
                    time.sleep(typing_delay)
                    pyautogui.press('backspace')
            type_character(char)
            time.sleep(typing_delay)
            typed_chars += 1

            # Calculate WPM and update the label
            elapsed_time = time.time() - start_time
            wpm = (typed_chars / 5) / (elapsed_time / 60)  # Calculate WPM (5 characters per word)
            update_wpm(wpm)
        
        pyautogui.press('enter')

# Function to type a character
def type_character(char):
    try:
        if char == " ":
            pyautogui.press('space')
        else:
            pyautogui.write(char)
    except Exception as e:
        print(f"Error typing character {char}: {e}")

# Function to generate random typos
def random_typo(char):
    keyboard_map = {
        'q': ['w', 'a'],
        'w': ['q', 'e', 's'],
        'e': ['w', 'r', 'd'],
        'r': ['e', 't', 'f'],
        't': ['r', 'y', 'g'],
        'y': ['t', 'u', 'h'],
        'u': ['y', 'i', 'j'],
        'i': ['u', 'o', 'k'],
        'o': ['i', 'p', 'l'],
        'p': ['o', ';'],
        'a': ['q', 's', 'z'],
        's': ['a', 'w', 'd', 'x'],
        'd': ['s', 'e', 'f', 'c'],
        'f': ['d', 'r', 'g', 'v'],
        'g': ['f', 't', 'h', 'b'],
        'h': ['g', 'y', 'j', 'n'],
        'j': ['h', 'u', 'k', 'm'],
        'k': ['j', 'i', 'l'],
        'l': ['k', 'o'],
        'z': ['a', 'x'],
        'x': ['z', 's', 'c'],
        'c': ['x', 'd', 'v'],
        'v': ['c', 'f', 'b'],
        'b': ['v', 'g', 'n'],
        'n': ['b', 'h', 'm'],
        'm': ['n', 'j'],
        ' ': [' '],
    }
    if char.lower() in keyboard_map:
        return random.choice(keyboard_map[char.lower()])
    return None

# Variable to control typing state
stop_typing = False

# Global variable for WPM
global_wpm = 30  # Default WPM value

# Function to start typing after countdown
def start_typing():
    global stop_typing
    stop_typing = False
    countdown(5)  # 5 second countdown before typing starts
    text = text_area.get("1.0", "end-1c")  # Get the input text from the text area
    error_rate = error_slider.get() / 100  # Convert to a decimal value

    # Run the typing function in a separate thread to avoid blocking the main thread
    typing_thread = Thread(target=realistic_typing, args=(text, error_rate))
    typing_thread.start()

# Function for countdown
def countdown(seconds):
    for i in range(seconds, 0, -1):
        countdown_label.config(text=f"Starting in {i} seconds...")
        root.update()
        time.sleep(1)

# Function to stop typing
def stop_typing_function():
    global stop_typing
    stop_typing = True

# Function to update WPM label
def update_wpm(wpm):
    wpm_label.config(text=f"WPM: {int(wpm)}")

# Function to update global WPM value from user input
def update_wpm_parameters():
    global global_wpm
    try:
        user_wpm = int(wpm_input.get())
        if user_wpm < 10:
            user_wpm = 10  # Ensure a minimum WPM of 10
        elif user_wpm > 120:
            user_wpm = 120  # Ensure a maximum WPM of 120
        global_wpm = user_wpm
        wpm_label.config(text=f"Target WPM: {global_wpm}")
    except ValueError:
        print("Invalid WPM input. Please enter a number.")
        wpm_input.delete(0, tk.END)

# Create GUI
root = tk.Tk()
root.title("Typing Simulator")

# Text input area
text_area = tk.Text(root, height=15, width=60)
text_area.pack(pady=10)

# Start Button
start_button = tk.Button(root, text="Start Typing", command=start_typing)
start_button.pack(pady=5)

# Stop Button
stop_button = tk.Button(root, text="Stop Typing", command=stop_typing_function)
stop_button.pack(pady=5)

# Countdown label
countdown_label = tk.Label(root, text="Starting in 5 seconds...")
countdown_label.pack(pady=10)

# WPM Input
wpm_label_input = tk.Label(root, text="Set Target Typing Speed (WPM):")
wpm_label_input.pack()

wpm_input = tk.Entry(root)
wpm_input.pack()

# Confirm Button
confirm_button = tk.Button(root, text="Confirm WPM", command=update_wpm_parameters)
confirm_button.pack(pady=5)

# Error Slider
error_label = tk.Label(root, text="Error Rate (%):")
error_label.pack()
error_slider = tk.Scale(root, from_=0, to=30, orient=tk.HORIZONTAL)
error_slider.set(10)  # Default Error Rate
error_slider.pack(pady=10)

# WPM Output Label
wpm_label = tk.Label(root, text="Target WPM: 30")
wpm_label.pack(pady=10)

# Start GUI loop
root.mainloop()