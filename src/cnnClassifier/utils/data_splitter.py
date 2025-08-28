import os
import random
import shutil
from pathlib import Path
from cnnClassifier import logger

def split_data(source_dir, dest_dir, split_ratio=(0.7, 0.15, 0.15), seed=42):
    """
    Splits data from a source directory into train, validation, and test sets.

    The source directory should have subdirectories for each class.
    The destination directory will be created with train, valid, and test subdirectories,
    each containing the class subdirectories.
    """
    random.seed(seed)
    
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        logger.info(f"Created destination directory: {dest_dir}")

    train_dir = os.path.join(dest_dir, 'train')
    valid_dir = os.path.join(dest_dir, 'valid')
    test_dir = os.path.join(dest_dir, 'test')

    if not os.path.exists(train_dir):
        os.makedirs(train_dir)
    if not os.path.exists(valid_dir):
        os.makedirs(valid_dir)
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    classes = [d for d in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, d))]
    logger.info(f"Found classes: {classes}")

    for cls in classes:
        # Create class subdirectories in train, valid, and test
        os.makedirs(os.path.join(train_dir, cls), exist_ok=True)
        os.makedirs(os.path.join(valid_dir, cls), exist_ok=True)
        os.makedirs(os.path.join(test_dir, cls), exist_ok=True)

        # Get all file paths for the current class
        src_cls_dir = os.path.join(source_dir, cls)
        all_files = [os.path.join(src_cls_dir, f) for f in os.listdir(src_cls_dir) if os.path.isfile(os.path.join(src_cls_dir, f))]
        random.shuffle(all_files)

        # Calculate split indices
        train_split_idx = int(len(all_files) * split_ratio[0])
        valid_split_idx = int(len(all_files) * (split_ratio[0] + split_ratio[1]))

        # Get file lists for each set
        train_files = all_files[:train_split_idx]
        valid_files = all_files[train_split_idx:valid_split_idx]
        test_files = all_files[valid_split_idx:]

        # Copy files to destination
        for f in train_files:
            shutil.copy(f, os.path.join(train_dir, cls))
        for f in valid_files:
            shutil.copy(f, os.path.join(valid_dir, cls))
        for f in test_files:
            shutil.copy(f, os.path.join(test_dir, cls))
            
        logger.info(f"Class '{cls}': {len(train_files)} train, {len(valid_files)} valid, {len(test_files)} test images.")
