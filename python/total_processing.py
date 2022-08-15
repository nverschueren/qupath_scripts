import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from scipy.spatial import distance_matrix, ConvexHull
from scipy.spatial.distance import cdist, directed_hausdorff
import numpy as np

##---------------------FUNCTIONS --------------------
co={'beta_cell':'r','none':'b','alpha_cell':'m','delta':'g','islet':'k'}
def plotea(S,i): #plotting the i-th network in the set S
    
    nx.draw(S[i],{j:(S[i].nodes[j]['x'],S[i].nodes[j]['y']) for j in list(S[i].nodes)},node_size=60,node_color=[co[S[i].nodes[k]['cell_type']] for k in S[i].nodes])
    print(len(S[i]))
    if len(S[i].graph)>0:
        
        x=S[i].graph['hull'].points[S[i].graph['hull'].vertices,0]
        y=S[i].graph['hull'].points[S[i].graph['hull'].vertices,1]
        
        plt.plot(x,y,color='c')
        plt.plot([x[-1],x[0]],[y[-1],y[0]],color='c')

        

        plt.axis('scaled')
       
        plt.scatter(S[i].graph['centroid'][0],S[i].graph['centroid'][1],c='c',marker='x',s=50)



def netat(S): #compute the centroid and  boundary of the network
    for i in range(0,len(S)):
        puntos=np.array([[S[i].nodes[k]['x'],S[i].nodes[k]['y']] for k in S[i].nodes])
        S[i].graph['centroid']=np.array([sum(puntos[:,0])/len(puntos[:,0]),sum(puntos[:,1])/len(puntos[:,1])])
        S[i].graph['hull']=ConvexHull(puntos)
##---------------------END OF FUNCTIONS --------------------


# for a given series of images, I assume I have 2 csv files, one with the cells(cells.csv) and one with the annotations (detections.csv).
S=[]
cells=pd.read_csv('cells.csv')
annotations=pd.read_csv('detections.csv')
# I am assuming I have the same imagelist for cells and annotations
cellsimages=cells['Image'].unique()
annoimages=annotations['Image'].unique()
i=0 #considering the first image (then loop)
cells.rename(columns={cells.columns[-2]:"X"},inplace=True)
cells.rename(columns={cells.columns[-1]:"Y"},inplace=True)

i=0 #considering the first image (then loop)
df=cells[cells['Image']==cellsimages[i]]
df=df[['X','Y','Name']]
df.rename(columns = {'X':'x','Y':'y','Name':'cell_type'}, inplace = True)#back compatibility
#verbatim  from islet_processing

df=df[df['cell_type']!='none'] #get rid of the none nodes
df['id']=np.arange(len(df))
        
    
dist_mat=distance_matrix(np.array(df[['x','y']]),np.array(df[['x','y']]),p=2)
#lets have a look at the typical distances
#plt.scatter(range(len(dist_mat[0,:])),dist_mat[0,:])
#plt.show()
epsi=15 #cut-off for the distances

dist_mat=np.where(dist_mat>epsi,0,1)
np.fill_diagonal(dist_mat,0)
G=nx.Graph(dist_mat,nodetype=int,)
G=nx.Graph(dist_mat)
    

node_attr = df.set_index('id').to_dict('index')
nx.set_node_attributes(G,node_attr)
   
S.extend([G.subgraph(c).copy() for c in nx.connected_components(G)])
