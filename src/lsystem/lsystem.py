#-*- coding: utf-8 -*-

# lsystem.py

# Copyright (c) 2011, see AUTHORS
# All rights reserved.

# This file is part of Lsysdrawer.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:

# Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
# Neither the name of the ProfileExtractor nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#-*- coding: utf-8 -*-

from lsystem_extractor import *

import random, copy

class Lsystem():
    """
    """

    def __init__(self, grammar_file, n = -1):
        """
        """

        grammar = LsystemExtractor(grammar_file)

        self.name = grammar.name
        self.axiom = grammar.axiom
        self.initial_axiom = copy.copy(grammar.axiom)
        self.angle = float(grammar.angle)
        self.ratio = float(grammar.ratio)
        self.iteration = int(grammar.iteration)
        self.width = float(grammar.width)
        self.radius = float(grammar.radius)

        self.rules = grammar.rules
        self.initial_rules = copy.copy(grammar.rules)
        self.symbols = grammar.symbols
        self.define = grammar.define
        self.ignores = grammar.ignores
        self.patterns = grammar.patterns
        
        self.current_iter = 0

        self.replace_defines()
        
        # Init l-system
        self.current_state = self.axiom
        
        # Convert state as a list of dict
        self.state_as_dict = self.getDict(self.current_state)
        print self.axiom

    def __str__(self):
        """
        """

        newline = '\n'

        s = ''
        s += 'Name of the l-system : ' + self.name + newline
        s += 'Angle : ' + str(self.angle) + newline
        s += 'Ratio : ' + str(self.ratio) + newline
        s += 'Number of iterations : ' + str(self.iteration) + newline
        s += 'Axiom : ' + str(self.initial_axiom) + newline
        s += newline

        s += 'Defined parameters : ' + str(self.define) + newline
        s += 'Ignore symbols ( context sensitive l-system ) : ' + str(self.ignores) + newline
        s += newline

        s += 'Alphabet ( with correspondance ): ' + str(self.symbols) + newline
        s += 'Rules are : ' + str(self.initial_rules) + newline

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
        for letter in self.state_as_dict:

            new_letters = letter['raw']
            
            # Look for rules
            rule = self.get_rule(letter, i)
            i += 1
            
            if rule:
                new_letters = rule['out']

            new_state += new_letters

        self.previous_state = self.current_state
        self.previous_state_as_dict = self.state_as_dict
        
        self.current_state = new_state
        self.state_as_dict = self.getDict(new_state)

        return self.previous_state_as_dict

    def get_rule(self, letter, position):
        """
        """

        candidates = {}
        p = 0.0

        # Replace pattern by symbols in rules
        for pattern in self.patterns:
            for r in self.rules:
                
                self.rules[r]['out'] = self.rules[r]['out'].replace("'%s'" % pattern, self.patterns[pattern])
                self.rules[r]['out'] = self.rules[r]['out'].replace("\"%s\"" % pattern, self.patterns[pattern])
                
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
                
            if cleanInit == letter['letter'] and contextOk:
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

    def replace_defines(self):
        """
        Replace defines variables
        """

        # Replace in axiom
        for var in self.define:

            # Replace in axiom
            self.axiom = self.axiom.replace(var, str(self.define[var]))

            # Replace in rules
            for r in self.rules:
                if ('(%s)'%var) in self.rules[r]['out'] \
                    or (',%s)'%var) in self.rules[r]['out'] \
                    or ('(%s,'%var) in self.rules[r]['out']:
                    
                    self.rules[r]['out'] = self.rules[r]['out'].replace(var, str(self.define[var]))

            # Replace in patterns
            for r in self.patterns:
                if ('(%s)'%var) in self.patterns[r] \
                       or (',%s)'%var) in self.patterns[r] \
                       or ('(%s,'%var) in self.patterns[r]:
                    self.patterns[r] = self.patterns[r].replace(var, str(self.define[var]))


    def checkContext(self, position, sign, toCheck):
        """
        """

        # Clean state with ignored symbols
        state = []
        i = j = 0
        for l in self.state_as_dict:
            if i == position:
                position = j
            if l['letter'] not in self.ignores:
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

            if idx != 'NO' and idx < len(state) and state[idx]['letter'] == toCheck.strip():
                return True
            else:
                return False

        else:
            return False

        
    def getDict(self, string):
        """
        """

        state = []
        params = False
        currentParams = ''

        for l in string:
            if l == '(':
                params = True
                
            elif l == ')':
                params = False
                if currentParams:
                    state[-1]['params'] = currentParams.split(',')
                    state[-1]['raw'] += '(' + currentParams.strip()  + ')'
                    currentParams = ''
                    
            elif not params:
                letter = { 'letter' : l,
                           'params' : [],
                           'raw' : l }
                state.append(letter)
                
            elif params:
                currentParams += l

        return state
        
