""" 
RandAugment
Paper: https://arxiv.org/abs/1909.13719
Re-implement (changed) using albumentations by seefun
"""

import numpy as np
import albumentations

## TODO update to albumentation 1.0.0

def randAugment(N=2, M=4, p=1.0, mode="all", cut_out = False):
    """
    Examples:
        >>> # M from 0 to 20
        >>> transforms = randAugment(N=3, M=8, p=0.8, mode='all', cut_out=False)
    """
    # Magnitude(M) search space  
    scale = np.linspace(0,0.4,20)
    translate_x = np.linspace(0,0.4,20)
    translate_y = np.linspace(0,0.4,20)
    rot = np.linspace(0,30,20)
    shear_x = np.linspace(0,20,20)
    shear_y = np.linspace(0,20,20)
    sola = np.linspace(0,160,20)
    post = [0,0,1,1,2,2,3,3,4,4,4,4,5,5,6,6,7,7,8,8]
    contrast = np.linspace(0.0,0.4,20)
    bright = np.linspace(0.0,0.4,20)
    shar = np.linspace(0.0,0.9,20)
    blur = np.linspace(0,0.5,20)
    cut = np.linspace(0,0.6,20)
     # Transformation search space
    Aug =[# geometrical
        albumentations.Affine(scale= (1.0-scale[M], 1.0+scale[M]), p=p),
        albumentations.Affine(translate_percent = {'x': (-translate_x[M], translate_x[M])}, p=p),
        albumentations.Affine(translate_percent = {'y': (-translate_y[M], translate_y[M])}, p=p),
        albumentations.Affine(rotate = (-rot[M], rot[M]), p=p),
        albumentations.Affine(shear = {'x': (-shear_x[M], shear_x[M])}, p=p),
        albumentations.Affine(shear = {'y': (-shear_y[M], shear_y[M])}, p=p),
        # Color Based
        albumentations.Solarize(threshold=sola[M], p=p),
        albumentations.Posterize(num_bits=post[M], p=p),
        albumentations.RandomContrast(limit=contrast[M], p=p),
        albumentations.RandomBrightness(limit=bright[M], p=p),
        albumentations.Sharpen(alpha=(0.1, shar[M]), lightness=(0.5, 1.0), p=p),
        albumentations.core.composition.PerChannel(
            albumentations.OneOf([
                albumentations.MotionBlur(p=1),
                albumentations.MedianBlur(blur_limit=3, p=1),
                albumentations.Blur(blur_limit=3, p=1),])
            , p=blur[M]*p),]
    # Sampling from the Transformation search space
    if mode == "geo": 
        transforms = albumentations.SomeOf(Aug[0:6], N)
    elif mode == "color": 
        transforms = albumentations.SomeOf(Aug[6:], N)
    else:
        transforms = albumentations.SomeOf(Aug, N)
  
    if cut_out:
        cut_trans = albumentations.OneOf([
            albumentations.CoarseDropout(max_holes=8, max_height=16, max_width=16, fill_value=0, p=1),
            albumentations.GridDropout(ratio=cut, p=1),
            albumentations.Cutout(num_holes=8, max_h_size=16, max_w_size=16, p=1),
        ], p=1), 
        transforms = albumentations.Compose([transforms, cut_trans])
    return transforms