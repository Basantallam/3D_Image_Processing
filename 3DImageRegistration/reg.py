import SimpleITK as sitk
from downloaddata import fetch_data as fdata
#%matplotlib notebook
import gui
import registration_gui as rgui

import numpy as np
import os

for pp in range(1,31):
  p = str(pp)
  for ff in range (0,4):
  
    files = ["SSpatient"+p+"_FLAIR.nii.gz","SSpatient"+p+"_T1W.nii.gz", "SSpatient"+p+"_T1WKS.nii.gz","SSpatient"+p+"_T2W.nii.gz"]

    filesPP = ["PPpatient"+p+"_FLAIR.nii","PPpatient"+p+"_T1W.nii", "PPpatient"+p+"_T1WKS.nii","PPpatient"+p+"_T2W.nii"]
    fixed_image =  sitk.ReadImage("Datasets\\originals\\14 training and test\\training\\training03\\preprocessed\\training03_05_flair_pp.nii", sitk.sitkFloat32)

    moving_image = sitk.ReadImage( "Datasets\\patients3Ddataset-Copy\\SS\\"+files[ff] , sitk.sitkFloat32)
  
    initial_transform = sitk.CenteredTransformInitializer(fixed_image, 
                                                      moving_image, 
                                                      sitk.Euler3DTransform(), 
                                                      sitk.CenteredTransformInitializerFilter.GEOMETRY)

  
    registration_method = sitk.ImageRegistrationMethod()
    
# Similarity metric settings.
    registration_method.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)
    registration_method.SetMetricSamplingStrategy(registration_method.RANDOM)
    registration_method.SetMetricSamplingPercentage(0.1)
    registration_method.SetInterpolator(sitk.sitkLinear)
 
# Optimizer settings.
    registration_method.SetOptimizerAsGradientDescent(learningRate=1.0, numberOfIterations=1000, convergenceMinimumValue=1e-6, convergenceWindowSize=10)
    registration_method.SetOptimizerScalesFromPhysicalShift()
   
# Setup for the multi-resolution framework.            
    registration_method.SetShrinkFactorsPerLevel(shrinkFactors = [4,2,1])
    registration_method.SetSmoothingSigmasPerLevel(smoothingSigmas=[2,1,0])
    registration_method.SmoothingSigmasAreSpecifiedInPhysicalUnitsOn()

# Don't optimize in-place, we would possibly like to run this cell multiple times.
    registration_method.SetInitialTransform(initial_transform, inPlace=False)

    
# Connect all of the observers so that we can perform plotting during registration.
    registration_method.AddCommand(sitk.sitkStartEvent, rgui.start_plot)
    registration_method.AddCommand(sitk.sitkEndEvent, rgui.end_plot)
    registration_method.AddCommand(sitk.sitkMultiResolutionIterationEvent, rgui.update_multires_iterations) 
    registration_method.AddCommand(sitk.sitkIterationEvent, lambda: rgui.plot_values(registration_method))
 
    final_transform = registration_method.Execute(fixed_image, moving_image)
   
    moving_resampled = sitk.Resample(moving_image,fixed_image, final_transform, sitk.sitkLinear, 0.0, moving_image.GetPixelID())
    moving_resampled1 = sitk.Resample(moving_image, final_transform, sitk.sitkLinear, 0.0, moving_image.GetPixelID())


    sitk.WriteImage(moving_resampled, os.path.join("Datasets\\patients3Ddataset-Copy\\Reg", filesPP[ff]))

    label=sitk.ReadImage("Datasets\\originals\\patients 3D dataset\\patient"+p+"\\patient"+p+"_consensus_gt.nii.gz", sitk.sitkFloat32)
    
    resampled_label = sitk.Resample(label, fixed_image, final_transform, sitk.sitkLinear, 0.0, label.GetPixelID())
    sitk.WriteImage(resampled_label, os.path.join("Datasets\\patients3Ddataset-Copy\\Reg", "PP"+"patient"+p+"_consensus_gt.nii"))
    
