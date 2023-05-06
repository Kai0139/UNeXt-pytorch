import os
import shutil

from pathlib import Path

dataset_root_dir =  Path("/home/iadc/medimg/busi/archive/Dataset_BUSI_with_GT").resolve()

dataset_sub_dirs = os.listdir(dataset_root_dir)

def file_index(filename):
    idx_start = fn.find("(")
    idx_end = fn.find(")")
    idx = int(fn[idx_start+1:idx_end])
    return idx

for sub_dir in dataset_sub_dirs:
    img_names = os.listdir(Path.joinpath(dataset_root_dir, sub_dir))
    print("total images: {}".format(len(img_names)))

    img_list = []
    mask_list = []

    for fn in img_names:
        
        idx = file_index(fn)
        if "mask" in fn:
            mask_list.append(fn)


print(dataset_sub_dirs)