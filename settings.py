build_num = "1.0.0"  # current build version

mode_activations = {"Salt & Pepper": 1, "Gaussian": 0, "Poisson": 0, "Adam's Custom Algorithm": 0}
available_modes = ("Salt & Pepper", "Gaussian", "Poisson", "Adam's Custom Algorithm")

min_window_width = 800
min_window_height = 500

def_font = 'Segoe UI'
button_font_size = 10
combobox_font_size = 10

supported_files = [('JPEG Files', '*.jpg*'), ('NEF Raw Files', '*.NEF*'), ('TIF Files', '*.tif*')]
default_save_directory = 'C:\\'

# ___ Salt & Pepper Parameters ___
neighborhood_dim = 3  # side length of neighborhood (in pixels)
tolerance = 1  # threshold for inserting median value for noisy pixel
