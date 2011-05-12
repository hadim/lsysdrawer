#-*- coding: utf-8 -*-

from lsystem_extractor import *

import random

class Lsystem():
    """
    """

    def __init__(self, grammar_file, n = -1):
        """
        """

        grammar = LsystemExtractor(grammar_file)

        self.name = grammar.name
        self.axiom = grammar.axiom
        self.angle = float(grammar.angle)
        self.ratio = float(grammar.ratio)
        self.iteration = int(grammar.iteration)

        self.rules = grammar.rules
        self.symbols = grammar.symbols
        self.define = grammar.define
        self.ignores = grammar.ignores
        
        self.current_iter = 0

        # Init l-system
        self.current_state = self.axiom

    def __str__(self):
        """
        """

        newline = '\n'

        s = ''
        s += 'Name of the l-system : ' + self.name + newline
        s += 'Angle : ' + str(self.angle) + newline
        s += 'Ratio : ' + str(self.ratio) + newline
        s += 'Number of iterations : ' + str(self.iteration) + newline
        s += 'Axiom : ' + str(self.axiom) + newline
        s += newline

        s += 'Defined parameters : ' + str(self.define) + newline
        s += 'Ignore symbols ( context sensitive l-system ) : ' + str(self.ignores) + newline
        s += newline

        s += 'Alphabet ( with correspondance ): ' + str(self.symbols) + newline
        s += 'Rules are : ' + str(self.rules) + newline

        return s

    def last_state(self):
        """
        """

        for s in self:
            pass

        return s
    
    def __iter__(self):
        """
        """
        
        return self

    def next(self):
        """
        """

        if self.current_iter >= self.iteration:
            self.current_iter = 0
            raise StopIteration

        self.current_iter += 1

        return self.next_step()

    def next_step(self):
        """
        """

        # Calculate next state
        new_state = ''
        i = 0
        for letter in self.current_state:

            new_letters = letter
            
            # Look for rules
            rule = self.get_rule(letter, i)
            i += 1
            
            if rule:
                new_letters = ''.join(rule['out'])

            new_state += new_letters

        state_to_return = self.current_state
        self.current_state = new_state

        return state_to_return

    def get_rule(self, letter, position):
        """
        """

        candidates = {}
        p = 0.0

        for name, rule in self.rules.items():

            # Look if rule is context sensitive
            init = rule['init']

            context = False
            if '<' in init :
                cleanInit = init.strip().split('<')[-1].strip()
                sign = '<'
                toCheck = init.strip().split('<')[0]
                context = True
                
            elif '>' in init :
                cleanInit = init.strip().split('>')[-1].strip()
                sign = '>'
                toCheck = init.strip().split('>')[0]
                context = True
            else:
                cleanInit = init

            contextOk = True
            if context:
                contextOk = self.checkContext(position, sign, toCheck)
                
            if cleanInit == letter and contextOk:
                candidates[name] = (p, float(rule['p']) + p)
                p += float(rule['p'])

        proba = random.random()

        for name in candidates:

            if proba >= candidates[name][0] and proba <= candidates[name][1]:
                return self.rules[name]

        return None

    def get_symbol(self, s):
        """
        """

        if s in self.symbols.keys():
            return self.symbols[s]
        else:
            return s

    def checkContext(self, position, sign, toCheck):
        """
        """

        # Clean state with ignored symbols
        state = []
        i = j = 0
        for l in self.current_state:
            if i == position:
                position = j
            if l not in self.ignores:
                state.append(l)
                j += 1
            i += 1
                
        idx = None
        if position > 0 and position < len(state):
            
            if sign == '<':
                idx = position - 1
            elif sign == '>':
                idx = position + 1
            else:
                idx = 'NO'
           
            # if position:
            #     print '#1'
            #     print 'state: ' + str(state)
            #     print 'position: ' + str(position)
            #     print 'sign: ' + sign
            #     print 'toCheck: ' + toCheck
            #     print 'idx: ' + str(idx)
            #     print 'state[idx]: ' + state[idx]
            #     print
            #     raw_input()

            if idx != 'NO' and idx < len(state) and state[idx].strip() == toCheck.strip():
                # print 'VALID'
                # raw_input()
                return True
            else:
                return False

        else:
            return False

        
