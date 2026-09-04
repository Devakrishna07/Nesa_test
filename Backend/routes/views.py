from django.shortcuts import render, redirect
from .forms import AirportRouteForm, SearchRouteForm, ShortestRouteForm
from .models import AirportRoute
import heapq


# Create your views here.


# Add route view
def add_route(request):
    if request.method == 'POST':
        form = AirportRouteForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('add_route')

    else:
        form = AirportRouteForm()

    return render(
        request,
        'routes/add_route.html',
        {'form': form}
    )


# Get route view
def get_route():
    return list(
        AirportRoute.objects.all().order_by('position')
    )


# Find nth left or right route view
def search_route(request):
    result = None
    error = None

    if request.method == 'POST':
        form = SearchRouteForm(request.POST)

        if form.is_valid():
            airport_code = (
                form.cleaned_data['airport_code']
                .strip()
                .upper()
            )

            n = form.cleaned_data['n']
            direction = form.cleaned_data['direction']

            routes = get_route()

            index = next(
                (
                    i
                    for i, route in enumerate(routes)
                    if route.airport_code.upper() == airport_code
                ),
                None
            )

            if index is not None:
                if direction == 'left':
                    target_index = index - n
                else:
                    target_index = index + n

                if 0 <= target_index < len(routes):
                    result = routes[target_index]
                else:
                    error = "No such route exists."

            else:
                error = "Airport code not found."

    else:
        form = SearchRouteForm()

    return render(
        request,
        'routes/search_route.html',
        {
            'form': form,
            'result': result,
            'error': error
        }
    )


# Longest route view
def longest_route(request):
    routes = get_route()

    if not routes:
        return render(
            request,
            'routes/longest_route.html',
            {'error': "No routes available."}
        )

    longest = max(
        routes,
        key=lambda route: route.duration
    )

    return render(
        request,
        'routes/longest_route.html',
        {'longest': longest}
    )


# Build shortest-path graph
def build_graph():
    graph = {}

    routes = get_route()

    for route in routes:
        source = route.airport_code.strip().upper()

        graph.setdefault(source, [])

        if route.next_airport:
            destination = route.next_airport.strip().upper()

            # Ensure the destination also exists as a graph node
            graph.setdefault(destination, [])

            graph[source].append(
                (destination, route.duration)
            )

    return graph


# Dijkstra shortest-path algorithm
def dijkstra(graph, start, end):
    # Priority queue containing:
    # (total duration, airport code)
    queue = [(0, start)]

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

        # Ignore an outdated queue entry
        if current_distance > distances[current_node]:
            continue

        # Stop when the destination is reached
        if current_node == end:
            break

        # Check all neighboring airports
        for neighbor, duration in graph.get(current_node, []):
            new_distance = current_distance + duration

            # Update if a shorter route is found
            if (
                neighbor not in distances
                or new_distance < distances[neighbor]
            ):
                distances[neighbor] = new_distance
                previous_nodes[neighbor] = current_node

                heapq.heappush(
                    queue,
                    (new_distance, neighbor)
                )

    # If the destination cannot be reached
    if end not in distances:
        return None, None

    # Reconstruct the shortest path
    path = []
    current_node = end

    while current_node is not None:
        path.append(current_node)
        current_node = previous_nodes.get(current_node)

    # Reverse the path to get start -> destination
    path.reverse()

    return path, distances[end]


# Shortest route view between two airports
def shortest_route(request):
    result = None
    error = None

    if request.method == 'POST':
        form = ShortestRouteForm(request.POST)

        if form.is_valid():
            source = (
                form.cleaned_data['source']
                .strip()
                .upper()
            )

            destination = (
                form.cleaned_data['destination']
                .strip()
                .upper()
            )

            graph = build_graph()

            if source not in graph:
                error = "Source airport not found."

            elif destination not in graph:
                error = "Destination airport not found."

            elif source == destination:
                result = {
                    'path': [source],
                    'distance': 0
                }

            else:
                path, distance = dijkstra(
                    graph,
                    source,
                    destination
                )

                if path is None:
                    error = (
                        "No path exists between the specified airports."
                    )

                else:
                    result = {
                        'path': path,
                        'distance': distance
                    }

    else:
        form = ShortestRouteForm()

    return render(
        request,
        'routes/shortest_route.html',
        {
            'form': form,
            'result': result,
            'error': error
        }
    )