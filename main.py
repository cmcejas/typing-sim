import customtkinter as ctk
import time
import pyautogui
import random
from threading import Thread
from datetime import datetime, timedelta
import pytz  # For time zone support
import tkinter.filedialog

# Typing function with errors, delays, and random stops
def realistic_typing(text, error_rate):
    total_chars = len(text.replace(" ", ""))  # Total characters to type (excluding spaces)
    start_time = time.time()
    typed_chars = 0
    time_since_last_pause = 0

    # Disable text area editing while typing
    text_area.configure(state="disabled")

    for line in text.splitlines():
        for char in line:
            if stop_typing:
                print("Typing stopped by user.")
                return

            # Use updated global WPM value after confirmation
            current_wpm = global_wpm
            typing_delay = current_wpm / (current_wpm * 200 * random.uniform(0.8, 1.1))  # Delay per character based on WPM (5 characters per word)

            # Add random stops every 15-20 seconds
            elapsed_time = time.time() - start_time
            if elapsed_time - time_since_last_pause >= random.randint(15, 20):  # Check every 15-20 seconds
                time.sleep(random.uniform(1, 3))  # Random pause between 1-3 seconds
                time_since_last_pause = elapsed_time  # Reset timer after pause

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
            wpm = (typed_chars / 5) / (elapsed_time / 60)  # Calculate WPM (5 characters per word)
            update_wpm(wpm)
            
            # Update progress bar and time remaining
            progress = typed_chars / total_chars
            progress_bar.set(progress)
            remaining_time = (elapsed_time / typed_chars) * (total_chars - typed_chars)
            update_time_remaining(remaining_time)
        pyautogui.press('enter')

    # Re-enable text area editing after typing
    text_area.configure(state="normal")

# Function to type a character
def type_character(char):
    try:
        if char == " ":
            pyautogui.press('space')
        elif char == "'":  # Single quote
            pyautogui.press("'")
        elif char == '"':  # Double quote
            pyautogui.press('"')
        elif char == "-":  # Hyphen
            pyautogui.press("-")
        elif char == "_":  # Underscore
            pyautogui.hotkey("shift", "-")  # Shift + Hyphen
        elif char == "!":  # Exclamation mark
            pyautogui.hotkey("shift", "1")  # Shift + 1
        elif char == "?":  # Question mark
            pyautogui.hotkey("shift", "/")  # Shift + Slash
        elif char == ".":  # Period
            pyautogui.press(".")
        elif char == ",":  # Comma
            pyautogui.press(",")
        elif char == ":":  # Colon
            pyautogui.hotkey("shift", ";")  # Shift + Semicolon
        elif char == ";":  # Semicolon
            pyautogui.press(";")
        elif char == "/":  # Forward slash
            pyautogui.press("/")
        elif char == "@":  # At symbol
            pyautogui.hotkey("shift", "2")  # Shift + 2
        elif char == "#":  # Hash symbol
            pyautogui.hotkey("shift", "3")  # Shift + 3
        elif char == "$":  # Dollar sign
            pyautogui.hotkey("shift", "4")  # Shift + 4
        elif char == "%":  # Percent sign
            pyautogui.hotkey("shift", "5")  # Shift + 5
        elif char == "&":  # Ampersand
            pyautogui.hotkey("shift", "7")  # Shift + 7
        elif char == "(":  # Opening parenthesis
            pyautogui.hotkey("shift", "9")  # Shift + 9
        elif char == ")":  # Closing parenthesis
            pyautogui.hotkey("shift", "0")  # Shift + 0
        elif char == "=":  # Equals sign
            pyautogui.press("=")
        elif char == "+":  # Plus sign
            pyautogui.hotkey("shift", "=")  # Shift + Equals
        else:
            pyautogui.write(char)  # For regular characters, just type normally
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
    waiting_label.pack_forget()  # Hide the waiting label when typing starts
    countdown(5)  # 5 second countdown before typing starts
    text = text_area.get("1.0", "end-1c")  # Get the input text from the text area
    error_rate = error_slider.get() / 100  # Convert to a decimal value

    # Run the typing function in a separate thread to avoid blocking the main thread
    typing_thread = Thread(target=realistic_typing, args=(text, error_rate))
    typing_thread.start()

# Function for countdown
def countdown(seconds):
    for i in range(seconds, 0, -1):
        countdown_label.configure(text=f"Starting in {i} seconds...")    
        root.update()
        time.sleep(1)
    waiting_label.pack_forget()  # Hide the waiting label once countdown begins

# Function to stop typing
def stop_typing_function():
    global stop_typing
    stop_typing = True
    waiting_label.pack(pady=20)  # Re-show the waiting label when stopped
    countdown_label.configure(text="Waiting to start...")  # Reset countdown label text

# Function to update WPM label
def update_wpm(wpm):
    wpm_label.configure(text=f"WPM: {int(wpm)}")

# Function to update global WPM value from user input
def update_wpm_parameters(val):
    global global_wpm
    global_wpm = int(val)
    wpm_label.configure(text=f"Target WPM: {global_wpm}")  # Update the label based on slider value

