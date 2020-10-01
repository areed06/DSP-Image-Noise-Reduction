# ___ Importing Modules ___
import tkinter as tk
from tkinter import ttk, filedialog
import getpass
from PIL import Image

# user-created modules
import settings


# ___ Functions ___
def get_image_file():
    """User searches and selects image file to be analyzed, the file is then opened"""

    global raw_image  # raw_image object (Python Image Library)

    # opens file browsing window and obtains file path for selected image
    file_path = filedialog.askopenfilename(initialdir=f'C:\\Users\\{user}\\Documents',
                                           title='Select an Image to De-Noise',
                                           filetypes=settings.supported_files)

    # for debugging
    if file_path:
        raw_image = Image.open(file_path)
        print(f"File Opened: {file_path}")

    else:
        print("No file was opened.")


# ___ User Interface Code ___

root = tk.Tk()  # main root
root.title(f"Image De-Noise v{settings.build_num}")
root.iconbitmap(default='transparent.ico')  # sets window icon (top left corner)
root.geometry("800x500")
root.minsize(settings.min_window_width, settings.min_window_height)
root.grid_columnconfigure((0, 1), weight=1)
root.grid_rowconfigure(3, weight=1)

# ttk style configurations
button_sty = ttk.Style()
button_sty.configure('my.TButton', font=(settings.def_font, settings.button_font_size))

# frame contains primary interactive widgets
frame1 = tk.Frame(root, highlightbackground='black', highlightthickness=1)
frame1.grid(row=1, columnspan=2, pady=10)

# frame contains preview of image (before)
frame2 = tk.Frame(root, highlightbackground='black', highlightthickness=1)
frame2.grid(row=3, column=0, padx=20, pady=20, sticky='NSWE')

# frame contains preview of image (after)
frame3 = tk.Frame(root, highlightbackground='black', highlightthickness=1)
frame3.grid(row=3, column=1, padx=20, pady=20, sticky='NSWE')

# Button to browse for image file name
file_input = ttk.Button(frame1, text='Browse Files', style='my.TButton', command=get_image_file)
file_input.grid(row=0, column=0, padx=10, pady=10)

# Drop down menu for selecting de-noise type
denoise_type_select = ttk.Combobox(frame1, state='readonly', width=25, values=settings.available_modes)
denoise_type_select.grid(row=0, column=1, padx=10, pady=10)
denoise_type_select.set("--Select De-Noise Type--")

# Button to start de-noising algorithm
denoise_action = ttk.Button(frame1, text='Start De-Noise', style='my.TButton')
denoise_action.grid(row=0, column=2, padx=10, pady=10)

# Button for accessing user alterable settings
user_settings = ttk.Button(root, text='Settings', style='my.TButton')
user_settings.grid(row=0, column=0, padx=10, pady=10, sticky='W')

# Region to display before image
before_image = tk.Canvas(frame2, width=300, height=300)
before_image.grid(row=0, column=0)

# label for before image
before_label = ttk.Label(root, text='Image Before')
before_label.grid(row=2, column=0)
before_label.config(font=("Segoe UI", 12))

# Region to display after image
after_image = tk.Canvas(frame3, width=300, height=300)
after_image.grid(row=0, column=0)

# label for after image
after_label = ttk.Label(root, text='Image After')
after_label.grid(row=2, column=1)
after_label.config(font=("Segoe UI", 12))


# ___ Main Program Code ___
user = getpass.getuser()
root.mainloop()  # runs UI window
