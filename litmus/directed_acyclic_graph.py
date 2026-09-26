###########
# imports #
###########
from litmus.graph import Graph

########################
# DirectedAcyclicGraph #
########################
class DirectedAcyclicGraph(Graph):

    ###############
    # descendants #
    ###############
    def descendants(self, u):
        """
        """
        return self.reachable(u)

    #############
    # ancestors #
    #############
    def ancestors(self, u, visited = None):
        """
        """
        if visited is None:
            visited = set()

        if u not in self.adj_t:
            return visited

        for v in self.adj_t[u]:
            if v not in visited:
                visited.add(v)
                self.ancestors(v, visited = visited)

        return visited

    #########
    # check #
    #########
    def check(self):
        """
        """
        for u in self.vertices():
            if u in self.descendants(u):
                raise ValueError(f"Vertex '{u}' is on a cycle.")

