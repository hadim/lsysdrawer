#-*- coding: utf-8 -*-

try:
    from pygraphml.GraphMLParser import *
    from pygraphml.Graph import *
    from pygraphml.Node import *
    from pygraphml.Edge import *
except ImportError:
    raise ImportError("Error: pygraphml module is needed. Get it at http://github.com/hadim/pygraphml")

class GraphMLExporter():
    """
    """

    def __init__(self, lines):
        """
        """

        self.lines = lines
        self.graph = Graph()

        self.createGraph()

    def createGraph(self):
        """
        """

        i = 0
        mul = 100

        for line in self.lines:
            n1 = self.graph.add_node(str(i))
            n2 = self.graph.add_node(str(i+1))
            i += 1

            n1['x'] = line.p1.x * mul
            n1['y'] = line.p1.y * mul
            n1['z'] = line.p1.z * mul

            n2['x'] = line.p2.x * mul
            n2['y'] = line.p2.y * mul
            n2['z'] = line.p2.z * mul

            self.graph.add_edge(n1, n2)

    def write(self, ):
        """
        """

        parser = GraphMLParser()
        parser.write(self.graph, "test.graphml")
