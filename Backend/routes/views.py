from django.shortcuts import render, redirect
from .forms import AirportRouteForm, SearchRouteForm, ShortestRouteForm
from .services import (
    search_nth_route,
    longest_route,
    shortest_route
)


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

            result, error = search_nth_route(
                airport_code,
                n,
                direction
            )

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
def longest_route_view(request):
    result, error = longest_route()

    return render(
        request,
        'routes/longest_route.html',
        {
            'longest': result,
            'error': error
        }
    )


# Shortest route view between two airports
def shortest_route_view(request):
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

            result, error = shortest_route(
                source,
                destination
            )

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