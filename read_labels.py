#!/usr/bin/env python
#########################################
#       nii2png for Python 3.7          #
#         NIfTI Image Converter         #
#                v0.2.9                 #
#                                       #
#     Written by Alexander Laurence     #
# http://Celestial.Tokyo/~AlexLaurence/ #
#    alexander.adamlaurence@gmail.com   #
#              09 May 2019              #
#              MIT License              #
#########################################

import numpy as np
import scipy, shutil, os, nibabel
import sys, getopt

import cv2

import imageio


def main(inputdir, filename, outputfile):

    inputfile = inputdir + filename
    # print('Input file is ', inputfile)
    # print('Output folder is ', outputfile)

    # set fn as your 4d nifti file
    image_array = nibabel.load(inputfile).get_fdata()
    # image_array = numpy.asanyarray(nibabel.load(inputfile))
    print(image_array.shape)

    # else if 3D image inputted
    if len(image_array.shape) == 3:
        # set 4d array dimension values
        nx, ny, nz = image_array.shape

        # set destination folder
        if not os.path.exists(outputfile):
            os.makedirs(outputfile)
            print("Created ouput directory: " + outputfile)

        # print('Reading NIfTI file...')

        total_slices = image_array.shape[2]

        slice_counter = 0
        # iterate through slices
        n2 = 0
        n3 = 0
        n4 = 0
        n5 = 0

        should_analyze = np.any(image_array)
        for current_slice in range(0, total_slices):
            # alternate slices
            if (slice_counter % 1) == 0:
                data = np.array(image_array[:, :, current_slice], dtype=np.uint8)

                # print("with non zeros: {}".format(np.any(data)))
                with_non_zeros = np.any(data)
                if(with_non_zeros):
                    for r in range(data.shape[0]):
                        for c in range(data.shape[1]):
                            pix = data[r, c]
                            if pix != 0:
                                if pix == 2:
                                    n2 += 1
                                elif pix == 3:
                                    n3 += 1
                                elif pix == 4:
                                    n4 += 1
                                elif pix == 5:
                                    n5 += 1

                #alternate slices and save as png
                if (slice_counter % 1) == 0:
                    # print('Saving image...')
                    image_name = filename[:-7] + "_z" + "{:0>3}".format(str(current_slice+1))+ ".png"
                    # imageio.imwrite(image_name, data)
                    cv2.imwrite(outputfile+image_name, data)
                    # print('Saved.')

                    #move images to folder
                    # print('Moving image...')
                    src = image_name
                    # shutil.move(src, outputfile)
                    slice_counter += 1
                    # print('Moved.')
        if should_analyze:
            print("n1: {}, n2: {}, n3: {}, n4: {}, n5: {}".format(n1, n2, n3, n4, n5))

        # print('Finished converting images')
    else:
        pass
        # print('Not a 3D or 4D Image. Please try again.')

# call the function to start the program
if __name__ == "__main__":
    label_path = "/home/iadc/medimg/picai/picai_labels/csPCa_lesion_delineations/human_expert"
    label_folder = "/resampled/"
    label_dir = label_path + label_folder

    target_folder = "/png/"
    filenames = os.listdir(label_path + label_folder)

    outputdir = label_path + target_folder

    # for fn in filenames:
    #     main(label_dir, fn, outputdir)

    fn = "10000_1000000.nii.gz"
    main(label_dir, fn, outputdir)
    
