# # Part 2

# Functions to calculate the per-pixel error, the rms error, and the fractions of pixels with less than 4, 2, 1, and 0.25 pixels error.
# All of the statistic function use get_dif in their implementation, so you don't need to call it first.


import numpy as np
ERROR_SHAPE_MISMATCH = -1

def get_dif(disp_calc, disp_truth):
    """
    Gets the difference in pixels between the calculated and ground disparity maps
    Assumes the ground is in units of 256*pixels, and the calculated is in pixels
    Returns the difference as a 2d array of same shape is its inputs, as well as an index representing the non-zero values
    """
    # Make sure the images are the same size
    if (disp_calc.shape != disp_truth.shape):
        print("ERROR! The disparity map and the ground truth have differenct sizes")
        return ERROR_SHAPE_MISMATCH, ERROR_SHAPE_MISMATCH
    # Get the indices of the nonzero values
    non_zero   = np.nonzero(disp_truth)
    difference = disp_truth.copy()/256
    # Get the differences
    difference[non_zero] = difference[non_zero] - disp_calc[non_zero]
    difference = np.abs(difference)
    
    return difference, non_zero

def rms(disp_calc, disp_truth):
    """
    Given a calculated and a ground disparity map, computes the rms between them
    """
    difference, non_zero = get_dif(disp_calc, disp_truth)
    error         = np.sqrt(np.mean(difference[non_zero].flatten()**2))
    return error

def fractions(disp_calc, disp_truth):
    """
    Given a calculated and a ground disparity map, computes the 
    fractions of pixels with less than 4, 2, 1, and 0.25 pixels error
    """
    difference, non_zero = get_dif(disp_calc, disp_truth)
    difs      = difference[non_zero].flatten()
    fracs     = [4,2,1,0.5,0.25]
    frac_dict = {}
    # Calculate the fractions
    for frac in fracs:
        frac_dict[frac] = len(difs[difs<frac])/len(difs)
        
    return frac_dict
# Now we wrap all of this up into one function
def get_stats(disp_calc, disp_truth):
    return rms(disp_calc, disp_truth), fractions(disp_calc, disp_truth)
