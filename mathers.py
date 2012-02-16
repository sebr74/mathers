#!/usr/bin/python
# -*- coding: utf-8 -*-'''

'''
Created on 2012-02-06

@author: Sebastien Renaud 
'''
import pygame
import random
import sys


# Define some colors
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
green    = (   0, 255,   0)
red      = ( 255,   0,   0)
message_timeout = 3000


def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # pressing escape quits
                    terminate()
                return


class Question:
    def __init__(self, question_text=None, answer=None):
        if question_text:
            self.text = question_text
            self.answer = answer
        else:
            self.update()
            
    def answer_is_valid(self,answer):
        if self.answer == answer:
            return True
        else:
            return False
    def update(self):
        a = random.randint(1,12)
        b = random.randint(1,12)
        self.answer = a * b
        self.text = '%d x %d = ?' % (a,b)
    def render(self, screen):
        if self.text:
            font = pygame.font.Font(None, 25)
            text = font.render(self.text,True,green)
            screen.blit(text, [250,250])

class Game:
    def __init__(self):
        pygame.init()
        # Set the height and width of the screen
        size=[700,500]
        self.scr=pygame.display.set_mode(size)
        self.clk=pygame.time.Clock()
        pygame.display.set_caption("Mathers")
        self.message = u"Bienvenue à Mathers"
        self.a = None
        self.q = None
        self.message_timeout = 0
    def update(self):
        # check if there is a new answer
        if self.a:
            print "checking %d" % self.a
            if self.q.answer_is_valid(self.a):
                self.message = "BRAVO"
                self.a = None
                self.q = Question()
            else:
                # Oops
                self.message =  "OOPS"
                self.a = None
    def render(self):
        self.scr.fill(black)
        if self.message:
            font = pygame.font.Font(None, 25)
            text = font.render(self.message,True,red)
            self.scr.blit(text, [250,350])
            self.message_timeout += time_chunk
            if self.message_timeout > message_timeout:
                self.message = None
                self.message_timeout = 0
        if self.q:
            self.q.render(self.scr)
            
if __name__ == '__main__':
    g = Game()
    time_chunk = 0
    g.render()
    pygame.display.flip()
    waitForPlayerToPressKey()
    g.q = Question()
    done=False
    user_input = ''
    while done==False:
        time_chunk = g.clk.tick(20)
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done=True # Flag that we are done so we exit this loop
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # pressing escape quits
                    done=True # Flag that we are done so we exit this loop
                    break
                for key in '0123456789':
                    if event.key == ord(key): 
                        user_input += key
                if event.key == pygame.K_RETURN: 
                    if user_input:
                        g.a = int(user_input)
                        user_input = ''
                        break
            
        g.render()
        g.update()
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

    
        

    
