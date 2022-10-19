import kmapper as km
import numpy as np

point_cloud = []

with open("game_data_1.txt") as f:
    for line in f:
        x,y,z = line.split(',')
        x = int(x)
        y = int(y)
        z = int(z)
        point_cloud.append([x/5,y/5,z/2])

point_cloud = np.array(point_cloud)
mapper = km.KeplerMapper(verbose = 1)
projected_data = mapper.fit_transform(point_cloud, projection = [2])
cover = km.Cover(n_cubes = 10)
#it gives an error here, but I'm not sure why that is
graph = mapper.map(projected_data, point_cloud, cover = cover)
mapper.visualize(graph, path_html = "did_it_work.html", title = "hi")