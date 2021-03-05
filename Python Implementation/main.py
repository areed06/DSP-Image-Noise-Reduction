# ___ Importing Modules ___
import tkinter as tk
from tkinter import ttk, filedialog
from numpy import asarray
from PIL import Image
from copy import deepcopy
import threading
import getpass
import time

# user-created modules
from settings import Settings
from algorithms import *


# ___ Functions ___
class NoiseReduction:
    def __init__(self):
        self.file_path = ""
        self.raw_image = None
        self.raw_data = None
        self.copy_raw_data = None
        self.save_directory = ""
        self.save_path = ""
        self.raw_data_exists = False

    def open_raw_image(self):
        """User searches and selects image file to be analyzed, the file is then opened"""

        # opens file browsing window and obtains file path for selected image
        self.file_path = filedialog.askopenfilename(initialdir=f'C:\\Users\\{user}\\Documents',
                                                    title='Select an Image to De-Noise',
                                                    filetypes=settings.supported_files)

        # creates PIL Image and Numpy objects if file path exists
        if self.file_path:
            print(f"File Opened: {self.file_path}")
            self.raw_image = Image.open(self.file_path)  # PIL image
            self.raw_image = self.raw_image.convert("L")  # convert to grayscale to simplify de-noise
            self.raw_data = asarray(self.raw_image)  # numpy array of raw image data
            self.copy_raw_data = deepcopy(self.raw_data)
            self.raw_data_exists = True

        else:
            self.raw_data_exists = False
            print("No file was opened.")

    def save_output_file(self):
        """Pop-up window which allows user to save output file"""

        def directory_select():
            """Opens window to select desired file destination"""

            self.save_directory = filedialog.askdirectory(initialdir=f'C:\\Users\\{user}\\Documents',
                                                          title='Select Destination Folder')

            folder_path["text"] = self.save_directory

        def proceed_with_save():
            """Takes user's directory and file name and saves output"""

            try:
                self.save_path = self.save_directory + "\\" + file_name.get()

            except NameError:
                print("Unable to create save path.")
                return  # nothing happens file is improper

            try:
                less_noisy_image = Image.fromarray(self.copy_raw_data)
                less_noisy_image.save(self.save_path)

            except ValueError:
                print("Unable to save output.")
                return

        # Toplevel widget
        save_config = tk.Toplevel()

        # Button for selecting directory
        dest_dir = ttk.Button(save_config, text='Select Folder', command=directory_select)
        dest_dir.grid(row=0, column=0, padx=10, pady=10, sticky="WE")

        # file name entry
        file_name = ttk.Entry(save_config)  # input for file name
        file_name.grid(row=1, column=0, padx=10, pady=10, sticky="WE")

        # proceed button
        save = ttk.Button(save_config, text='Proceed', command=proceed_with_save)  # proceed with de-noising
        save.grid(row=2, column=0, padx=10, pady=10, sticky="WE")

        # label to show path to directory
        folder_path = ttk.Label(save_config, text=self.save_directory)
        folder_path.grid(row=3, column=0, padx=10, pady=10, sticky="WE")

    def apply_denoise(self):
        """Applies selected de-noising algorithm to image."""

        # de-noising functions
        def blocking_code():
            start_time = time.time()

            # status indicator goes red to reflect system processing state
            status['background'] = 'red'
            status['text'] = 'Processing...'

            # disables buttons to avoid simultaneous de-noising
            file_input["state"] = "disabled"
            denoise_action["state"] = "disabled"

            if selected_mode == "Salt & Pepper" and settings.mode_activations[selected_mode] == 1:
                save_output = True
                self.copy_raw_data = salt_pepper_denoise(self.copy_raw_data, settings)

            elif selected_mode == "Gaussian" and settings.mode_activations[selected_mode] == 1:
                # insert algorithm function
                save_output = True
                print("Gaussian")

            elif selected_mode == "Poisson" and settings.mode_activations[selected_mode] == 1:
                # insert algorithm function
                save_output = True
                print("Poisson")

            elif selected_mode == "Adam's Custom Algorithm" and settings.mode_activations[selected_mode] == 1:
                # insert algorithm function
                save_output = True
                print("Custom")

            else:
                save_output = False
                print("Invalid mode or no mode was selected.")
                status['background'] = 'white'  # default status color
                status['text'] = 'Status'  # default status text

            # total time taken to de-noise image
            elapsed = round((time.time() - start_time), 2)
            print(f"Process complete at time {elapsed}s")

            # re-enables buttons
            file_input["state"] = "normal"
            denoise_action["state"] = "normal"

            if save_output:
                # indicates de-noising has successfully completed
                status['background'] = 'green'
                status['text'] = 'Complete!'

                self.save_output_file()

        # checks for selected mode in ComboBox widget
        selected_mode = denoise_type_select.get()

        # checks to ensure raw data file exists
        if not self.raw_data_exists:
            print("Cannot apply de-noise without image file...")
            return

        if selected_mode in settings.available_modes:

            # creates new thread to execute de-noising through
            denoise_thread = threading.Thread(target=blocking_code, daemon=True)
            denoise_thread.start()


