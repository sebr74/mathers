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

# support numpad values ans some shift values
keynum = {
 48:['0',')'],256:['0','0']
,49:['1','!'],257:['1','1']
,50:['2','@'],258:['2','2']
,51:['3','#'],259:['3','3']
,52:['4','$'],260:['4','4']
,53:['5','%'],261:['5','5']
,54:['6','%'],262:['6','6']
,55:['7','&'],263:['7','7']
,56:['8','*'],264:['8','8']
,57:['9','('],265:['9','9']
,45:['-','_']
,47:['/','?']
,61:['=','+']
,267:['/','/']
,268:['*','*']
,269:['-','-']
,270:['+','+']
}
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
        if self.unknown == 'OPERATOR' and self.second == 1:
            if self.operator == '*' or self.operator == '/':
                if user_input == '*' or user_input == '/':
                    return True
        if self.valid_input == user_input:
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
        
    def render(self, screen):
        if self.text:
            font = pygame.font.Font(None, self.size)
            text = font.render(self.text,True,self.color)
            sx, sy = screen.get_size()
            fx, fy = font.size(self.text)
            screen.blit(text, [sx/2-fx/2,sy/2-fy/2])

# states
WAITING_FOR_INPUT = 0
SOME_INPUT_PRESENT = 1
ANS_SUBMITTED = 2 
ANS_VALID = 3
CONGRADULATE = 4
ANS_WRONG = 5
PUNISH = 6
QUIT = 7

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
        self.user_input = ''
        self.state = WAITING_FOR_INPUT
        
    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = QUIT
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # pressing escape quits
                    self.state = QUIT
                    break
                for key, char in keynum.iteritems():
                    if event.key == key:
                        self.state = SOME_INPUT_PRESENT 
                        g.user_input += keynum[key][event.mod&1]
                if event.key == pygame.K_RETURN or event.key == K_NUMPAD_RETURN: 
                    if g.user_input != '':
                        self.state = ANS_SUBMITTED
                        g.a = g.user_input
                        break
                if event.key == pygame.K_BACKSPACE:
                    # erase last char of user input
                    if len(g.user_input) <= 1:
                        g.user_input = ''
                        self.state = WAITING_FOR_INPUT
                    else:                        
                        g.user_input = g.user_input[:len(g.user_input)-1]
                print event
        
        
    def update(self):
        # empty input queue
        self.process_events()
        if self.state == WAITING_FOR_INPUT:
            self.q.reset_text()
        elif self.state == SOME_INPUT_PRESENT:
            self.q.color = yellow
            self.q.size = 50
            self.q.update(g.user_input)
        elif self.state == ANS_SUBMITTED:
            if self.q.answer_is_valid(g.user_input):
                self.state = ANS_VALID
            else:
                self.state = ANS_WRONG
        elif self.state == ANS_VALID:
            self.q.size = 70
            self.q.color = green
            self.q.update(g.user_input)
            self.timeout = 0
            self.state = CONGRADULATE
        elif self.state == CONGRADULATE:
            self.timeout += time_chunk
            if self.timeout > message_timeout:
                self.q = Question()
                g.user_input = ''
                self.state = WAITING_FOR_INPUT
        elif self.state == ANS_WRONG:
            self.q.color = red
            self.q.update(g.user_input)
            self.timeout = 0
            self.state = PUNISH
        elif self.state == PUNISH:
            self.timeout += time_chunk
            if self.timeout > message_timeout:
                g.user_input = ''
                self.state = WAITING_FOR_INPUT
            
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

    while g.state!=QUIT:
        time_chunk = g.clk.tick(20)
        g.render()
        g.update()
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()
