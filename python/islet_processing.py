import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import glob
import networkx as nx
from scipy.spatial import distance_matrix, ConvexHull
from scipy.spatial.distance import cdist, directed_hausdorff

##---------------------FUNCTIONS --------------------

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
pf=glob.glob(os.path.join('./cells','*.geojson'))
S=[]
for a in pf:
    
    f=open(a)
    datos=json.load(f)
    totcells=len(datos['features'])#total number of cells
    co={'beta_cell':'r','none':'b','alpha_cell':'m','delta':'g','islet':'k'}
    #esto es muy old school
    rows=[]
    for i in range(0,totcells):
        puntos=np.array(datos['features'][i]['geometry']['coordinates'])
        cell_type=datos['features'][i]['properties']['classification']['name']
        x=sum(puntos[0][:,0])/len(puntos[0][:,0])
        y=sum(puntos[0][:,1])/len(puntos[0][:,1])
        rows.append([x,-y,cell_type])
        
    df=pd.DataFrame(rows,columns=["x","y","cell_type"])
    df=df[df['cell_type']!='none'] #get rid of the none nodes
    df['id']=np.arange(len(df))
        
    
    dist_mat=distance_matrix(np.array(df[['x','y']]),np.array(df[['x','y']]),p=2)
    #lets have a look at the typical distances
    #plt.scatter(range(len(dist_mat[0,:])),dist_mat[0,:])
    #plt.show()
    epsi=30 #cut-off for the distances

    dist_mat=np.where(dist_mat>epsi,0,1)
    np.fill_diagonal(dist_mat,0)
#    G=nx.Graph(dist_mat,nodetype=int,)
    G=nx.Graph(dist_mat)
    

    node_attr = df.set_index('id').to_dict('index')
    nx.set_node_attributes(G,node_attr)
    
    S.extend([G.subgraph(c).copy() for c in nx.connected_components(G)])


#postprocessing. end of the for though the cells
del x, y,totcells,rows,puntos,i,f,dist_mat,datos,df,node_attr,pf,G,a,cell_type

S=[g for g in S if len(g.nodes)>20] #keep only the networks with more than 2 cells
# for each network, compute the centroid and
print("done!")


netat(S)
var=input("Create the figures? [y]")
if var=="y":
    print("..Figures in ./figures/")
    for i in range(0,len(S)):
        plotea(S,i)
        
        plt.savefig("./figuras/fig_"+str(i)+".jpg")
        plt.clf()

        
var=input("Create the dataframes [y]")
if var=="y":
    # DATAFRAMES
    # ISLET DATAFRAME
    rows=[]
    for i in range(0,len(S)):
        did=nx.get_node_attributes(S[i],'cell_type')
        rows.append([i,S[i].graph['centroid'][0],S[i].graph['centroid'][1],S[i].graph['hull'].area,S[i].graph['hull'].volume,len(S[i].nodes),len(S[i].edges),sum(1 for v in did.values() if v == 'delta'),sum(1 for v in did.values() if v == 'alpha_cell'),sum(1 for v in did.values() if v == 'beta_cell')])
        
    islets_df=pd.DataFrame(rows,columns=["islet_id","centroid_x","centroid_y","perimeter","area","tot_cells","edges","delta_cells","alpha_cell","beta_cell"])
    rows=[]    
     # CELL DATAFRAME
    for i in range(0,len(S)):
        for j in list(S[i].nodes):
            pos=np.array([[S[i].nodes[j]['x'],S[i].nodes[j]['y']]])
            cpos=np.array([[S[i].graph['centroid'][0],S[i].graph['centroid'][1]]])
            hull=S[i].graph['hull']
            test=np.transpose(np.array([hull.points[hull.vertices,0],hull.points[hull.vertices,1]]))
            rows.append([i,S[i].nodes[j]['x'],S[i].nodes[j]['y'],S[i].nodes[j]['cell_type'],cdist(cpos,pos).item(),cdist(pos,test).min(),directed_hausdorff(pos,test)[0],len(S[i].edges(j))])
                
    cells_df=pd.DataFrame(rows,columns=["islet_id","posx","posy","cell_type","dist2centre","dist2border(cdist)","dist2border(hausdorff)","edges"])
                
    print(" dataframes created!")
                
                
                





