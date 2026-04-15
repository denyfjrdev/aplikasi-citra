import cv2

def terapkan_median_filter(citra, ukuran_kernel=5):
    """
    Menerapkan Median Filter untuk reduksi derau salt-and-pepper.
    """
    if ukuran_kernel % 2 == 0:
        ukuran_kernel += 1
    hasil = cv2.medianBlur(citra, ukuran_kernel)
    return hasil