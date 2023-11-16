import numpy as np
import matplotlib.pyplot as plt

# Parameters for the normal distribution
mean = 0  # Mean of the distribution
std_dev = 1  # Standard deviation of the distribution
num_samples = 1000  # Number of samples

# Generate normal distribution data
data = np.random.normal(mean, std_dev, num_samples)

# Plotting the data to visualize the bell curve
plt.hist(data, bins=30, density=True)
plt.title('Normal Distribution (Bell Curve)')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.show()
