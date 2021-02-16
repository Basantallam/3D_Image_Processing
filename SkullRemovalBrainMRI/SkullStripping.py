import numpy as np
import nibabel as nib                                                    
from ipywidgets import interact, interactive, IntSlider, ToggleButtons
from medpy.io import load, save
import matplotlib.pyplot as plt

import seaborn as sns
sns.set_style('darkgrid')

for pa in range (1,31):
  p=str(pa)
  mask_path = "patient"+p+"\patient"+p+"_brainmask.nii.gz"

  for f in range(1):
    files = ["patient"+p+"_FLAIR","patient"+p+"_T1W", "patient"+p+"_T1WKS","patient"+p+"_T2W"]

    image_path = "patient"+p+"\\"+ files[f]+".nii.gz"
    image_obj = nib.load(image_path)
    mask_obj = nib.load(mask_path)
    xx, image_header = load(image_path)
    print(image_header)
    image = image_obj.get_fdata()
    mask = mask_obj.get_fdata()

    result = np.multiply(image, mask)

    save(result, 'SS'+files[f]+'.nii.gz', image_header)
