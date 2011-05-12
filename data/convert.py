import os

for f in os.listdir('./'):

    if f.split('.')[-1] == 'ls':

        g = open('../data_new/' + f, 'w')
        ff = open('./' + f, 'r')

        for line in ff:

            line = line.strip()

            if line != '':

                line = line.replace('"', '')
                line = line.replace(',', '')

                g.write(line + '\n')

