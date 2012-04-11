#!/usr/bin/python
# -*- coding: utf-8 -*-'''

'''
Created on 2012-02-06

@author: Sebastien Renaud 
'''
import pygame
import random
import sys
import os
import ConfigParser


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

def load_sound(name):
    fullname = os.path.join('data', name)
    return pygame.mixer.Sound(fullname)



import bisect
class wrg(object):
    """weighted random generator returning the index of the next item randomly selected using provided weights"""
    def __init__(self, weights):
        self.totals = []
        running_total = 0

        for w in weights:
            running_total += w
            self.totals.append(running_total)

    def next(self):
        rnd = random.random() * self.totals[-1]
        return bisect.bisect_right(self.totals, rnd)

    def __call__(self):
        return self.next()
    
class Qtable:
    "Table that defines the possible questions with associated answers, difficulty level and user stats"
    def __init__(self, operator, num_first, num_second):
        self.operator = operator
        self.num_first = num_first
        self.num_second = num_second
        self.difficulties = dict()
        self.answers = dict()
        self.user_stats = dict()
        if self.operator == '+':
            for first in range(num_first):
                for second in range(num_second):
                    self.difficulties[(first, second)] = self.get_difficulty(first,second)
                    self.answers[(first, second)] = first + second
                    self.user_stats[(first, second)] = self.get_user_stats(operator,first,second)
        elif self.operator == '*':
            for first in range(num_first):
                for second in range(num_second):
                    self.difficulties[(first, second)] = self.get_difficulty(first,second)
                    self.answers[(first, second)] = first * second
                    self.user_stats[(first, second)] = self.get_user_stats(operator,first,second)
        self.set_weights()

    def get_difficulty(self,first,second):
        minop = min(first,second)
        minop -= minop%2
        diff = int(minop/2 + 1)
        return diff
    
    def get_user_stats(self,operator,first,second):
        return ( 1.0, 0 ) # success_rate, num_tries
    
    def update_user_stats(self,operator,first,second,answer):
        tot_ans_cnt = self.user_stats[(first, second)][1] + 1
        good_ans_cnt = self.user_stats[(first, second)][0]
        bad_ans_cnt = tot_ans_cnt - good_ans_cnt
        if answer == self.answers[(first,second)]:
            # success
            good_ans_cnt += 1 
        else:
            bad_ans_cnt += 1
            
        self.user_stats[(first, second)][1] = tot_ans_cnt
        self.user_stats[(first, second)][0] = good_ans_cnt/tot_ans_cnt
        
    
    def show_diff_table(self):
        for first in range(self.num_first):
            for second in range(self.num_second):
                print '%d ' % self.difficulties[(first, second)],
            print ' ' 
    
    def set_weights(self):
        self.weights = []
        self.wei_idx = []
        for coord, diff in self.difficulties.iteritems():
            self.weights.append(diff + 1 * 1/self.user_stats[coord][0])
            self.wei_idx.append(coord)
        self.wrg = wrg(self.weights)
    
    def select_next(self):
        return self.wei_idx[self.wrg()]
    
    


