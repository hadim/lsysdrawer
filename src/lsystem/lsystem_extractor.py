#-*- coding: utf-8 -*-

# lsystem_extractor.py

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

import sys

class LsystemExtractor():
    """
    """

    def __init__(self, fname):
        """
        """

        self.fname = fname

        # Static and simple variable
        self.static_variables = ['name', 'iteration', 'axiom', 'angle',
                                 'ratio', 'radius', 'width']

        # Default parameters
        self.name = ''
        self.axiom = ''
        self.iteration = 3
        self.angle = 90.0
        self.ratio = 1.0
        self.width = 1
        self.radius = 0.05
        
        self.rules = {}
        self.symbols = {}
        self.patterns = {}
        
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

                # Set patterns
                elif field == 'patterns':
                    key = line[1].strip()
                    value = line[2].strip()
                    self.patterns[key] = value

                # Set rules
                elif field == 'rules':

                    # Stochastic or context rules
                    if len(line) == 5:
                    
                        self.rules[line[1]] = { 'init' : line[2].strip(),
                                                'p' : line[3].strip(),
                                                'out' : line[4].strip().replace(' ', '') }

                    # Context rules
                    if len(line) == 4:
                    
                        self.rules[line[1]] = { 'init' : line[2].strip(),
                                                'p' : 1,
                                                'out' : line[3].strip().replace(' ', '') }

                    # Normal rules
                    elif len(line) == 3:

                        self.rules[line[1]] = { 'init' : line[1].strip(),
                                                'p' : 1,
                                                'out' : line[2].strip().replace(' ', '') }
