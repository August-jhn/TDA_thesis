#this file is meant to be independent of pygame and ripser. It's only dependency is numpy.
#the intention here is to give us more freedom in how exactly we want to use the game of life functions
#I'll also try and create a higher dimensional version of the game of life.


class point_cloud_GoL:

    #initial points is just a 2d array, [[x_1,y_1], ... , [x_n,y_n]] of live cells
    def __init__(self, initial_points = "empty", verbose = False):
        if initial_points == 0:
            self.initial_points = []
        else:
            self.initial_points = initial_points
        self.verbose = verbose
        

    def update(self, verbose = self.verbose):
        potential_lazaruses = {} # a dictionary
        #the key values are points, the values are sets of nieghbors
        new_points = self.points[:]

        cells_killed = 0
        cells_born = 0

        for point in self.points:
            total_neighbors = 0
            for i in [-1,0,1]:
                for j in [-1,0,1]:
                    if i != 0 or j != 0 and [point[0] + i, point[1]+j] in self.points:
                        total_neighbors += 1
                    
                    if [point[0] + i, point[1] + j] not in potential_lazaruses:
                        potential_lazaruses[[point[0] + i, point[1] + j]] = {[point[0] + i, point[1] + j]}
                    else:
                        potential_lazaruses[[point[0] + i, point[1] + j]].add([point[0] + i, point[1] + j])
            if total_neighbors == 2 or total_neighbors == 3:
                new_points.append(point)
            else:
                cells_killed += 1
        for point in potential_lazaruses:
            if len(potential_lazaruses[point]) >= 3 and point not in self.points:
                new_points.append(point)
                cells_born += 1

        self.points = new_points

        if verbose:
            print("Total of {killed} cells died".format(killed = cells_killed))
            print("Total of {}  cells born".format(born = cells_born))
        