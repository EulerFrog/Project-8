from enum import Enum
import numpy as np

def minmax(data: list[float]):
    '''
    Bounds: [0,1]
    '''
    data_np = np.array(data)
    norm_np = (data_np - np.min(data_np)) / (np.max(data_np)-np.min(data_np))
    return norm_np.tolist()

def katielane(data: list[float]):
    '''
    Bounds: [1,2] (theoretically)
    '''
    data_np = np.array(data)
    min_norm_avgs = data_np / np.mean(data_np[-5:])
    full_norm_avgs = ((min_norm_avgs - 1) / ((np.mean(min_norm_avgs[:5])) - 1)) + 1
    return full_norm_avgs.tolist()

def two_one(data: list[float]):
    '''
    Bounds: [1,2]
    '''
    data = minmax(data)
    data_np = np.array(data)
    min_norm_avgs = data_np / np.mean(data_np[-5:]) # Normalize the end 5 to be at value 1
    full_norm_avgs = ((min_norm_avgs - 1) / (np.max(min_norm_avgs) - np.min(min_norm_avgs))) + 1  # Normalize maximum to be at 2
    return full_norm_avgs

class NormalizationEnum(Enum):
    MINMAX = minmax
    KATIELANE = katielane
    TWO_ONE = two_one

