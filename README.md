# Airport Route Management System

A Django-based web application for managing airport routes and finding routes between airports based on travel duration.

## Features

- Add airport routes with airport code, position, duration, and next airport.
- Display airport routes in position order.
- Find the nth airport to the left or right of a selected airport.
- Find the longest route based on duration.
- Find the shortest route between two airports.
- Display the shortest route and its total duration.
- Uses Dijkstra's shortest-path algorithm.
- Provides form validation and error messages.

## Technologies Used

- Python
- Django
- HTML
- CSS
- SQLite
- Dijkstra's Algorithm
- Heap Queue (`heapq`)

## Project Structure

```text
Backend/
│
├── manage.py
│
├── airport_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
└── routes/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── models.py
    ├── views.py
    ├── urls.py
    │
    └── templates/
        └── routes/
            ├── add_route.html
            ├── search_route.html
            ├── longest_route.html
            └── shortest_route.html
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/airport-route-management.git
```

### 2. Open the project directory

```bash
cd airport-route-management
```

### 3. Create a virtual environment

For Windows:

```bash
python -m venv venv
```

For Linux or macOS:

```bash
python3 -m venv venv
```

### 4. Activate the virtual environment

For Windows Command Prompt:

```bash
venv\Scripts\activate
```

For Windows PowerShell:

```bash
venv\Scripts\Activate.ps1
```

For Linux or macOS:

```bash
source venv/bin/activate
```

### 5. Install Django

```bash
pip install django
```

If a `requirements.txt` file is available, install dependencies using:

```bash
pip install -r requirements.txt
```

## Django Configuration

Add the application to `INSTALLED_APPS` in `airport_project/settings.py`:

```python
INSTALLED_APPS = [
    # Default Django applications
    'routes',
]
```

Make sure template discovery is enabled:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Default context processors
            ],
        },
    },
]
```

## Database Setup

Run the migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Create an administrator account if required:

```bash
python manage.py createsuperuser
```

## Run the Application

Start the Django development server:

```bash
python manage.py runserver
```

Open the application in a browser:

```text
http://127.0.0.1:8000/
```

The shortest-route page can be accessed using:

```text
http://127.0.0.1:8000/shortest-route/
```

To run the application on a different host and port:

```bash
python manage.py runserver 0.0.0.0:8080
```

## Application Workflow

### 1. Add an Airport Route

Enter the following details:

- Airport code
- Position
- Duration to the next airport
- Next airport code

The route is saved in the database.

### 2. Search for an Airport

Select an airport code, enter the required position number, and choose:

- Left
- Right

The application displays the airport located at the selected position.

### 3. Find the Longest Route

The application compares the duration of all stored routes and displays the route with the highest duration.

### 4. Find the Shortest Route

Enter the source and destination airport codes. The application:

1. Reads all airport routes from the database.
2. Builds a graph of connected airports.
3. Uses Dijkstra's algorithm.
4. Calculates the shortest total duration.
5. Reconstructs the airport sequence.
6. Displays the shortest route and total duration.

## Example

Assume the following routes are stored:

| Source Airport | Destination Airport | Duration |
|---|---|---:|
| COK | BLR | 60 minutes |
| COK | DEL | 180 minutes |
| BLR | DEL | 120 minutes |
| DEL | BOM | 150 minutes |

For the route from `COK` to `BOM`, the application displays:

```text
COK → BLR → DEL → BOM
```

Total duration:

```text
330 minutes
```

Calculation:

```text
60 + 120 + 150 = 330 minutes
```

## Algorithm Used

The application uses Dijkstra's shortest-path algorithm.

Dijkstra's algorithm is suitable when:

- The graph contains weighted edges.
- Each duration is non-negative.
- The shortest route must be found between two nodes.

In this application:

- Airports are represented as graph nodes.
- Routes are represented as graph edges.
- Route durations are represented as edge weights.

The Python `heapq` module is used as a priority queue to efficiently select the airport with the lowest known duration.

## Important Notes

- Airport codes should be entered consistently, such as `COK`, `BLR`, or `DEL`.
- Airport codes are converted to uppercase before searching.
- Route durations should be non-negative.
- The application displays an error if the source or destination airport does not exist.
- The application displays an error if no route exists between the selected airports.
- The graph currently represents directed routes. A route from airport `A` to airport `B` does not automatically create a route from `B` to `A`.

## Common Errors

### TemplateDoesNotExist

Make sure the template is located at:

```text
routes/templates/routes/shortest_route.html
```

The view should render it using:

```python
return render(
    request,
    'routes/shortest_route.html',
    {
        'form': form,
        'result': result,
        'error': error
    }
)
```

Also verify that `APP_DIRS` is set to `True` in `settings.py`.

### No Route Found

Check the following:

- Both airport codes exist in the database.
- The `next_airport` values are correct.
- The routes are connected in the required direction.
- Route durations are stored as valid numeric values.

## Future Enhancements

- Add authentication and user roles.
- Display routes on an interactive map.
- Add airport and route deletion features.
- Add route-editing functionality.
- Support bidirectional routes.
- Display all possible routes.
- Add route distance and ticket price.
- Add REST API support using Django REST Framework.
- Improve the user interface with Bootstrap.
- Deploy the application on a cloud platform.

## Author

Developed using Python and Django as an airport route management and shortest-path application.

## License

This project is intended for educational and demonstration purposes.
````
