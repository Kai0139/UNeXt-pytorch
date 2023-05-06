import os
import shutil

from pathlib import Path
import cv2
import numpy as np

class ImageWithMask(object):
    def __init__(self):
        self.global_idx = None
        self.local_idx = None
        self.image = None
        self.masks = []
        

class DataArrange(object):
    def __init__(self, root_dir="/home/iadc/medimg/busi/archive/Dataset_BUSI_with_GT"):
        self.dataset_root_dir =  Path(root_dir).resolve()
        self.dataset_sub_dirs = os.listdir(self.dataset_root_dir)
        print("sub directories: {}".format(self.dataset_sub_dirs))

        self.target_dir = Path.joinpath(Path(__file__).resolve().parent.parent, "busi_dataset")

        self.image_target_dir = Path.joinpath(self.target_dir, "images")
        Path.mkdir(self.image_target_dir, parents=True, exist_ok=True)
        print("target image directory: {}".format(str(self.image_target_dir)))

        self.mask_target_dir = Path.joinpath(self.target_dir, "masks", "0")
        Path.mkdir(self.mask_target_dir, parents=True, exist_ok=True)
        print("target mask directory: {}".format(str(self.mask_target_dir)))

        self.target_image_size = (512, 512)

        self.image_dict = {}

    def file_index(self, fn):
        idx_start = fn.find("(")
        idx_end = fn.find(")")
        idx = int(fn[idx_start+1:idx_end])
        return idx
    
    def arrange_file_dirs(self):
        global_idx = 0
        for sub_dir in self.dataset_sub_dirs:
            img_names = os.listdir(Path.joinpath(self.dataset_root_dir, sub_dir))
            print("total images: {}".format(len(img_names)))

            for fn in img_names:
                idx = self.file_index(fn) + global_idx
                img_dir = str(Path.joinpath(self.dataset_root_dir, sub_dir, fn))

                if idx not in self.image_dict:
                    self.image_dict[idx] = ImageWithMask()
                    self.image_dict[idx].global_idx = global_idx

                if "mask" in fn:
                    self.image_dict[idx].masks.append(img_dir)
                elif self.image_dict[idx].image is None:
                    self.image_dict[idx].image = img_dir
                else:
                    raise ValueError("image dict index {} is {}".format(img_dir, self.image_dict[idx].image))
                
            # update global index to next sub directory
            global_idx = max(self.image_dict)


    def move_files(self):

        for idx in self.image_dict:
            img_dir = Path.joinpath(self.image_target_dir, str(idx)+".png")
            img = cv2.imread(str(img_dir))
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            img = cv2.resize(img, self.target_image_size)
            cv2.imwrite(str(img_dir), img)
            # print(img.shape)
            # shutil.copy(self.image_dict[idx].image, str(img_dir))

            mask_dir = str(Path.joinpath(self.mask_target_dir, str(idx)+".png"))
            mask = self.merge_masks(self.image_dict[idx].masks)
            mask = cv2.resize(mask, self.target_image_size)
            cv2.imwrite(mask_dir, mask)


    def test_merge(self):
        result = self.merge_masks(self.image_dict[173].masks)
        cv2.imwrite("merged_mask_173.png", result)

    def merge_masks(self, masks):
        result = None
        for m in masks:
            img = cv2.imread(m)
            if result is None:
                result = np.zeros(img.shape)
            result += img

        return result
                
if __name__ == "__main__":
    da = DataArrange()
    da.arrange_file_dirs()
    da.move_files()
    # da.test_merge()
    
            

