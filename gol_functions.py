import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from ripser import ripser
from persim import plot_diagrams
import pygame as pg
import time
from mpl_toolkits import mplot3d

BLACK = (0,0,0)
WHITE = (255, 255, 255)
TILE_SIZE = 50
DIM = 800
random_death = 0 
sleep_time = 0.01
complement = True
length_between_generations = 1 
generations = False
graph = True
random_death_dict = {1: np.random.choice([0,1],p = [5/10, 5/10]), 0: 0 }
game_data = []

#much of this courtesy of NeuralNine, though it isn't exactly the same thing
def make_rand_mat():
    return np.random.choice([0,1], size = (DIM//TILE_SIZE, DIM//TILE_SIZE), p = [2/3, 1/3])


#DEFINING PERSISTENCE HOMOLOGY RELATED STUFF
def find_point_cloud(game_data):
    point_cloud_list = []
    for i in range(len(game_data)):
        t = i
        grid = game_data[i]
        for j,k in np.ndindex(grid.shape):
            if grid[j][k] == 1:
                point_cloud_list.append([j,k, length_between_generations * t])
    point_cloud_array = np.array(point_cloud_list)
#    print(point_cloud_array)
    return point_cloud_array

def point_cloud_to_txt(point_cloud_array):
    """this writes the game data into a format that is readable to the live ripser website. 
    Hopefully, we will be able to also use this to only look at certain parts of a game, as well
    as go back to past ones without having to re-create things manually"""
    done = False
    while not done:
        number = 1
        try:
            with open("game_data_{}.txt".format(number), "x") as game_data_file:
                for point in point_cloud_array:
                    game_data_file.write(str(point[0])+ "," +str(point[1])+"," + str(point[2]) + "\n")

            done = True

        except:
            number += 1
            if number > 20:
                print("either we have way too many files or i fucked up the code")
                done = True

def pointcloud_to_matrix(point_cloud, TILE_SIZE = TILE_SIZE, t= 0):
    """needs to specify n, and it won't work it t is too big"""
    matrix = np.zeros((DIM //TILE_SIZE , DIM //TILE_SIZE) )
    for point in point_cloud:
        if point[2] == t:
            matrix[point[0]][point[1]] = 1
    return matrix

def txt_to_pointcloud(name):
    point_cloud = []
    with open(name,"r") as f:
        for line in f:
            coordinates = line.split('')
            x = int(coordinates[0])
            y = int(coordinates[1])
            t = int(coordinates[2])
            point_cloud.append(x,y,t)
            
    return point_cloud
              
    
def find_point_cloud_complement(game_data):
    point_cloud_array = find_point_cloud(game_data)
    point_cloud_comp_list = []
    
    #same method as with find_point_cloud, but to reduce the size of what we are storing we are only storing
    # the data in a box around where actual stuff happens. This increases the time it takes but with any luck will decrease
    #the storage which was giving me, Tyler, an error 
    min_x = int(min(point_cloud_array[:,0]))
    max_x = int(max(point_cloud_array[:,0]))
    min_y = int(min(point_cloud_array[:,1]))
    max_y = int(max(point_cloud_array[:,1]))
    
    
    for i in range(len(game_data)):
        t = i
        grid = game_data[i]
        for j in range(min_x -1 ,max_x + 2 ):
                for k in range(min_y -1, max_y + 2):
                    if j < len(grid) and k < len(grid[0]):
                        if grid[j][k] == 0:
                            point_cloud_comp_list.append([j,k, length_between_generations * t])
    point_cloud_comp_array = np.array(point_cloud_comp_list)
    return point_cloud_comp_array


def point_cloud_ph(array):
    return ripser(find_point_cloud(array),2)['dgms']

def complement_ph(array):
    return ripser(find_point_cloud_complement(array),2)['dgms']



#DEFINING BIG FUNCTION STUFF
def update_grid_looped(grid,screen, update = False):
    
    grid_updated = np.zeros((grid.shape[0], grid.shape[1]), dtype = int)
    for row, col in np.ndindex(grid.shape):
        if update:
            alive = np.sum(grid[row-1:row + 2, col-1:col+2]) - grid[row,col]
            #It occured to me that because we are working on a finite grid, this isn't quite correct.
            
            if grid[row, col] == 1 and 3 >= alive >= 2:
                grid_updated[row, col] =1 
            elif grid[row, col] == 0 and 3 == alive:
                grid_updated[row, col] = 1
            else:
                grid_updated[row, col] = random_death_dict[random_death]
            
        else:
            grid_updated = grid

        color = BLACK
        if grid_updated[row, col] == 1:
            color = WHITE
        pg.draw.rect(screen, color, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 1, TILE_SIZE - 1))
    return grid_updated

#Now with hip new generations so we can take it for only a finite number of generations

def load_game(name = "z", t = 0, TILE_SIZE = TILE_SIZE):
    matrix = None
    if name == "r":
        matrix = make_rand_mat()
    elif name == 'z':
        matrix = np.zeros((DIM //TILE_SIZE , DIM //TILE_SIZE) )
    else:
        matrix = pointcloud_to_matrix(txt_to_pointcloud(name), TILE_SIZE, t)
        
    main(matrix)
    

def main(grid):

    
    
    pg.init()

    game_data = []
    screen = pg.display.set_mode((DIM, DIM))

    
    #screen.fill(BLACK)

    pg.display.flip()
    pg.display.update()


    running = False
    cells = grid

    while True:
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    if not running:
                        print(len(game_data), "frames have passed since start")
                    running = not running
                    
                if event.key == pg.K_RIGHT:
                    cells = update_grid_looped(cells, screen, update = True)
                    game_data.append(cells)
                    pg.display.update()

                if event.key == pg.K_c:
                    running = False
                    game_data = []
                    cells = np.zeros((DIM//TILE_SIZE, DIM//TILE_SIZE), dtype = int)
                    update_grid_looped(cells, screen)
                    pg.display.update()
                    
                if event.key == pg.K_r:
                    running = False
                    game_data = []
                    cells = make_rand_mat()
                    update_grid_looped(cells, screen)
                    pg.display.update()
                    
                if event.key == pg.K_s:
                    #saves game data as a txt file if you press S
                    running = False
                    points = find_point_cloud(game_data)
                    point_cloud_to_txt(points)
                    
                if event.key == pg.K_d:
                    game_data = []
                    
                if event.key == pg.K_p:
                    running = False
                    dgms1 = point_cloud_ph(game_data)
                    dgms2 = complement_ph(game_data)
                    print("Number of generations is", str(len(game_data)))
                    print("Point Cloud Diagram")
                    if graph == True:
                        ax = plt.axes(projection='3d')
                        ax.grid()
                        points = find_point_cloud(game_data)
                        ax.scatter(points[:,0], points[:,1], points[:,2], c = 'r', s = 50)
                        plt.show()
                    plot_diagrams(dgms1, show=True)
                    print(dgms1)
                    if complement == True: #There is probably a better way to do this, if anyone wants to change how we select
                                          #which persistence homologi we want to compute since we might assemble an arsenal
                        print("Point Cloud Complement Diagram")
                        if graph == True:
                            ax = plt.axes(projection='3d')
                            ax.grid()
                            points = find_point_cloud_complement(game_data)
                            ax.scatter(points[:,0], points[:,1], points[:,2], c = 'r', s = 50)
                            plt.show()
                        
                        plot_diagrams(dgms2, show = False)
                        plt.savefig('saving')
                        print(dgms2)
                
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                
            if pg.mouse.get_pressed()[0]:
                pos = pg.mouse.get_pos()
                if cells[pos[1]//TILE_SIZE, pos[0]//TILE_SIZE] == 0:
                    cells[pos[1]//TILE_SIZE, pos[0]//TILE_SIZE] = 1
                else:
                    cells[pos[1]//TILE_SIZE,pos[0]//TILE_SIZE] = 0 
                    
                update_grid_looped(cells, screen)
                pg.display.update()
        
        if generations != False: #this code checks if t = generations and if so, stops 
            if len(game_data) == generations:
                print(len(game_data), "frames have passed game quitting")
                dgms = point_cloud_ph(game_data)
                plot_diagrams(dgms, show=True)
                pg.quit()
            
        if running:

            cells = update_grid_looped(cells, screen, update = True)
            game_data.append(cells)
            pg.display.update()

        time.sleep(sleep_time)
        
if __name__ == "__main__":
    main(load_game('r'))