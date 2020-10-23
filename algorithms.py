# needed to retrieve parameters for specific de-noise processes
import numpy as np
import math
from concurrent import futures
import multiprocessing as mp
from itertools import product
import time


def salt_pepper_denoise(img, settings):
    """Removes salt and pepper noise from images."""

    # for debugging
    print("Salt and Pepper Noise Removal underway...")

    # variables needed for de-noising
    num_rings = int((settings.neighborhood_dim - 1) / 2)
    x_pixels = img.shape[1]
    y_pixels = img.shape[0]

    adjust_threads = list()  # list to store adjustment threads
    thread_dim = 4  # how many processes each column should be split into
    process_threads = [None] * (thread_dim ** 2)  # list to store processing threads
    all_changes = [None] * (thread_dim ** 2)  # stores all adjustments made to image

    # adjusts pixels based on whether they are close to median value of neighborhood
    # parity and sub-parity which help parallelize rows and columns
    def parallel_processing(parity, sub_parity):
        """This function processes the noise for one particular set of rows and columns"""
        """The parity values determine how many threads are run at once"""
        """Threads = number of parity, sub_parity combinations"""

        changes = list()

        for y in range(num_rings + parity, y_pixels - num_rings, thread_dim):

            for x in range(num_rings + sub_parity, x_pixels - num_rings, thread_dim):

                median_of_these = list()  # list to hold all pixel values in neighborhood

                # adds each value in the neighborhood to the list of neighborhood values
                for sub_y in range(settings.neighborhood_dim):
                    for sub_x in range(settings.neighborhood_dim):
                        median_of_these.append(img[(y - num_rings + sub_y), (x - num_rings + sub_x)])

                # gets median pixel value of the neighborhood
                median_val = int(np.median(median_of_these))

                # stores location of the change and the desired pixel value
                if np.absolute(img[y, x] - median_val) > settings.tolerance:
                    changes.append([y, x, median_val])

        return changes

    def parallel_adjustments(adjustments):
        """This function changes the pixel values at the locations specified in the adjustments parameter"""

        for element in adjustments:
            img[element[0], element[1]] = element[2]

    # concurrent futures allows for multi-threading
    with futures.ThreadPoolExecutor(max_workers=thread_dim ** 2) as executor:

        for strand in range(thread_dim ** 2):
            p_1 = math.floor(strand / thread_dim)  # represents parity
            p_2 = strand % thread_dim  # represents sub_parity

            # starts threads to execute each set of calculations
            process_threads[strand] = (executor.submit(parallel_processing, p_1, p_2))
            all_changes[strand] = process_threads[strand].result()

            # for debugging
            print(f"Strand {strand+1}/{thread_dim ** 2} complete!")

    # starts threads to modify pixel values
    with futures.ThreadPoolExecutor(max_workers=thread_dim ** 2) as executor:
        for thread in range(thread_dim ** 2):
            adjust_threads.append(executor.submit(parallel_adjustments, all_changes[thread]))

    # for debugging
    print("De-noising complete!")

    return img


def gaussian_denoise(img, settings):
    """Removes Gaussian noise from images."""

    # for debugging
    print("Gaussian Noise Removal underway...")

    # variables needed for de-noising
