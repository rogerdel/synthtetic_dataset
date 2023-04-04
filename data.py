# path where the object images are
images_dir         = 'images/plastics'

# path where the background images are
background_dir        = 'images/background'

# path where new images will be generated
save_dir        = 'dataset'

# Probability of having more than one object per background image
# if the value is 0 then there will just one object per background image
# if the values is 1 then there will more than one obejct per background image/

prob_many_objs   = 0.4

# When one more than object will be added per background image 
# this value is the probabily of adding a type or class of an object
# e.g there are three classes of objects A,B,C and the values is 0.5
# there is a 50% of adding an object A, 50% of adding an object of B
# and 50% of adding an object of C

prob_add_obj     = 0.5

# probability of resizing genreated image
resize_prob     = 0.96

# lenght of the names of the files to be generated
filename_size   = 10

# How manny images will be genereated per class 
# e.g there are three classes of objects A,B,C if the value is 10
# there will be at least 10 images with A object , 10 images with B objects 
# and 10 images with C object. In total 30 images will be generated

imagesperClass = 10