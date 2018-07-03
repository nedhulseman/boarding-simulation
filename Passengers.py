import pygame, sys
from pygame.locals import *
from random import shuffle
import math
import time
import pickle

'''
    This module is used to make the passengers board the plane and go to their respective seats
    I plan for the following boarding methods all with varying number of zones
        1) random boarding zones
        2) front to back boarding zones
        3) back to front boarding zones
        4) simply boarding in order (no zones)
    
    I will implement the class passenger with the following methods
        @default constructor __init__()
        @create_line()                   -- instantiates line positions
        @assign_seats()                  -- assigns seats to each member in line
        @board                           -- actually starts the boarding process
'''



#creation of colors
BLACK=(0,0,0)
OBSIDIAN=(61,53,75)
WHITE=(255, 255, 255)
RED=(255, 0, 0)
GREEN=(0, 255, 0)
BLUE=(0, 0, 255)
GREY=(220,220,220)



class passengers:
    
    def __init__(self, windowSurface, move_speed, boarding_procedure, num_zones, seat_locations, 
                 left_aisle, right_aisle, row1Y, seat_width, left_plane, brdg_wide, brdg_to_plane):
        
        self.num_seats           = len(seat_locations)
        self.start_cords         = [50, 735] # clean this up
        self.radius              = 10
        self.personal_bubble     = 15
        self.seat_locations      = seat_locations
        
        self.boarding_procedure  = boarding_procedure
        self.num_zones           = num_zones
        
        self.windowSurface       = windowSurface
        
        #List containg a list of X,Y cords for the passengers curent position n-passengers long
        self.passenger_positions = self.create_line()
        self.seat_assignments    = self.assign_seats(seat_locations)
        self.move_speed          = move_speed
        self.load_carryon_timer  = 160
        
        # needed dimensions to guide passengers through the right path
        self.left_aisle          = left_aisle
        self.right_aisle         = right_aisle
        self.row1Y               = row1Y
        self.seat_width          = seat_width
        self.left_plane          = left_plane
        self.brdg_wide           = brdg_wide
        self.brdg_to_plane       = brdg_to_plane
        
        self.passenger_info = self.instantiate_passenger_info(self.passenger_positions, self.seat_assignments)
        
        self.iterations = 1
        self.start = 0
        self.end = 0
        self.time_tracker = []
        self.pickled = False
        self.start_timer = False


        return None


    def instantiate_passenger_info(self, passenger_positions, seat_assignments):
        passenger_info = {}
        for i in range(0, self.num_seats):
            passenger_info[str(i+1)] = {'passenger_position' : passenger_positions[i],
                                      'seat_assignment'    : seat_assignments[i],
                                      'boarding_status'    : 'boarding',
                                      'loading_timer'      : 0}
        return passenger_info
    
    def create_line(self): #creates starting line positions
        passenger_positions = []
        X = self.start_cords[0]
        Y = self.start_cords[1]
        
    
        for i in range(0, self.num_seats):
            passenger_positions.append([X, Y])
            X    -= (self.radius*2) + self.personal_bubble
            
        return passenger_positions

    def assign_seats(self, seat_locations): # currently just assigns random seats
        
        if self.num_zones != None:
            row_cords = []
            for seat in self.seat_locations:
                if seat[1] not in row_cords:
                    row_cords.append(seat[1])
            
            num_rows = len(row_cords)
            num_aisles = len(seat_locations) / num_rows
            mod = num_rows % self.num_zones 
            
            rows_in_each_zone = []
            for i in range(0, self.num_zones):
                if mod == 0:
                    rows_in_each_zone.append(int(num_rows / self.num_zones))
                else:
                    rows_in_each_zone.append(int(num_rows / self.num_zones) + 1 )
                    mod -= 1


        if self.boarding_procedure == 'random':
            shuffle(seat_locations)
        
        elif self.boarding_procedure == 'front_to_back':
            f2b_order = []
            start = 0
            for num_row_in_zone in rows_in_each_zone:
                end = start + (num_row_in_zone * num_aisles)
                seats_in_zone = seat_locations[int(start) : int(end)]
                shuffle(seats_in_zone)
                for seat in seats_in_zone:
                    f2b_order.append(seat)
                
                
                start = end
            seat_locations = f2b_order
            
        elif self.boarding_procedure == 'back_to_front':
            b2f_order = []
            end = len(seat_locations)
            for num_row_in_zone in rows_in_each_zone:
                start = end - (num_row_in_zone * num_aisles)
                seats_in_zone = seat_locations[int(start) : int(end)]
                shuffle(seats_in_zone)
                for seat in seats_in_zone:
                    b2f_order.append(seat)
                
                end = start
            seat_locations = b2f_order

        


        return seat_locations

        
        
        
        
      
            
        
                        
    def board(self, num_iterations):
        
        people_not_seated = [person for person in self.passenger_info.keys() if self.passenger_info[person]['boarding_status'] != 'seated']
      
        if len(people_not_seated) == self.num_seats and self.start_timer == False:
            self.start = time.time()
            self.start_timer = True
        elif len(people_not_seated) == 0 and self.iterations < num_iterations:
            self.end = time.time()
            self.time_tracker.append(self.end - self.start)
            start_timer = False
            self.passenger_positions = self.create_line()
            self.seat_assignments    = self.assign_seats(self.seat_locations)                
            self.passenger_info = self.instantiate_passenger_info(self.passenger_positions, self.seat_assignments)
            print(self.iterations)
            self.iterations += 1
        
        elif len(people_not_seated) == 0 and self.iterations == num_iterations and self.pickled == False:
            with open(str(self.boarding_procedure) + '.pkl', 'wb') as f:
                pickle.dump(self.time_tracker, f) 
                self.pickled = True

       
        for i in range(1, self.num_seats + 1):
    

            try:
                if len(people_not_seated) == 2 and i < people_not_seated[people_not_seated.index(str(i)) - 1]:
                    person_in_front_pos = [99999999, 99999999]
                elif len(people_not_seated) == 1:
                    person_in_front_pos = [99999999, 99999999]
                else:
                    person_in_front_pos = self.passenger_info[people_not_seated[people_not_seated.index(str(i)) - 1]]['passenger_position']
            except:
                person_in_front_pos = [99999999, 99999999]


            if i != 1 and self.passenger_info[str(i)]['boarding_status'] != 'seated' and  math.sqrt((self.passenger_info[str(i)]['passenger_position'][0]-person_in_front_pos[0])**2 + (self.passenger_info[str(i)]['passenger_position'][1]-person_in_front_pos[1])**2) < self.personal_bubble + self.radius:
                pass
            
            elif self.passenger_info[str(i)]['boarding_status'] == 'loading':
                self.passenger_info[str(i)]['loading_timer'] += 1
                
                if self.passenger_info[str(i)]['loading_timer'] == self.load_carryon_timer:
                    self.passenger_info[str(i)]['boarding_status'] = 'sitting'                
            
            #Check to see if person has sat in correct seat... if so then don't do anything
            elif self.passenger_info[str(i)]['passenger_position'][0] == self.passenger_info[str(i)]['seat_assignment'][0]+int(self.seat_width/2) and self.passenger_info[str(i)]['passenger_position'][1] == self.passenger_info[str(i)]['seat_assignment'][1]:

                pass
            
             #if person is at or past their row location
            elif self.passenger_info[str(i)]['passenger_position'][1] >= self.passenger_info[str(i)]['seat_assignment'][1] - self.radius and self.passenger_info[str(i)]['passenger_position'][0] > self.left_plane:
                self.passenger_info[str(i)]['passenger_position'][1]  = self.passenger_info[str(i)]['seat_assignment'][1] - self.radius
                #if passenger hasemt started loading bag, start loading
                if self.passenger_info[str(i)]['boarding_status'] == 'boarding':
                    self.passenger_info[str(i)]['boarding_status'] = 'loading'
                #if the person's seat is to the left go left
                elif self.passenger_info[str(i)]['passenger_position'][0] >= self.passenger_info[str(i)]['seat_assignment'][0]+int(self.seat_width/2):
                    self.passenger_info[str(i)]['passenger_position'][0] -= self.move_speed
                    #prevents person from moving past their seat
                    if self.passenger_info[str(i)]['passenger_position'][0] <= self.passenger_info[str(i)]['seat_assignment'][0]+int(self.seat_width/2):
                        self.passenger_info[str(i)]['boarding_status'] = 'seated'
                        self.passenger_info[str(i)]['passenger_position'][0] = self.passenger_info[str(i)]['seat_assignment'][0]+int(self.seat_width/2)
                #if the person's seat is to the right, then go to the right
                elif self.passenger_info[str(i)]['passenger_position'][0] <= self.passenger_info[str(i)]['seat_assignment'][0]+int(self.seat_width/2):
                    self.passenger_info[str(i)]['passenger_position'][0] += self.move_speed
                    #prevents person from moving past their seat
                    if self.passenger_info[str(i)]['passenger_position'][0] >= self.passenger_info[str(i)]['seat_assignment'][0]+int(self.seat_width/2):
                        self.passenger_info[str(i)]['boarding_status'] = 'seated'
                        self.passenger_info[str(i)]['passenger_position'][0] = self.passenger_info[str(i)]['seat_assignment'][0]+int(self.seat_width/2)
            #if person has not arrived at their row, but is on plane, then walk down the aisle
            #if person is at or past the middle of the plane aisle
            elif self.passenger_info[str(i)]['passenger_position'][0] >= self.left_aisle + (self.right_aisle - self.left_aisle)/2:
                self.passenger_info[str(i)]['passenger_position'][0] = int(self.left_aisle + (self.right_aisle - self.left_aisle)/2)
                self.passenger_info[str(i)]['passenger_position'][1] += self.move_speed
                
               
            #if person reaches second bridge elbow, then walk onto plane
            elif self.passenger_info[str(i)]['passenger_position'][1] <= self.row1Y-10-int(self.brdg_wide/2):
                self.passenger_info[str(i)]['passenger_position'][1] = self.row1Y-10-int(self.brdg_wide/2)
                self.passenger_info[str(i)]['passenger_position'][0] += self.move_speed
            #if person reaches first bridge elbow then walk up
            elif self.passenger_info[str(i)]['passenger_position'][0] >= self.left_plane-(int(self.brdg_wide/2)+self.brdg_to_plane):
                self.passenger_info[str(i)]['passenger_position'][0] = self.left_plane-(int(self.brdg_wide/2)+self.brdg_to_plane)
                self.passenger_info[str(i)]['passenger_position'][1] -= self.move_speed 
            #if just starting on bridge walk forward(right)
            else:
                self.passenger_info[str(i)]['passenger_position'][0] += self.move_speed
            
            #draws passenger
            pygame.draw.circle(self.windowSurface, RED, tuple(self.passenger_info[str(i)]['passenger_position']), self.radius)
            


    
    
    
    
    
    

