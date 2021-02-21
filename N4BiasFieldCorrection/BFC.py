from __future__ import print_function
#from tensorflow.python.client import device_lib
#device_lib.list_local_devices()

import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt
#matplotlib notebook
#matplotlib inline

print("N4 bias correction runs.")
inputImage = sitk.ReadImage("patient01/patient01_T2W.nii.gz")
# maskImage = sitk.ReadImage("06-t1c_mask.nii.gz")
maskImage = sitk.OtsuThreshold(inputImage,0,1,200) #choose suitable threshold
sitk.WriteImage(maskImage, "patient01/patient01_T2W1.nii.gz" )

inputImage = sitk.Cast(inputImage,sitk.sitkFloat32)

corrector = sitk.N4BiasFieldCorrectionImageFilter();

output = corrector.Execute(inputImage,maskImage)
sitk.WriteImage(output, "patient01/patient01_T2W3.nii.gz")
print("Finished N4 Bias Field Correction.....")
