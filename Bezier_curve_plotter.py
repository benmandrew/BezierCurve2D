## ----------------------------------------------- ##
## https://en.wikipedia.org/wiki/B%C3%A9zier_curve ##
## ----------------------------------------------- ##

from random import randint
import pygame
from pygame.locals import *

pygame.init()

WIDTH = 1920 # Screen dimensions
HEIGHT = 1080
TICK_RATE = 30 # Framerate
ORDER = randint(2, 8) # Order of the bezier curve
INCREMENT = 0.005 # Incrementation of line in percent/100

font = pygame.font.SysFont("monospace", 15) # Standard font

# - Instructional text -
instruction_text_list = list()
instruction_list = ("Press space to pause the simulation", "Press R to restart the simulation", "Press H to toggle contruction lines", "Press G to toggle tutorial text", "Press F to toggle fullscreen", "Press ESC to exit")
for i in range(len(instruction_list)):
    temp_text = font.render(instruction_list[i], 1, (255, 255, 255))
    instruction_text_list.append(temp_text)
# ----------------------

# - Informational text -
information_text_list = list()
information_list = ("Order: " + str(ORDER))


order_text = font.render("Order: " + str(ORDER), 1, (255, 255, 255))
# ----------------------

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

running = True
show_construction = True
show_text = True
pause = False
infinite_loop = True
fullscreen = False

clock = pygame.time.Clock()

class Point:
    """
    A point class,
    it's a lot easier
    than x0, y0, x1
    etc and allows
    me to have as
    many orders as
    I want.
    """
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self, colour = (255, 255, 255)):
        # Nice easy draw function
        pygame.draw.circle(screen, colour, (self.x, self.y), self.radius, 0)

def draw_construction_lines(point_list, colour_list):
    """
    Self explanatory
    """
    for i in range(len(point_list)):
        # Iterate over each of the layers
        if len(point_list[i]) == 1:
            # If the plotter has been reached, stop.
            break
        for p in range(len(point_list[i]) - 1):
            # Join each point up with it's right neighbor
            colour = (colour_list[i][0], colour_list[i][1], colour_list[i][2])
            point0 = point_list[i][p]
            point1 = point_list[i][p+1]
            pygame.draw.aaline(screen, colour, (point0.x, point0.y), (point1.x, point1.y), True)

def draw_curve(point_list, increment):
    """
    Draw the curve
    by stringing up
    the points in a
    chain, looks pretty
    bad but hey ho
    """
    for i in range(increment):
        point0 = point_list[i]
        point1 = point_list[i+1]
        if point1.x == 0 and point1.y == 0:
            continue # The next point is default, so it's coordinates are (0, 0) which look weird when joined up
        pygame.draw.line(screen, (255, 255, 255), (point0.x, point0.y), (point1.x, point1.y), 2)

def calc_new_points(point_list, percentage):
    """
    Calculate all
    the new points
    for the given
    percentage.
    """
    for i in range(len(point_list)):
        for p in range(len(point_list[i]) - 1):

            point0 = point_list[i][p] # Set points in list to variables,
            point1 = point_list[i][p+1] # makes subsequent code easier to read.

            xdiff = point1.x - point0.x # Find the differences
            ydiff = point1.y - point0.y
            xdiff *= percentage # Find percentage of the differences
            ydiff *= percentage

            xnew = int(point0.x + xdiff) # Get the new position of the points
            ynew = int(point0.y + ydiff)

            point_list[i+1][p].x = xnew # Apply the new positions to lower layers
            point_list[i+1][p].y = ynew

    return point_list

# Generate the top layer of construction points randomly
position_list = list()
for i in range(ORDER + 1):
    position_list.append((randint(0, WIDTH), randint(0, HEIGHT)))
construction_point_list = list()

#
new_point_num = ORDER + 1
while new_point_num > 0:
    temp_list = list()
    for i in range(new_point_num):
        temp_point = Point(position_list[i][0], position_list[i][1], 3)
        temp_list.append(temp_point)
    construction_point_list.append(temp_list)
    new_point_num -= 1

colour_list = [(200, 200, 200)]
for i in range(ORDER - 1):
    colour_list.append((randint(0, 255), randint(0, 255), randint(0, 255)))

