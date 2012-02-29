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
yellow   = ( 255, 255,   0)

# support numpad values
keynum = {
 48:'0',256:'0'
,49:'1',257:'1'
,50:'2',258:'2'
,51:'3',259:'3'
,52:'4',260:'4'
,53:'5',261:'5'
,54:'6',262:'6'
,55:'7',263:'7'
,56:'8',264:'8'
,57:'9',265:'9'}
K_NUMPAD_RETURN = 271

message_timeout = 1000


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
    unknowns=['ANS','FIRST','SECOND','OPERATOR']
    operators=['+','-','*','/']
    
    def __init__(self):
        self.operator = self.operators[random.randint(0,len(self.operators)-1)]
        self.unknown = self.unknowns[random.randint(0,len(self.unknowns)-1)]
        if self.operator == '+':
            self.first = random.randint(1,12)
            self.second = random.randint(1,12)
            self.answer = self.first + self.second
        elif self.operator == '-':
            self.first = random.randint(1,12)
            self.second = random.randint(1,12)
            while self.second > self.first:
                self.second = random.randint(1,12)
            self.answer = self.first - self.second
        elif self.operator == '*':
            self.first = random.randint(1,12)
            self.second = random.randint(1,12)
            self.answer = self.first * self.second
        elif self.operator == '/':
            self.first = random.randint(4,12)
            self.second = random.randint(1,12)
            while self.first < self.second and self.first % self.second != 0:
                self.second = random.randint(1,12)
            self.answer = self.first / self.second

        self.reset_text()
        
    def reset_text(self):
        if self.unknown == 'FIRST':
            self.text = '?'
            self.valid_input = '%d' % self.first
        else:
            self.text = '%d' % self.first
        if self.unknown == 'OPERATOR':
            self.text += ' ?'
            self.valid_input = '%s' % self.operator
        else:
            self.text += ' ' + self.operator
        if self.unknown == 'SECOND':
            self.text += ' ?'
            self.valid_input = '%d' % self.second
        else:
            self.text += ' %d' % self.second
        self.text += ' ='
        if self.unknown == 'ANS':
            self.text += ' ?'
            self.valid_input = '%d' % self.answer
        else:
            self.text += ' %d' % self.answer
        
        self.color = green
        self.size = 50
            
    def answer_is_valid(self,user_input):
        if self.valid_input == user_input:
            self.color = green
            self.size = 70
            return True
        else:
            self.reset_text()
            return False
    
    def update(self, user_input):
        if self.unknown == 'FIRST':
            self.text = '%s' % user_input
        else:
            self.text = '%d' % self.first
        if self.unknown == 'OPERATOR':
            self.text += ' %s' % user_input
        else:
            self.text += ' ' + self.operator
        if self.unknown == 'SECOND':
            self.text += ' %s' % user_input
        else:
            self.text += ' %d' % self.second
        self.text += ' ='
        if self.unknown == 'ANS':
            self.text += ' %s' % user_input
        else:
            self.text += ' %d' % self.answer
        
        self.color = yellow
        self.size = 40
        
    def render(self, screen):
        if self.text:
            font = pygame.font.Font(None, self.size)
            text = font.render(self.text,True,self.color)
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
    def update(self, user_input):
        # check if there is a new answer
        if self.a != None:
            print "checking %s" % self.a
            if self.q.answer_is_valid(self.a):
                self.message = "BRAVO"
                self.a = None
            else:
                # Oops
                self.message =  "OOPS"
                self.a = None
        else:
            if user_input != '':
                self.q.update(user_input)
            
    def render(self):
        self.scr.fill(black)
        if self.message:
            font = pygame.font.Font(None, 25)
            text = font.render(self.message,True,red)
            self.scr.blit(text, [250,350])
            self.message_timeout += time_chunk
            if self.message_timeout > message_timeout:
                if self.message == "BRAVO":
                    self.q = Question()
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
                for key, char in keynum.iteritems():
                    if event.key == key: 
                        user_input += keynum[key]
                if event.key == pygame.K_RETURN or event.key == K_NUMPAD_RETURN: 
                    if user_input != '':
                        g.a = user_input
                        user_input = ''
                        break
                print event
            
        g.render()
        g.update(user_input)
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

    
        

    
