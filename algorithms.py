import settings  # needed to retrieve parameters for specific de-noise processes
import numpy as np


def salt_pepper_denoise(img):
    """Removes salt and pepper noise from images."""

    # for debugging
    print("Salt and Pepper Noise Removal underway...")

    # variables needed for de-noising
    num_rings = int((settings.neighborhood_dim - 1) / 2)
    x_pixels = img.shape[1]
    y_pixels = img.shape[0]

    # adjusts pixels based on whether they are close to median value of neighborhood
    for y in range(num_rings, y_pixels - num_rings):
        for x in range(num_rings, x_pixels - num_rings):

            median_of_these = list()  # list to hold all pixel values in neighborhood

            # adds each value in the neighborhood to the list of neighborhood values
            for sub_y in range(settings.neighborhood_dim):
                for sub_x in range(settings.neighborhood_dim):
                    median_of_these.append(img[(y - num_rings + sub_y), (x - num_rings + sub_x)])

            # gets median pixel value of the neighborhood
            median_val = int(np.median(median_of_these))

            # changes central pixel value if it differs too greatly from the median
            if np.absolute(img[y, x]) > settings.tolerance:
                img[y, x] = median_val

    # for debugging
    print("De-noising complete!")

    return img
