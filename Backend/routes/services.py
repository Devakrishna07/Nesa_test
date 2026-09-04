import heapq

from .models import AirportRoute


# Get route records
def get_route():
    return list(
        AirportRoute.objects.all().order_by('position')
    )


# Build airport lookup
def build_airport_map():
    airport_map = {}

    routes = get_route()

    for route in routes:
        airport_code = route.airport_code.strip().upper()
        airport_map[airport_code] = route

    return airport_map


# Find nth left or right route using actual tree branches
def search_nth_route(airport_code, n, direction):
    airport_map = build_airport_map()

    current_code = airport_code.strip().upper()

    if current_code not in airport_map:
        return None, "Airport code not found."

    current_route = airport_map[current_code]

    for i in range(n):
        if direction == 'left':
            next_code = current_route.left_airport
        else:
            next_code = current_route.right_airport

        if not next_code:
            return None, "No such route exists."

        next_code = next_code.strip().upper()

        if next_code not in airport_map:
            return None, "No such route exists."

        current_route = airport_map[next_code]

    return current_route, None


# Find longest cumulative route in the binary tree
def longest_route():
    airport_map = build_airport_map()

    if not airport_map:
        return None, "No routes available."

    # Store all child airport codes
    child_codes = set()

    for route in airport_map.values():

        if route.left_airport:
            child_codes.add(
                route.left_airport.strip().upper()
            )

        if route.right_airport:
            child_codes.add(
                route.right_airport.strip().upper()
            )

    # Root airports are airports that are not children
    root_codes = [
        airport_code
        for airport_code in airport_map
        if airport_code not in child_codes
    ]

    # If every airport is part of a cycle,
    # start from every airport instead
    if not root_codes:
        root_codes = list(airport_map.keys())

    longest = None
    longest_distance = 0

    def traverse(airport_code, path, distance, visited):
        nonlocal longest
        nonlocal longest_distance

        # Get current airport
        route = airport_map.get(airport_code)

        if route is None:
            return

        # Prevent circular references
        if airport_code in visited:
            return

        visited = visited | {airport_code}

        # Update longest route
        if distance > longest_distance:
            longest_distance = distance

            longest = {
                'path': path,
                'distance': distance
            }

        # Check left child
        if route.left_airport:
            left_code = route.left_airport.strip().upper()

            if (
                left_code in airport_map
                and left_code not in visited
            ):
                traverse(
                    left_code,
                    path + [left_code],
                    distance + route.duration,
                    visited
                )

        # Check right child
        if route.right_airport:
            right_code = route.right_airport.strip().upper()

            if (
                right_code in airport_map
                and right_code not in visited
            ):
                traverse(
                    right_code,
                    path + [right_code],
                    distance + route.duration,
                    visited
                )

    # Start traversal from every root airport
    for airport_code in root_codes:
        traverse(
            airport_code,
            [airport_code],
            0,
            set()
        )

    return longest, None


# Build shortest-path graph
def build_graph():
    graph = {}

    routes = get_route()

    for route in routes:
        source = route.airport_code.strip().upper()

        graph.setdefault(source, [])

        children = [
            route.left_airport,
            route.right_airport
        ]

        for child in children:

            if child:
                destination = child.strip().upper()

                graph.setdefault(destination, [])

                # Parent to child
                graph[source].append(
                    (destination, route.duration)
                )

                # Child to parent
                graph[destination].append(
                    (source, route.duration)
                )

    return graph


# Dijkstra shortest-path algorithm
def dijkstra(graph, start, end):

    # Priority queue contains:
    # (total duration, airport code)
    queue = [
        (0, start)
    ]

    # Shortest known distance to each airport
    distances = {
        start: 0
    }

    # Previous airport in the shortest route
    previous_nodes = {
        start: None
    }

    while queue:

        current_distance, current_node = heapq.heappop(queue)

        # Ignore outdated queue entries
        if current_distance > distances[current_node]:
            continue

        # Stop when destination is reached
        if current_node == end:
            break

        # Check all neighboring airports
        for neighbor, duration in graph.get(
            current_node,
            []
        ):

            new_distance = (
                current_distance + duration
            )

            # Update if a shorter route is found
            if (
                neighbor not in distances
                or new_distance < distances[neighbor]
            ):

                distances[neighbor] = new_distance

                previous_nodes[neighbor] = current_node

                heapq.heappush(
                    queue,
                    (
                        new_distance,
                        neighbor
                    )
                )

    # If destination cannot be reached
    if end not in distances:
        return None, None

    # Reconstruct shortest path
    path = []

    current_node = end

    while current_node is not None:

        path.append(current_node)

        current_node = previous_nodes.get(
            current_node
        )

    # Reverse path to get source to destination
    path.reverse()

    return path, distances[end]


# Find shortest route between two airports
def shortest_route(source, destination):

    graph = build_graph()

    source = source.strip().upper()
    destination = destination.strip().upper()

    if source not in graph:
        return None, "Source airport not found."

    if destination not in graph:
        return None, "Destination airport not found."

    if source == destination:
        return {
            'path': [source],
            'distance': 0
        }, None

    path, distance = dijkstra(
        graph,
        source,
        destination
    )

    if path is None:
        return None, (
            "No path exists between the specified airports."
        )

    return {
        'path': path,
        'distance': distance
    }, None