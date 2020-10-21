class Settings:
    def __init__(self):
        self.build_num = "1.0.0"  # current build version

        self.mode_activations = {"Salt & Pepper": 1, "Gaussian": 0, "Poisson": 0,
                                 "Adam's Custom Algorithm": 0}
        self.available_modes = ("Salt & Pepper", "Gaussian", "Poisson", "Adam's Custom Algorithm")

        self.min_window_width = 800
        self.min_window_height = 500

        self.def_font = 'Segoe UI'
        self.button_font_size = 10
        self.combobox_font_size = 10

        self.supported_files = [('JPEG Files', '*.jpg*'), ('NEF Raw Files', '*.NEF*'),
                                ('TIF Files', '*.tif*')]
        self.default_save_directory = 'C:\\'

        # ___ Salt & Pepper Parameters ___
        self.neighborhood_dim = 3  # side length of neighborhood (in pixels)
        self.tolerance = 1  # threshold for inserting median value for noisy pixel

        self.test_variable = 100
