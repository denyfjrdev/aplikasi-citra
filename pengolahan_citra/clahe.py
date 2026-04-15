import cv2

def terapkan_clahe(citra, batas_klip=2.0, ukuran_tile=8):
    """
    Menerapkan CLAHE (Contrast Limited Adaptive Histogram Equalization)
    pada kanal Luminance (LAB color space).
    """
    lab = cv2.cvtColor(citra, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=batas_klip, tileGridSize=(ukuran_tile, ukuran_tile))
    l_clahe = clahe.apply(l)
    lab_clahe = cv2.merge([l_clahe, a, b])
    hasil = cv2.cvtColor(lab_clahe, cv2.COLOR_LAB2BGR)
    return hasil