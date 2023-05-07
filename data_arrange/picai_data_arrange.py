import os
import shutil

import numpy as np
from pathlib import Path
import itk
import nibabel
import cv2

class PicaiDataArrange(object):
    def __init__(self, root_dir="/home/iadc/medimg/picai/dataset"):
        self.dataset_root_dir =  Path(root_dir).resolve()
        self.dataset_sub_dirs = list(self.dataset_root_dir.iterdir())

        self.target_dir = Path.joinpath(Path(__file__).resolve().parent.parent, "picai_dataset")

        self.image_target_dir = Path.joinpath(self.target_dir, "images")
        Path.mkdir(self.image_target_dir, parents=True, exist_ok=True)
        print("target image directory: {}".format(str(self.image_target_dir)))

        self.mask_target_dir = []
        for i in range(4):
            mask_dir_i = Path.joinpath(self.target_dir, "masks", str(i))
            Path.mkdir(mask_dir_i, parents=True, exist_ok=True)
            self.mask_target_dir.append(mask_dir_i)
            print("target mask {} directory: {}".format(i, str(mask_dir_i)))

        self.label_dir = Path("/home/iadc/medimg/picai/picai_labels/csPCa_lesion_delineations/human_expert/resampled").resolve()
        self.label_names = list(self.label_dir.iterdir())
        # print(self.label_names)


    def arrange_file_dirs(self):
        idx_list = []
        # Read mha data
        for folder in self.dataset_sub_dirs:
            if not folder.is_dir():
                continue
            # Find all folder names for all samples
            mha_list = list(folder.iterdir())
            for mha in mha_list:
                idx = int(str(mha.name))
                # Find all sequences for the sample
                seqs = list(mha.iterdir())
                # Find the t2w sequence
                for seq in seqs:
                    if "t2w" in str(seq):
                        shutil.copy(str(seq), self.image_target_dir.joinpath(str(idx)+".mha"))
                        idx_list.append(idx)
                        break

        # Read labels
        for idx in idx_list:
            for lb in self.label_names:
                if (str(idx)+"_") in str(lb.name):
                    # print(f"save {idx}")
                    image_array = np.array(nibabel.load(str(lb)).get_fdata(), dtype=np.uint8)
                    # image_array = nibabel.load(str(lb)).get_fdata()
                    m0, m1, m2, m3 = self.generate_bit_masks(image_array.shape)
                    mask0 = nibabel.nifti1.Nifti1Image((np.bitwise_and(image_array, m0) / 2).astype(np.uint8), np.eye(4))
                    mask1 = nibabel.nifti1.Nifti1Image((np.bitwise_and(image_array, m1) / 3).astype(np.uint8), np.eye(4))
                    mask2 = nibabel.nifti1.Nifti1Image((np.bitwise_and(image_array, m2) / 4).astype(np.uint8), np.eye(4))
                    mask3 = nibabel.nifti1.Nifti1Image((np.bitwise_and(image_array, m3) / 5).astype(np.uint8), np.eye(4))

                    nibabel.save(mask0, Path.joinpath(self.mask_target_dir[0], str(idx)+".nii.gz"))
                    nibabel.save(mask1, Path.joinpath(self.mask_target_dir[1], str(idx)+".nii.gz"))
                    nibabel.save(mask2, Path.joinpath(self.mask_target_dir[2], str(idx)+".nii.gz"))
                    nibabel.save(mask3, Path.joinpath(self.mask_target_dir[3], str(idx)+".nii.gz"))
                    break
            pass

    def generate_bit_masks(self, shape):
        m = np.ones(shape, dtype=np.uint8)
        mask0 = 2 * m
        mask1 = 3 * m
        mask2 = 4 * m
        mask3 = 5 * m
        return mask0, mask1, mask2, mask3


if __name__ == "__main__":
    pda = PicaiDataArrange()
    pda.arrange_file_dirs()