percentage = 0
plot_increment = 0

# Point objects are created
# prior to the simulation to
# prevent unnecessary creation
# after the curve has been calculated
plot_point_list = list()
for i in range(int(1/INCREMENT)):
    temp_point = Point(0, 0, 0)
    plot_point_list.append(temp_point)

# ----------- Game loop -----------
while running:

    # ------------------ Events -------------------
    events = pygame.event.get()
    for event in events:

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_h: # 'H' key
                show_construction = not show_construction # Hide or show the construction lines
                
            if event.key == pygame.K_g: # 'G' key
                show_text = not show_text # Hide or show the instructional text
                
            if event.key == pygame.K_f: # 'F' key
                pass # Toggle fullscreen
            
            if event.key == pygame.K_r: # 'R' key
                percentage = 0 # Restart the simulation
                plot_increment = 0
                for i in range(int(1/INCREMENT)):
                    plot_point_list[i].x = 0
                    plot_point_list[i].y = 0
                    
            if event.key == pygame.K_SPACE: # 'Space' key
                pause = not pause # Pause the simulation
                
            if event.key == pygame.K_ESCAPE: # 'Escape' key
                running = False # Exit the simulation

        if event.type == VIDEORESIZE: # Window resize event
            WIDTH = event.w
            HEIGHT = event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    ## --------------------------------------------


    ## --------------- Full restart ---------------
    if infinite_loop and (percentage >= 1):
        ## Incredibly messy code that is here because I quickly wanted the functionality as a sort of screensaver
        ## Set infinite_loop to false if you don't want this
        percentage = 0
        plot_increment = 0
        plot_point_list = list()
        for i in range(int(1/INCREMENT)):
            temp_point = Point(0, 0, 0)
            plot_point_list.append(temp_point)
        for i in range(int(1/INCREMENT)):
            plot_point_list[i].x = 0
            plot_point_list[i].y = 0
        ORDER = randint(2, 8)
        colour_list = [(255, 255, 255)]
        for i in range(ORDER - 1):
            colour_list.append((randint(0, 255), randint(0, 255), randint(0, 255)))
        position_list = list()
        for i in range(ORDER + 1):
            position_list.append((randint(0, WIDTH), randint(0, HEIGHT)))
        construction_point_list = list()
        new_point_num = ORDER + 1
        while new_point_num > 0:
            temp_list = list()
            for i in range(new_point_num):
                temp_point = Point(position_list[i][0], position_list[i][1], 3)
                temp_list.append(temp_point)
            construction_point_list.append(temp_list)
            new_point_num -= 1
        order_text = font.render("Order: " + str(ORDER), 1, (255, 255, 255))
    ## --------------------------------------------

    if (percentage <= 1) and not pause:
        # First statement argument checks if the percentage is below or equal to 1, otherwise the construction lines would go over the top layer
        # The second checks if it's paused
        calc_new_points(construction_point_list, percentage)
        percentage += INCREMENT

        ## Calculate the new plot points
        plot_point_list[plot_increment].x = construction_point_list[-1][0].x
        plot_point_list[plot_increment].y = construction_point_list[-1][0].y
        if plot_increment < (1/INCREMENT) - 1:
            plot_increment += 1





    screen.fill((20, 20, 25)) # Fill the screen with colour (sort of a reset)

    if show_text:
        y_pos = -23
        for text_obj in instruction_text_list:
            screen.blit(text_obj, (10, HEIGHT + y_pos))
            y_pos -= 20

    screen.blit(order_text, (10, 20))

    fps_text = font.render("FPS: " + str(round(clock.get_fps(), 1)), 1, (255, 255, 255))
    screen.blit(fps_text, (10, 5))

    time_text = font.render("Tick: " + str(round(percentage, 2)), 1, (255, 255, 255))
    screen.blit(time_text, (10, 35))

    if show_construction:
        for i in range(len(construction_point_list)):
            for p in range(len(construction_point_list[i])):
                point = construction_point_list[i][p]
                point.draw()
        draw_construction_lines(construction_point_list, colour_list)


    draw_curve(plot_point_list, plot_increment)

    pygame.display.flip()
    clock.tick(TICK_RATE)


























































