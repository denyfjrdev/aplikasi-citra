import cv2
import numpy as np

def terapkan_penajaman(citra):
    """
    Menerapkan penajaman citra menggunakan kernel Laplacian.
    """
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    hasil = cv2.filter2D(citra, -1, kernel)
    return hasil