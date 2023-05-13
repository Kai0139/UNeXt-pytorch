from dataset import Dataset
from pathlib import Path
import cv2

from matplotlib import pyplot as plt

def apply_filter(img):
    img_filtered = cv2.medianBlur(img, 9)
    # img_filtered = cv2.bilateralFilter(img, 9, 75, 75)
    return img_filtered

file_name = "ISIC_0000306_original.png"
file_dir = Path.joinpath(Path(__file__).resolve().parent, "isic_dataset", "samples", file_name)
print(str(file_dir))

img = cv2.imread(str(file_dir))

img_filtered = apply_filter(img)

cv2.imwrite("img_filtered.png" ,img_filtered)
