import kmapper as km
import numpy as np
from mogutda import SimplicialComplex


point_cloud = []

with open("white_noise.txt") as f:
    for line in f:
        x,y,z = line.split(',')
        x = int(x)
        y = int(y)
        z = int(z)
        point_cloud.append([x/4.5,y/4.5,z/4])

point_cloud = np.array(point_cloud)  #mapper needs the data to be in this format

mapper = km.KeplerMapper(verbose = 1) #this creates an instance of the KeplerMapper class, where verbose specifies 
# how much debugging info we want 

projected_data = mapper.fit_transform(point_cloud, projection = [2]) 

#KeplerMapper.fit_transform is a function which takes a dataset as a numpy array,
# and a method of projecting. In this case, we have projected the data based upon the third commonent
#of the point cloud data, which corresponds to generation. There are a number of other ways to project

#In the mapper algorithm, we have a dataset X, and a function f: X \to \R. projection is our way of defining f. 
#this class can be viewed as the function f, where point_cloud (or whatever the dataset might be) is X

cover = km.Cover(n_cubes = 15)
# Actually, the mapper algorithm can be made more abstract by projecting into any number of dimensions.
# While mapping into R, we cover it using open intervals, we would use open squares to cover R^2
# 

graph = mapper.map(projected_data, point_cloud, cover = cover)

def convert_to_simplicial(graph):
    """Unfortunately, I can't seem to figure out how to directly calculate the betti numbers. 
    Simplicial has this tool, but we first need to convert our simplicial complex to their special
    SimplicialComplex class"""
    # names_to_numbers = {}
    # index = 1
    graph_sc = []
    # for s in graph['simplices']:
    #     if len(s) == 1:
    #         names_to_numbers[s[0]] = index
    #         index += 1
    # for s in graph['simplices']:
    #     face = []
    #     for p in s:
    #         face.

    for s in graph['simplices']:
        graph_sc.append(tuple(s))
    return SimplicialComplex(simplices = graph_sc)




# def calculate_cycles(graph):
#     c = convert_to_simplicial(graph)
#     print(c)
#     return print(c.bettiNumbers())

c = convert_to_simplicial(graph)
print(c.betti_number(0),c.betti_number(1))


# print(c.numberOfSimplicesOfOrder())
# print(c.bettiNumbers(ks = [1]))
mapper.visualize(graph)