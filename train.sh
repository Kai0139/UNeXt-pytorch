#!/bin/sh

DATASET_DIR=${PWD}/picai_dataset

echo $DATASET_DIR

python3 train.py --dataset ${DATASET_DIR} \
                 --arch UNext3D \
                 --name picai \
                 --img_ext .mha \
                 --mask_ext .nii.gz \
                 --lr 0.0001 \
                 --epochs 200 \
                 --input_w 256 \
                 --input_h 256 \
                 --b 16