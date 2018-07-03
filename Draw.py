import pygame, sys
from pygame.locals import *



'''
    This module is used to draw everything that doesn't move
        ie)
        plane
        seats
        jet bridge
        ticket counter
        
    In order to do this I will create one class @draw
    Methods:
            @default constructor __init__()
                arguments   -- windowSurface object, desired number of rows, number of aisles
            @plane()        -- draws the fuselage
            @seats()        -- iterated through the rows draws and saves the seat locations
            @jet_bridge()   -- draws the jet bridge
'''




#creation of colors
BLACK=(0,0,0)
OBSIDIAN=(61,53,75)
WHITE=(255, 255, 255)
RED=(255, 0, 0)
GREEN=(0, 255, 0)
BLUE=(0, 0, 255)
GREY=(220,220,220)







class draw:
    
    '''
        This class will be used to draw all non-moving parts in the airport
        
        @num_rows    : number of rows on the plane
        @num_aisles : number of aisles
    '''
    def __init__(self, windowSurface, num_rows, num_aisles):
        
        #converts the arguments to attributes
        self.num_rows         = num_rows
        self.num_aisles       = num_aisles
        self.windowSurface   = windowSurface
        
        #dictionary for the plane's width based on number of aisles
        self.planeWidth_dict = {3:200, 4:240, 5:270, 6:300}
    
        #The plane's dimensions
        self.DISPLAY_HEIGHT  = 770
        self.left_plane      = 800
        self.PLANE_WIDTH     = self.planeWidth_dict[self.num_aisles]
        self.RIGHT_PLANE     = self.left_plane + self.PLANE_WIDTH
        self.FRONT_PLANE     = 0
        self.BACK_PLANE      = self.DISPLAY_HEIGHT
        
        #The seats dimensions
        self.row1Y           = 65
        self.SEAT_WIDTH      = 40
        self.SEAT_HEIGHT     = 7
        self.aisle_space     = self.SEAT_WIDTH + 2
        self.row_space       = self.SEAT_HEIGHT + 20
        
        #The Jet Bridge dimensions
        self.brdg_wide       = 50
        self.BRDG_TOP        = 710
        self.brdg_to_plane   = 40
        self.TICKET_LEN      = 50
        
        return None



    def plane(self): 
        #drawing the fuselage
        pygame.draw.rect(self.windowSurface, GREY, (self.left_plane, self.FRONT_PLANE, self.PLANE_WIDTH, self.BACK_PLANE)) 
        
    def seats(self):
        #drawing the seats
        
        #dictionary used to monitor the number of seats in each aisle
        #If an odd number of aisles, the left section will have 1 more row than right
        maxSeatsInAisle = {3:2, 4:2, 5:3, 6:3}
        
        #Saves the left and right positions of the aisle -- will be used in @Passengers module
        left_aisle = self.left_plane + (maxSeatsInAisle[self.num_aisles] * (self.SEAT_WIDTH + self.aisle_space)) - self.aisle_space
        if (self.num_aisles) % 2 == 0: #if even number of aisles
            right_aisle = self.RIGHT_PLANE - (maxSeatsInAisle[self.num_aisles] * (self.SEAT_WIDTH + self.aisle_space)) + self.aisle_space
        else:
            right_aisle = self.RIGHT_PLANE - (maxSeatsInAisle[self.num_aisles - 1] * (self.SEAT_WIDTH + self.aisle_space)) - self.aisle_space
        
        #creates a null list that will be used to save the locations of the seats
        #will be used in Passengers module to  board
        seat_locations = []
        
        #instantiates the positions of the seats
        seatX = self.left_plane
        seatY = self.row1Y           
        for i in range(1, self.num_rows + 1): #iterates through each row
            seatX = self.left_plane
            
            for j in range(1, self.num_aisles + 1): #iterates through the aisles
                pygame.draw.rect(self.windowSurface, BLACK, (seatX, seatY, self.SEAT_WIDTH, self.SEAT_HEIGHT)) 
                seat_locations.append([seatX, seatY])
                
                #This makes sure the x value of the seat is being set correctly
                if int(j) == maxSeatsInAisle[self.num_aisles]: #if max seats in aisle then start drawing the right section
                    seatX = self.RIGHT_PLANE - self.SEAT_WIDTH
                elif int(j) > maxSeatsInAisle[self.num_aisles]: # if it is in the right section
                    seatX -= self.aisle_space
                else:  #if it is in the left section  
                    seatX += self.aisle_space    
                
               
            seatY += self.row_space


                
        
        return {'seat_locations' : seat_locations, 
                'left_aisle'     : left_aisle, 
                'right_aisle'    : right_aisle,
                'brdg_wide'      :  self.brdg_wide,
                'BRDG_TOP'       :  self.BRDG_TOP,
                'brdg_to_plane'  :  self.brdg_to_plane,
                'TICKET_LEN'     :  self.TICKET_LEN,
                'left_plane'     : self.left_plane,
                'row1Y'          : self.row1Y,
                'seat_width'     : self.SEAT_WIDTH
                }
    
    def jet_bridge(self):
        #draws the jet bridge based on given attirbutes
        
        pygame.draw.line(self.windowSurface, BLACK, (0, self.BRDG_TOP+self.brdg_wide), (self.left_plane-self.brdg_to_plane, self.BRDG_TOP+self.brdg_wide))
        pygame.draw.line(self.windowSurface, BLACK, (0, self.BRDG_TOP), (self.left_plane-(self.brdg_wide+self.brdg_to_plane), self.BRDG_TOP))
        
        pygame.draw.line(self.windowSurface, BLACK, (self.left_plane-self.brdg_to_plane, self.BRDG_TOP+self.brdg_wide), (self.left_plane-self.brdg_to_plane, self.row1Y-10))
        pygame.draw.line(self.windowSurface, BLACK, (self.left_plane-(self.brdg_to_plane+self.brdg_wide), self.BRDG_TOP), (self.left_plane-(self.brdg_to_plane+self.brdg_wide), self.row1Y-10-self.brdg_wide))
        
        
        pygame.draw.line(self.windowSurface, BLACK, (self.left_plane-self.brdg_to_plane, self.row1Y-10), (self.left_plane, self.row1Y-10))
        pygame.draw.line(self.windowSurface, BLACK, (self.left_plane-(self.brdg_to_plane+self.brdg_wide), self.row1Y-10-self.brdg_wide), (self.left_plane, self.row1Y-10-self.brdg_wide))
        
        pygame.draw.rect(self.windowSurface, RED, (200, self.BRDG_TOP-self.TICKET_LEN, self.TICKET_LEN, self.TICKET_LEN))
        pygame.draw.line(self.windowSurface, RED, (200, self.BRDG_TOP), (200, self.BRDG_TOP+self.brdg_wide))
        

    



