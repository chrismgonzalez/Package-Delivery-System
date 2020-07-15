from hash_table import HashTable

# this class constructs a vertex, which will be each location that packages
# will be delivered to.  Locations are stored in a Hash table
class Vertex(object):
    def __init__(self, location):
        self.edges = HashTable()
        self.location = location

    # this method adds an edge (distance from vertex to vertex)
    # time complexity: O(n)
    def add_new_edge(self, edge):
        self.edges.insert(edge.identifier, edge)

    # find the edge from the edge id
    # time complexity: O(n)
    def find_edge(self, edge_id):
        return self.edges.find(edge_id)

    # find the distance to the nearest neighbor vertex
    # time complexity: O(n)
    def distance_to_next(self, location):
        return self.edges.find(location.identifier).weight
