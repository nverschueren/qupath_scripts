import pandas as pd
import matplotlib.pyplot as plt
import json
import numpy as np
from scipy.spatial import distance_matrix# I ditched th ConvexHull for now
import networkx as nx
##---------------------FUNCTIONS --------------------
def plotea(S,i): #plotting the i-th network in the set S
    nx.draw(S[i],{j:(S[i].nodes[j]['X'],S[i].nodes[j]['Y']) for j in list(S[i].nodes)},node_size=60,node_color=[co[S[i].nodes[k]['cell_type']] for k in S[i].nodes])
    print(len(S[i]))
    plt.scatter(S[i].graph['stain_border'][:,0],S[i].graph['stain_border'][:,1],color='gray',marker='.')
    ax = plt.gca()
    ax.set_aspect('equal')
    ax.invert_yaxis()
    plt.scatter(S[i].graph['centroid'][0],S[i].graph['centroid'][1],c='c',marker='x',s=50)

##---------------------END OF FUNCTIONS --------------------

##==================CREATING THE NETWORKS=======================

#The input is one file with the measurements per cell
df=pd.read_csv('../measurements_cells.csv')
list_islets=df[['Image','Parent']].drop_duplicates()
S=[]
bf='../islets/'
atr='_islets.geojson'
dp=0.4963271788763152 #this is the width=height of the pixels (obtained from QuPath and it does depend on the imageset)
co={'beta_cell':'r','none':'b','alpha_cell':'m','delta_cell':'g'}#dict colours per cell type
epsi=14 #cut-off for the distances (in Cabrera et al, the contact between cells occurs whenever epsilon=3 micro meters between the edges (not centroid!)

for j in range(0,len(list_islets)):
    imname=list_islets.iloc[j]['Image']
    ide=list_islets.iloc[j]['Parent']
    islets=json.load(open(bf+imname+atr))['features']
    #The ide of the islet should coincide with the index of the islet i.e.
    # if islets[ide]['properties']['names']==ide?
    boundaries=dp*np.array([ xx for l in islets[ide]['geometry']['coordinates'] for xx in l])#here, I am ignoring the subcurves
    cells=df[(df['Image']==imname) & (df['Parent']==ide)][['Name','Centroid X µm','Centroid Y µm','Nucleus: Area','Nucleus: Perimeter','Nucleus: Circularity', 'Nucleus/Cell area ratio']]
    # Name and Class have the same information
    cells.rename(columns={cells.columns[0]:'cell_type',cells.columns[1]:"X",cells.columns[2]:"Y"},inplace=True)
    cells=cells[cells['cell_type']!='none'] #get rid of the nones
    dist_mat=distance_matrix(np.array(cells[['X','Y']]),np.array(cells[['X','Y']]),p=2)

    dist_mat=np.where(dist_mat>epsi,0,1)
    np.fill_diagonal(dist_mat,0)
    G=nx.Graph(dist_mat)
    #cells attributes
    cells['id']=np.arange(len(cells))
    node_attr=cells.set_index('id').to_dict('index')
    nx.set_node_attributes(G,node_attr)
    #network attributes
    G.graph['centroid']=np.array([sum(cells['X'])/len(cells['X']),sum(cells['Y'])/len(cells['Y'])])
    G.graph['stain_border']=boundaries;S.append(G)
    print(j,ide)

print('done! Networks created!')
# FROM here we can create the figurs, dataframes at islet and cellular level (of the whole imageset). Before proceeding any further, I will make sure that I can apply this to additional imagesets.

