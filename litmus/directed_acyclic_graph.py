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
        Returns every vertex reachable by following edges forward.

        Args:
            u (hashable): The vertex to walk from.

        Returns:
            set: Every descendant of u, which excludes u unless it sits on a cycle.
        """
        return self.reachable(u)

    #############
    # ancestors #
    #############
    def ancestors(self, u, visited = None):
        """
        Returns every vertex reachable by following edges backward.

        Args:
            u (hashable): The vertex to walk from.
            visited (set): Vertices already seen, carried through the recursion.

        Returns:
            set: Every ancestor of u, which excludes u unless it sits on a cycle.
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
        Checks that the graph is acyclic, raising if any vertex is on a cycle.
        """
        for u in self.vertices():
            if u in self.descendants(u):
                raise ValueError(f"Vertex '{u}' is on a cycle.")