class Question:
    unknowns=['ANS','FIRST','SECOND','OPERATOR']
    ukn_wght=[   75,     10,      15,         0]
    unkn_wrg = wrg(ukn_wght)
    operators=['+', '-', '*', '/']
    oper_wght=[ 0,  0,  100,   0]
    oper_wrg = wrg(oper_wght)
    add_table = Qtable('+', 9, 12)
    mul_table = Qtable('*', 9, 12)
    
    def __init__(self):
        self.operator = self.operators[self.oper_wrg()]
        self.unknown  = self.unknowns[self.unkn_wrg()]
        
        if self.operator == '+' or self.operator == '-':
            self.inst_table = self.add_table
        elif self.operator == '*' or self.operator == '/':
            self.inst_table = self.mul_table
        
        self.first, self.second = self.inst_table.select_next()
        self.answer = self.inst_table.answers[(self.first, self.second)]
        self.score_value = self.inst_table.difficulties[(self.first, self.second)]
        
        if self.operator == '-' or self.operator == '/':
            temp = self.first
            self.first = self.answer
            self.answer = temp

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
        if self.unknown == 'OPERATOR' and (self.operator == '*' or self.operator == '/'): 
            if self.second == 1 or self.first == 0:
                if user_input == '*' or user_input == '/':
                    return True
                else:
                    return False
        if self.unknown == 'FIRST' and self.operator == '*' and self.second == 0: 
            return True
        if self.unknown == 'SECOND' and self.operator == '*' and self.first == 0: 
            return True
        if self.unknown == 'SECOND' and self.operator == '/' and self.first == 0 and user_input != '0': 
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
        
    def render(self):
        if self.text:
            font = pygame.font.Font(None, self.size)
            text = font.render(self.text,True,self.color)
            fx, fy = font.size(self.text)
            screen.blit(text, [screen_x/2-fx/2,screen_y/2-fy/2])

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
        pygame.mixer.init()
        # Set the height and width of the screen
        self.scr=screen
        self.clk=pygame.time.Clock()
        pygame.display.set_caption("Mathers")
        self.message = u"Bienvenue à Mathers"
        self.qcnt = 0
        self.rightcnt = 0
        self.score = 0
        self.a = None
        self.q = None
        self.message_timeout = 0
        self.user_input = ''
        self.state = WAITING_FOR_INPUT
        self.bravo_snd = load_sound("bravo.wav")
        self.oops_snd = load_sound("oops.wav")
        
    def new_question(self):
        self.q = Question()
        
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
                        self.user_input += keynum[key][event.mod&1]
                if event.key == pygame.K_RETURN or event.key == K_NUMPAD_RETURN: 
                    if self.user_input != '':
                        self.state = ANS_SUBMITTED
                        self.a = self.user_input
                        break
                if event.key == pygame.K_BACKSPACE:
                    # erase last char of user input
                    if len(self.user_input) <= 1:
                        self.user_input = ''
                        self.state = WAITING_FOR_INPUT
                    else:                        
                        self.user_input = self.user_input[:len(self.user_input)-1]
                print event
        
        
    def update(self):
        # empty input queue
        self.process_events()
        if self.state == WAITING_FOR_INPUT:
            self.q.reset_text()
        elif self.state == SOME_INPUT_PRESENT:
            self.q.color = yellow
            self.q.size = 50
            self.q.update(self.user_input)
        elif self.state == ANS_SUBMITTED:
            if self.q.answer_is_valid(self.user_input):
                self.state = ANS_VALID
            else:
                self.state = ANS_WRONG
        elif self.state == ANS_VALID:
            self.q.size = 70
            self.q.color = green
            self.q.update(self.user_input)
            self.timeout = 0
            self.rightcnt+=1
            self.qcnt += 1
            self.score += self.q.score_value
            self.bravo_snd.play()
            self.state = CONGRADULATE
        elif self.state == CONGRADULATE:
            self.timeout += time_chunk
            if self.timeout > message_timeout:
                self.new_question()
                self.user_input = ''
                self.state = WAITING_FOR_INPUT
        elif self.state == ANS_WRONG:
            self.q.color = red
            self.q.update(self.user_input)
            self.timeout = 0
            self.qcnt += 1
            self.oops_snd.play()
            self.state = PUNISH
        elif self.state == PUNISH:
            self.timeout += time_chunk
            if self.timeout > message_timeout:
                self.user_input = ''
                self.state = WAITING_FOR_INPUT
            
    def render(self):
        screen.fill(black)
        if self.message:
            global time_chunk
            font = pygame.font.Font(None, 25)
            text = font.render(self.message,True,red)
            screen.blit(text, [250,350])
            self.message_timeout += time_chunk
            if self.message_timeout > message_timeout:
                self.message = None
                self.message_timeout = 0
        else:
            font = pygame.font.Font(None, 40)
            #text = '%d' % self.rightcnt + ' / ' + '%d' % self.qcnt
            text = '%d' % self.score
            text_surface = font.render(text,True,white)
            fx, fy = font.size(text)
            screen.blit(text_surface, [screen_x-fx-5,5])
        if self.q:
            self.q.render()

screen=0
screen_x = 0 
screen_y = 0
time_chunk = 0
      
def main():
    size=[800,600]
    global screen
    global screen_x, screen_y
    screen=pygame.display.set_mode(size)
    screen_x, screen_y = screen.get_size()
        
    g = Game()
    
    g.render()
    pygame.display.flip()
    waitForPlayerToPressKey()
    screen=pygame.display.set_mode(size)
    screen_x, screen_y = screen.get_size()
    
    g.new_question()

    while g.state!=QUIT:
        global time_chunk
        time_chunk = g.clk.tick(20)
        g.render()
        g.update()
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()
                
if __name__ == '__main__':
    main()
  
