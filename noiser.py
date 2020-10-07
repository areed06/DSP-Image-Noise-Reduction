import numpy as np
from numpy import asarray
import os
from PIL import Image
from copy import deepcopy


# ___ Functions ___
def add_salt_pepper(image, salt_percent, noise_density):
    """Adds salt and pepper noise to image"""

    # imports image data into np array and copies it to protect original file
    data = asarray(image)
    copy_data = deepcopy(data)

    # proportion of noise that is salt/pepper
    percent_salt = salt_percent
    percent_pepper = 1 - percent_salt

    # total number of desired salt and pepper noisy pixels
    num_salt = np.ceil(noise_density*data.shape[0]*percent_salt)
    num_pepper = np.ceil(noise_density*data.shape[0]*percent_pepper)

    for row in copy_data:
        # adding salt noise
        coords = [np.random.randint(0, column-1, int(num_salt)) for column in row.shape]
        row[coords, :] = 255

        # adding pepper noise
        coords = [np.random.randint(0, column-1, int(num_pepper)) for column in row.shape]
        row[coords, :] = 0

    return copy_data


# ___ Main Code ___
while True:
    path = input("Enter path to image file: ")  # file path to image

    try:
        img = Image.open(path)  # instance of PIL Image object
        break

    except OSError or FileNotFoundError:
        print("File not found.")

# prints available modes for user to choose from
print("\nMode Description:\n"
      "(0) --> Salt and Pepper\n"
      "(1) --> Gaussian Noise\n"
      "(2) --> Poisson Noise\n"
      "(3) --> Speckle Noise\n")

# only permits integer inputs for mode
while True:
    try:
        mode = int(input("Enter desired mode: "))
        break
    except ValueError:
        print("Mode is integer")

# each if statement contains the specific parameters needed for each noise type
if mode == 0:
    slt_pct = float(input("Enter salt noise percentage: "))
    dns = float(input("Enter noise density: \n"))

    # converts numpy array back into PIL image
    noisy_image = Image.fromarray(add_salt_pepper(img, slt_pct, dns))
    save_output = True

else:
    save_output = False

# saves noisy image file if save_output is True
if save_output and 'noisy_image' in locals():
    noisy_image = noisy_image.resize((int(0.25*noisy_image.width), int(0.25*noisy_image.height)), resample=0)
    noisy_image = noisy_image.convert("L")

    directory = input("Enter desired directory: ")

    original_dir = os.getcwd()

    while True:
        try:
            os.chdir(directory)
            break

        except FileNotFoundError:
            print("Invalid directory.")

    output_file = input("Enter name of output file: ")
    noisy_image.save(output_file)

    os.chdir(original_dir)
