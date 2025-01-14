import customtkinter as ctk
import time
import pyautogui
import random
from threading import Thread
from datetime import datetime, timedelta
import pytz  # For time zone support

# Typing function with errors, delays, and random stops
def realistic_typing(text, error_rate):
    total_chars = len(text.replace(" ", ""))  # Total characters to type (excluding spaces)
    start_time = time.time()
    typed_chars = 0
    time_since_last_pause = 0

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

# Waiting label
waiting_label = ctk.CTkLabel(scrollable_frame, text="Waiting to start...", font=("Arial", 18))
waiting_label.pack(pady=20)

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

# WPM Output Label
wpm_label = ctk.CTkLabel(scrollable_frame, text="Target WPM: 30")
wpm_label.pack(pady=10)

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

# Add Progress Bar
progress_bar = ctk.CTkProgressBar(scrollable_frame, width=400)
progress_bar.pack(pady=10)
progress_bar.set(0)  # Initialize to 0%

# Add Timer Label
timer_label = ctk.CTkLabel(scrollable_frame, text="Elapsed Time: 0:00", font=("Arial", 14))
timer_label.pack(pady=10)

# Function to update progress and timer
def update_progress_and_time(typed_chars, total_chars, start_time):
    # Update progress bar
    progress = typed_chars / total_chars if total_chars > 0 else 0
    progress_bar.set(progress)

    # Update timer
    elapsed_seconds = int(time.time() - start_time)
    elapsed_time = str(timedelta(seconds=elapsed_seconds))  # Convert to H:MM:SS
    hours, minutes, *_ = elapsed_time.split(":")  # Extract hours and minutes
    timer_label.configure(text=f"Elapsed Time: {int(hours)}:{minutes.zfill(2)}")  # Format to H:MM

# Start GUI loop
root.mainloop()