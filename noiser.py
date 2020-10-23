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
        row[tuple(coords)] = 255

        # adding pepper noise
        coords = [np.random.randint(0, column-1, int(num_pepper)) for column in row.shape]
        row[tuple(coords)] = 0

    return copy_data


def add_gaussian(image, st_dev, average):
    """Adds gaussian noise to image"""

    # imports image data into np array and copies it to protect original file
    data = asarray(image)
    copy_data = deepcopy(data)

    # number of pixels in the image
    num_of_pixels = copy_data.size

    # create noise map of gaussian noise
    noise_map = np.random.normal(average, st_dev, num_of_pixels)
    noise_map = [round(element) for element in noise_map]

    # adds noise values to each pixel
    for y in range(copy_data.shape[0]):
        for x in range(copy_data.shape[1]):

            # amount of noise to be added
            noise_value = noise_map.pop()

            noisy_pixel = copy_data[y, x] + noise_value

            # add noise value to the pixel value
            # limits pixel values to 0-255 and prevents "wrapping"
            if 0 <= noisy_pixel <= 255:
                copy_data[y, x] = noisy_pixel
            elif noisy_pixel < 0:
                copy_data[y, x] = 0
            elif noisy_pixel > 255:
                copy_data[y, x] = 255

    copy_data = np.clip(copy_data, 0, 255)

    return copy_data


# ___ Main Code ___
while True:
    path = input("Enter path to image file: ")  # file path to image

    try:
        img = Image.open(path)  # instance of PIL Image object
        img = img.convert("L")
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

    while True:
        try:
            slt_pct = float(input("Enter salt noise percentage: "))
            dns = float(input("Enter noise density: "))

            if 0 <= slt_pct <= 1 and 0 <= dns <= 1:
                break

            else:
                print("Invalid value(s).")

        except ValueError:
            print("Values must be float.")

    # converts numpy array back into PIL image
    noisy_image = Image.fromarray(add_salt_pepper(img, slt_pct, dns))
    save_output = True

elif mode == 1:
    while True:
        try:
            avg = int(input("Enter average noise value: "))
            standard_dev = int(input("Enter standard deviation of noise: "))

            if -64 < avg < 64 and standard_dev >= 0:
                break
            else:
                print("Invalid value(s).")

        except ValueError:
            print("Inputs must be integers")

    # converts numpy array back into PIL image
    noisy_image = Image.fromarray(add_gaussian(img, standard_dev, avg))
    save_output = True

else:
    noisy_image = None
    save_output = False

# saves noisy image file if save_output is True
if save_output and 'noisy_image' in locals():

    print(f"Image resolution: {noisy_image.width}x{noisy_image.height}")  # original resolution of image

    # gives user option to resize an image if it is too large
    while True:
        try:
            resize = float(input("Enter resize factor: "))

            # limit for resize set to 2 to avoid excessive file sizes
            if resize != 1 and 0 < resize < 2:
                noisy_image = noisy_image.resize((int(resize*noisy_image.width),
                                                  int(resize*noisy_image.height)), resample=0)
                break

            # no change needed if resize=1
            elif resize == 1:
                break

            elif resize >= 2:
                print("Resize factor exceeds limit.")

            else:
                print("Resize factor must be positive.")

        except ValueError:
            print("Value is a float.")

    original_dir = os.getcwd()

    # changes directory or gives proper error message
    while True:
        try:
            directory = input("\nEnter desired directory: ")
            os.chdir(directory)
            break

        except FileNotFoundError:
            print("Invalid directory.")

    # avoids errors where file name is missing image file extension (aka .jpg, etc)
    while True:
        try:
            output_file = input("Enter name of output file: ")
            noisy_image.save(output_file)
            break

        except ValueError:
            print("Invalid file name or format")

    os.chdir(original_dir)
