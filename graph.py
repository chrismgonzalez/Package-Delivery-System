from hash_table import HashTable
from graph_vertex import Vertex
from graph_edge import Edge


class Graph(object):
    def __init__(self):
        self.vertices = HashTable(20)

    # this method creates a vertex from a location given as an argument
    # it then adds the location as a vertex in the vertices hashtable
    # time complexity: O(n)
    def add_vertex(self, location):
        self.vertices.insert(location.identifier, Vertex(location))

    # this method adds a weighted edge, which is the distance between the origin location
    # and arrival location.  The weighted edge can be traversed both ways, it is undirected
    # time complexity: 0(n)
    def add_weighted_edge(self, origin, destination, weight):
        self.vertices.find(origin.identifier).add_new_edge(Edge(destination, weight))
        self.vertices.find(destination.identifier).add_new_edge(Edge(origin, weight))

    # this method finds the vertex of the location passed in as an argument
    # time complexity: 0(n)
    def find_vertex(self, location):
        return self.vertices.find(location.identifier)

    # this method finds the distance between two given vertices
    # time complexity: O(n)
    def distance_between_vertices(self, origin, target):
        return self.vertices.find(origin.identifier).distance_to_next_location(target)

    # similar to the above method, this one finds the distance between a location
    # and where the package needs to arrive
    def distance_to_delivery(self, location):
        def distance_to_next_location(package):
            return self.vertices.find(location.identifier).distance_to_next_location(package.destination)

        return distance_to_next_location

    # this method is used when finding the next closest location to which the truck should travel
    def distance_from_location(self, origin):
        def distance_to_next_location(destination):
            return self.vertices.find(origin.identifier).distance_to_next_location(destination)

        return distance_to_next_location