# Function to update the error rate display
def update_error_rate_label(val):
    error_rate_label.configure(text=f"Error Rate: {int(float(val))}%")


# Function to update the time remaining label
def update_time_remaining(remaining_time):
    minutes = int(remaining_time // 60)
    seconds = int(remaining_time % 60)
    time_remaining_label.configure(text=f"Time remaining: {minutes:02d}:{seconds:02d}")

# Function to open a file dialog and load the file content into the text area
def upload_file():
    file_path = tkinter.filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])  # Only allow text files
    if file_path:
        try:
            with open(file_path, 'r') as file:
                file_content = file.read()
                text_area.delete("1.0", "end")  # Clear any existing text
                text_area.insert("1.0", file_content)  # Insert the file content into the text area
        except Exception as e:
            print(f"Error reading the file: {e}")

# Create the main window
root = ctk.CTk()
root.title("Typing Simulator")
root.geometry("800x600")  # Increased window size for better visibility

# Create the sidebar frame (on the left side)
sidebar_frame = ctk.CTkFrame(root, width=200, height=600, corner_radius=10)  # Set width and height to fill vertically
sidebar_frame.pack(side="left", fill="y", padx=10, pady=10)  # Pack it on the left side

# Sidebar content
wpm_label_input = ctk.CTkLabel(sidebar_frame, text="Set Target Typing Speed (WPM):")
wpm_label_input.pack(pady=10)

wpm_slider = ctk.CTkSlider(sidebar_frame, from_=10, to=120, command=update_wpm_parameters)  # WPM slider
wpm_slider.set(global_wpm)  # Set default value of slider
wpm_slider.pack(pady=10)

# Target WPM moved to sidebar
wpm_label = ctk.CTkLabel(sidebar_frame, text=f"Target WPM: {global_wpm}")
wpm_label.pack(pady=10)  # Add to sidebar

# Error Rate Percent Display
error_rate_label = ctk.CTkLabel(sidebar_frame, text="Error Rate: 10%")  # Default error rate display
error_rate_label.pack(pady=10)

# Error Slider
error_slider = ctk.CTkSlider(sidebar_frame, from_=0, to=30, command=update_error_rate_label)  # Update label on slider change
error_slider.set(10)
error_slider.pack(pady=10)

# Create a scrollable frame for the main content
scrollable_frame = ctk.CTkScrollableFrame(root)
scrollable_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)  # Main content now on the right side

# Title Card at the top of the window
title_card = ctk.CTkLabel(scrollable_frame, text="Typing Simulator", font=("Arial", 24, "bold"), fg_color="grey", width=800, height=50, corner_radius=10)
title_card.pack(side="top", fill="x", pady=10)

# Waiting label
waiting_label = ctk.CTkLabel(scrollable_frame, text="Waiting to start...", font=("Arial", 18))
waiting_label.pack(pady=20)

# Upload File Button
upload_button = ctk.CTkButton(scrollable_frame, text="Upload File", command=upload_file)
upload_button.pack(pady=5)

# Text input area with blue border
text_area = ctk.CTkTextbox(scrollable_frame, height=200, width=400, border_color="blue", border_width=2)  # Blue outline for the text area
text_area.pack(pady=10)

# Start Button
start_button = ctk.CTkButton(scrollable_frame, text="Start Typing", command=start_typing)
start_button.pack(pady=5)

# Stop Button
stop_button = ctk.CTkButton(scrollable_frame, text="Stop Typing", command=stop_typing_function)
stop_button.pack(pady=5)

# Countdown label
countdown_label = ctk.CTkLabel(scrollable_frame, text="Starting in 5 seconds...")
countdown_label.pack(pady=10)

# Time Remaining Label
time_remaining_label = ctk.CTkLabel(scrollable_frame, text="Time remaining: 00:00")
time_remaining_label.pack(pady=10)

# Progress Bar
progress_bar = ctk.CTkProgressBar(scrollable_frame, width=400)
progress_bar.pack(pady=20)

# Function to toggle the sidebar and adjust the hamburger button's position
def toggle_sidebar():
    if sidebar_frame.winfo_ismapped():  # Check if the sidebar is currently visible
        sidebar_frame.pack_forget()  # Hide the sidebar
        hamburger_button.place(relx=0.95, y=10, anchor="ne")  # Move hamburger button back to the right
    else:
        sidebar_frame.pack(side="left", fill="y", padx=10, pady=10)  # Show the sidebar
        hamburger_button.place(relx=0.95, y=10, anchor="ne")  # Keep hamburger button on the right side

# Hamburger Button positioned at the top-right (initially)
hamburger_button = ctk.CTkButton(
    root, 
    text="☰", 
    command=toggle_sidebar, 
    width=50,        # Set custom width
    height=50,       # Set custom height
    font=("Arial", 20),  # Adjust font size
    corner_radius=10  # Optional: Set corner radius for rounded corners
)

hamburger_button.place(relx=0.95, y=10, anchor="ne")  # Initial position of the button on the top-right

# Start GUI loop
root.mainloop()
