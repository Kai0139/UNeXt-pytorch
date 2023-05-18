#!/bin/sh

DATASET_DIR=${PWD}/isic_dataset

echo $DATASET_DIR

python3 train.py --dataset ${DATASET_DIR} \
                 --arch UNext_S \
                 --name isic_unextS_kernel5 \
                 --img_ext .jpg \
                 --mask_ext .png \
                 --num_classes 1 \
                 --lr 0.0001 \
                 --epochs 100 \
                 --input_w 512 \
                 --input_h 512 \
                 --b 8