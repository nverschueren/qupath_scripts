# This is an alternative method to export the position of the cells.
import pandas as pd
import matplotlib.pyplot as plt
#we have a .csv file whose columns include the image name and the positions (in micrometers of the centroid)

df=pd.read_csv('measurements.csv')

# so we make an array of strings with the image names

listimages=df['Image'].unique()
df1=df[df['Image']==listimages[0]]
df2=df[df['Image']==listimages[1]]
cells=df1.iloc[: , -2:]
cells.rename(columns={ cells.columns[0]: "X" }, inplace = True)
cells.rename(columns={ cells.columns[1]: "Y" }, inplace = True)

cells1=df2.iloc[: , -2:]
cells1.rename(columns={ cells1.columns[0]: "X" }, inplace = True)
cells1.rename(columns={ cells1.columns[1]: "Y" }, inplace = True)


plt.scatter(cells['X'],cells['Y']);
plt.ylim(max(cells['Y']), min(cells['Y']))  # decreasing time

plt.show()