# ___ User Interface Code ___
denoise = NoiseReduction()  # creates instance of NoiseReduction class
settings = Settings()

root = tk.Tk()  # main root
root.title(f"Image De-Noise v{settings.build_num}")
root.iconbitmap(default='transparent.ico')  # sets window icon (top left corner)
root.geometry("800x500")
root.minsize(settings.min_window_width, settings.min_window_height)
root.grid_columnconfigure((0, 1), weight=1, uniform='half')
root.grid_rowconfigure(3, weight=1)

# ttk style configurations
button_sty = ttk.Style()
button_sty.configure('my.TButton', font=(settings.def_font, settings.button_font_size))

# frame contains primary interactive widgets
frame1 = tk.Frame(root, highlightbackground='black', highlightthickness=1)
frame1.grid(row=1, columnspan=2, pady=10)

# Button to browse for image file name
file_input = ttk.Button(frame1, text='Browse Files', style='my.TButton', command=denoise.open_raw_image)
file_input.grid(row=0, column=0, padx=10, pady=10)

# Drop down menu for selecting de-noise type
denoise_type_select = ttk.Combobox(frame1, state='readonly', width=25, values=settings.available_modes)
denoise_type_select.grid(row=0, column=1, padx=10, pady=10)
denoise_type_select.set("--Select De-Noise Type--")

# Button to start de-noising algorithm
denoise_action = ttk.Button(frame1, text='Start De-Noise', style='my.TButton', command=denoise.apply_denoise)
denoise_action.grid(row=0, column=2, padx=10, pady=10)

# Button for accessing user alterable settings
user_settings = ttk.Button(root, text='Settings', style='my.TButton')
user_settings.grid(row=0, column=0, padx=10, pady=10, sticky='W')

# Label to denote status of de-noise
status = ttk.Label(root, width=15, borderwidth=1, background='white', text="Status")
status.grid(row=0, column=1, padx=10, pady=10, sticky='E')
status.configure(anchor='center')

# label for before image
before_label = ttk.Label(root, text='Image Before')
before_label.grid(row=2, column=0)
before_label.config(font=("Segoe UI", 12), anchor='center')

# frame to contain before image
before_image = tk.Frame(root, highlightbackground='black', highlightthickness=1)
before_image.grid(row=3, column=0, padx=10, pady=15, sticky='nsew')

# label for after image
after_label = ttk.Label(root, text='Image After')
after_label.grid(row=2, column=1)
after_label.config(font=("Segoe UI", 12), anchor='center')

# frame to contain after image
after_image = tk.Frame(root, highlightbackground='black', highlightthickness=1)
after_image.grid(row=3, column=1, padx=10, pady=15, sticky='nsew')

# ___ Main Program Code ___
user = getpass.getuser()
root.mainloop()  # runs UI window
