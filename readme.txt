

glassesusa_split_alpha_mask.py
    input: internet downloaded images
    output: alpha mask and RGB
    
Celeba_generate_faces_png.py
    input: 30K high resolution celebA-HQ images
    output: resize a subset to 1024x1024

Composition_code_for_glasses.py
    input: face images, glass images, alpha matte
    output (1024x1024): composited face+glass, glass mask (binary), glass removed with Poisson
    
Crop_near_eyes.py
    input: large images (1024x1024)
    output: cropped images around the eye region
    
Resize.py
    output: resize images (320x160)