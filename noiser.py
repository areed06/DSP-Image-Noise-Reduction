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
path = input("Enter path to image file: ")

img = Image.open(path)

print("Mode Description:\n"
      "(0) --> Salt and Pepper\n"
      "(1) --> Gaussian Noise\n"
      "(2) --> Poisson Noise\n"
      "(3) --> Speckle Noise\n")

while True:
    try:
        mode = int(input("Enter desired mode: "))
        break
    except ValueError:
        print("Mode is integer")

if mode == 0:
    slt_pct = float(input("Enter salt noise percentage: "))
    dns = float(input("Enter noise density: "))

    noisy_image = Image.fromarray(add_salt_pepper(img, slt_pct, dns))
    save_output = True
else:
    save_output = False

if save_output:
    noisy_image.save('output.jpg')
