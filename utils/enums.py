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

class NormalizationEnum(Enum):
    MINMAX = minmax
    KATIELANE = katielane

