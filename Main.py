import pygame, sys
from pygame.locals import *
from random import shuffle
from Draw import draw
from Passengers import passengers
import time


num_rows = 28
num_aisles = 6
boarding_procedures = ['random', 'front_to_back', 'back_to_front']
num_zones = 4
num_iterations = 51
move_speed = 4
refresh_rate = 0



def main(num_rows, num_aisles, refresh_rate, num_iterations, move_speed, boarding_procedure, num_zones):#, boarding_procedures, num_zones = None):

    pygame.init()
    windowSurface = pygame.display.set_mode((1200, 770), 0, 32)
    pygame.display.set_caption('Airport')
    drawing = draw(windowSurface, num_rows, num_aisles)
    seats = drawing.seats()
    
    passengersz = passengers(windowSurface, move_speed, boarding_procedure, num_zones, seats['seat_locations'], seats['left_aisle'], seats['right_aisle'],
                            seats['row1Y'], seats['seat_width'], seats['left_plane'], seats['brdg_wide'], seats['brdg_to_plane'])
    
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
        
        windowSurface.fill((255, 255, 255)) 
    
        drawing.plane()  
        drawing.seats()
        drawing.jet_bridge()    
    
        passengersz.board(num_iterations)
    
        pygame.display.update()
    
        time.sleep(refresh_rate)

main(num_rows, num_aisles, refresh_rate, num_iterations, move_speed, boarding_procedures[1], num_zones)



        
