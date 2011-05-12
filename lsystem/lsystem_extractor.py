#-*- coding: utf-8 -*-

import sys

class LsystemExtractor():
    """
    """

    def __init__(self, fname):
        """
        """

        self.fname = fname

        # Static and simple variable
        self.static_variables = ['name', 'iteration', 'axiom', 'angle', 'ratio']

        # Default parameters
        self.name = ''
        self.axiom = ''
        self.iteration = 3
        self.angle = 90.0
        self.ratio = 1.0
        
        self.rules = {}
        self.symbols = {}
        
        self.define = {}
        self.ignores = []
        
        self.extract()

    def extract(self):
        """
        """

        f = open(self.fname, 'r')

        for line in open(self.fname, 'r'):
            line = line.strip()
            
            if line != '' and line[0] != '#':

                line = line.split(':')
                field = line[0].strip()

                # Get static and simple variable
                if field in self.static_variables:
                    setattr(self, field, line[1].strip())

                # Set some parameters value for parametric l system
                elif field == 'define':
                    key = line[1].strip()
                    value = line[2].strip()
                    self.define[key] = value

                # Set ignore symbols in case of context sensitive l system
                elif field == 'ignore':
                    for s in line[1].strip():
                        self.ignores.append(s)

                # Set symbols correspondance
                elif field == 'symbols':
                    key = line[1].strip()
                    value = line[2].strip()
                    self.symbols[key] = value

                # Set rules
                elif field == 'rules':

                    # Stochastic or context rules
                    if len(line) == 5:
                    
                        self.rules[line[1]] = { 'init' : line[2].strip(),
                                                'p' : line[3].strip(),
                                                'out' : line[4].strip() }

                    # Context rules
                    if len(line) == 4:
                    
                        self.rules[line[1]] = { 'init' : line[2].strip(),
                                                'p' : 1,
                                                'out' : line[3].strip() }

                    # Normal rules
                    elif len(line) == 3:

                        self.rules[line[1]] = { 'init' : line[1].strip(),
                                                'p' : 1,
                                                'out' : line[2].strip() }
