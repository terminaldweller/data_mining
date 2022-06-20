#!/usr/bin/env python3
"""A* algorithm implementation."""
# https://www.simplilearn.com/tutorials/artificial-intelligence-tutorial/a-star-algorithm
# https://www.redblobgames.com/pathfinding/a-star/introduction.html
import typing


# substitution operator
def get_neighbours(
    v: str,
) -> typing.Optional[typing.List[typing.Tuple[str, int]]]:
    """Get neighbour nodes."""
    if v in Graph_nodes:
        return Graph_nodes[v]
    return None


def determine_cost(
    open_set,
    closed_set: typing.Set,
    parents: typing.Dict[str, str],
    n: str,
    g: typing.Dict[str, int],
):
    """The cost function."""
    neighbours = get_neighbours(n)
    if neighbours is not None:
        for (m, weight) in neighbours:
            if m not in open_set and m not in closed_set:
                open_set.add(m)
                parents[m] = n
                g[m] = g[n] + weight
            else:
                if g[m] > g[n] + weight:
                    g[m] = g[n] + weight
                    parents[m] = n

                    if m in closed_set:
                        closed_set.remove(m)
                        open_set.add(m)


# f = g + h
# in our case, weight is g
def a_star_algo(
    start_node, stop_node: str
) -> typing.Optional[typing.List[str]]:
    """A* algorithm implementation."""
    # the list of nodes to be visited
    open_set = set(start_node)
    # set of all of the visited nodes
    closed_set: typing.Set[str] = set()
    g = {}
    parents = {}

    g[start_node] = 0
    parents[start_node] = start_node

    while len(open_set) > 0:
        n: typing.Optional[str] = None

        for v in open_set:
            if n is None or g[v] + heuristic(v) < g[n] + heuristic(n):
                n = v

        if n == stop_node or Graph_nodes[n] is None:
            pass
        else:
            determine_cost(open_set, closed_set, parents, n, g)

        if n is None:
            print("path doesnt exist.")
            return None

        if n == stop_node:
            path: typing.List[str] = []

            while parents[n] != n:
                path.append(n)
                n = parents[n]

            path.append(start_node)

            path.reverse()

            print("path found:", format(path))
            return path

        open_set.remove(n)
        closed_set.add(n)

    print("path does not exist.")
    return None


def heuristic(n: str) -> int:
    """Get the heuristic for a given node."""
    h_dist = {"A": 11, "B": 6, "C": 99, "D": 1, "E": 7, "G": 0}
    return h_dist[n]


Graph_nodes: typing.Dict[
    str, typing.Optional[typing.List[typing.Tuple[str, int]]]
] = {
    "A": [("B", 2), ("E", 3)],
    "B": [("C", 1), ("G", 9)],
    "C": None,
    "E": [("D", 6)],
    "D": [("G", 1)],
}


def main() -> None:
    """Main."""
    a_star_algo("A", "G")


if __name__ == "__main__":
    main()
