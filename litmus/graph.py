
#########
# Graph #
#########
class Graph:
    ############
    # __init__ #
    ############
    def __init__(self, adj = None):
        """
        Constructs a directed graph.

        Vertices are dict keys, so any hashable object can be one, and two vertices
        are the same vertex when they compare equal. A vertex type that uses value
        equality will therefore have duplicates silently collapse into a single
        node; types whose duplicates must stay distinct have to keep Python's
        default identity equality.

        Args:
            adj (dict, optional): Adjacency dict of vertex to set of successors.
                Defaults to an empty graph.
        """
        self.adj = adj or {}

    ############
    # __repr__ #
    ############
    def __repr__(self):
        """
        Returns an unambiguous representation, e.g. Graph({'a': {'b'}}).

        This round-trips only when every vertex has an evaluable repr, which is not
        the case for vertex types relying on the default object repr.
        """
        return f"Graph({self.adj})"

    ###########
    # __str__ #
    ###########
    def __str__(self):
        """
        Returns the adjacency dict as a string.
        """
        return f"{self.adj}"

    ############
    # __len__ #
    ############
    def __len__(self):
        """
        Returns the number of vertices.
        """
        return len(self.adj)

    ################
    # __contains__ #
    ################
    def __contains__(self, u):
        """
        Returns True if u is a vertex in the graph.

        Args:
            u: Vertex to check.

        Returns:
            bool: True if u is in the graph.
        """
        if u in self.adj:
            return True
        else:
            return False

    ##############
    # add_vertex #
    ##############
    def add_vertex(self, u):
        """
        Adds a vertex, if it is not already present.

        Adding a vertex that already exists is a no-op and leaves its edges intact.

        Args:
            u: Vertex to add.
        """
        if u not in self.adj:
            self.adj[u] = set()

    #################
    # remove_vertex #
    #################
    def remove_vertex(self, u):
        """
        Removes a vertex and every edge touching it.

        Removing a vertex that is not in the graph is a no-op. Only successors are
        stored, so finding the edges that point at u means scanning every vertex,
        making this O(V) rather than O(degree).

        Args:
            u: Vertex to remove.
        """
        for v in self.adj:
            self.remove_edge(v, u)

        if u in self.adj:
            self.adj.pop(u)

    ############
    # add_edge #
    ############
    def add_edge(self, u, v):
        """
        Adds a directed edge from u to v.

        Both vertices must already exist. Adding an edge does not create them, so
        that a typo becomes an error rather than a stray vertex.

        Args:
            u: Source vertex.
            v: Destination vertex.

        Raises:
            KeyError: If either vertex is not in the graph.
        """
        if u not in self.adj:
            raise KeyError(f"Vertex '{u}' not in graph.")
        if v not in self.adj:
            raise KeyError(f"Vertex '{v}' not in graph.")
        self.adj[u].add(v)

    ###############
    # remove_edge #
    ###############
    def remove_edge(self, u, v):
        """
        Removes the directed edge from u to v.

        Removing an edge that is not there is a no-op, but the source vertex must
        exist.

        Args:
            u: Source vertex.
            v: Destination vertex.

        Raises:
            KeyError: If u is not in the graph.
        """
        if u not in self.adj:
            raise KeyError(f"Vertex '{u}' not in graph.")

        self.adj[u].discard(v)

    ############
    # indegree #
    ############
    def indegree(self, u):
        """
        Returns the number of edges arriving at u.

        Only successors are stored, so this scans every vertex and is O(V), unlike
        outdegree which is a single lookup.

        Args:
            u: Vertex to query.

        Returns:
            int: Number of incoming edges.
        """
        return sum(1 for v in self.adj if u in self.adj[v])

    #############
    # outdegree #
    #############
    def outdegree(self, u):
        """
        Returns the number of edges leaving u.

        Args:
            u: Vertex to query.

        Returns:
            int: Number of outgoing edges.
        """
        return len(self.adj[u])

    ###########
    # is_sink #
    ###########
    def is_sink(self, u):
        """
        Returns True if no edges leave u.

        Args:
            u: Vertex to query.

        Returns:
            bool: True if u is a sink.
        """
        if self.outdegree(u) == 0:
            return True
        else:
            return False

    #############
    # is_source #
    #############
    def is_source(self, u):
        """
        Returns True if no edges arrive at u.

        Args:
            u: Vertex to query.

        Returns:
            bool: True if u is a source.
        """
        if self.indegree(u) == 0:
            return True
        else:
            return False

    #########
    # sinks #
    #########
    def sinks(self):
        """
        Returns every vertex with no outgoing edges.

        Returns:
            set: The sink vertices.
        """
        return {u for u in self.adj if self.is_sink(u)}

    ###########
    # sources #
    ###########
    def sources(self):
        """
        Returns every vertex with no incoming edges.

        This calls indegree once per vertex, so it is O(V^2) where sinks() is O(V).
        Prefer sinks() on a hot path.

        Returns:
            set: The source vertices.
        """
        return {u for u in self.adj if self.is_source(u)}

    #########
    # empty #
    #########
    def empty(self):
        """
        Returns True if the graph has no vertices.
        """
        if self.adj == {}:
            return True
        else:
            return False
