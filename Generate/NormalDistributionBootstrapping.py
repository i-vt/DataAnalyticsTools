#Generate data with similar distribution as existing dataset

import numpy as np

sample_data = [29, 21, 35, 15, 23, 6, 46, 
28, 13, 8, 40, 46, 2, 34, 29, 5, 24, 42, 
16, 33, 5, 3, 13, 46, 4, 36, 18, 23, 32, 47, 0, 29, 9, 
34, 1, 11, 43, 25, 46, 17, 9, 32, 7, 21, 47, 42, 
45, 17, 16, 29, 47, 43, 47, 10, 49, 28, 33, 44, 
39, 0, 41, 14, 33, 41, 18, 32, 29, 39, 47, 35, 40, 36, 
28, 23, 32, 27, 25, 47, 15, 5, 49, 6, 43, 40, 13, 30, 22, 
13, 22, 8, 6, 23, 22, 17, 6, 19, 26, 3, 46, 0]

original_data = np.array(sample_data)  

# Number of samples you want to generate
num_samples = 1000  # Adjust this as needed

# Generate new samples using bootstrapping
bootstrapped_data = np.random.choice(original_data, size=num_samples, replace=True)
