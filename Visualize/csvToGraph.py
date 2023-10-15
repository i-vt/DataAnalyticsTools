import matplotlib.pyplot as plt
import pandas as pd

strSource = "SampleData.csv"
pdData = pd.read_csv(strSource, sep=' ', header=None, names=['x', 'y'])

pltFigure = plt.figure(dpi=600) # create figure & set DPI

plt.plot(pdData['x'], pdData['y'])

plt.xlabel('Test X-axis')
plt.ylabel('Test Y-axis')
plt.title('Title go here :)')

plt.savefig("ImageOutput.jpg", dpi=600)

plt.show()
