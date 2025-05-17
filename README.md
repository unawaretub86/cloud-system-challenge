# Task Management Application

A full-stack task management application built with React.js (frontend) and Django (backend).

## Features

- User authentication (register, login, logout)
- Create, read, update, and delete tasks
- Filter tasks by status (all, active, completed)
- Responsive design
- Dockerized for easy deployment

## Tech Stack

### Frontend
- React.js with TypeScript
- React Router for navigation
- Context API for state management
- Axios for API requests
- CSS for styling

### Backend
- Django with Django REST Framework
- PostgreSQL database
- JWT authentication
- Docker for containerization

## Installation and Setup

### Prerequisites
- Docker and Docker Compose
- Make (optional, for simplified commands)
- Git

### Environment Setup

1. Clone the repository
```bash
git clone <repository-url>
cd cloud-system-challenge
```

2. Configure environment variables
   
   The project uses environment variables for configuration. A sample `.env` file is provided below:

```
# Copy this to .env in the root directory
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database settings
DB_ENGINE=django.db.backends.postgresql
DB_NAME=todo_db
DB_USER=root
DB_PASSWORD=qwerty
DB_HOST=db
DB_PORT=5432

# Port settings
FRONTEND_PORT=3000
BACKEND_PORT=8000
POSTGRES_PORT=5432

# Database URL
DATABASE_URL=postgres://root:qwerty@db:5432/todo_db

# CORS settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://frontend:80
CORS_ALLOW_CREDENTIALS=True
```

### Running with Docker

#### Using Make (Recommended)

We've included a Makefile to simplify common operations:

1. Build the containers:
```bash
make build
```

2. Start the application:
```bash
make up
```

3. Run database migrations:
```bash
make migrate
```

4. Create a superuser (optional):
```bash
make superuser
```

5. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/api
   - Admin interface: http://localhost:8000/admin

6. To stop the application:
```bash
make down
```

#### Using Docker Compose Directly

If you don't have Make installed, you can use Docker Compose commands directly:

1. Build and start the application:
```bash
docker compose up --build
```

2. Run database migrations:
```bash
docker compose exec backend python manage.py migrate
```

3. Create a superuser (optional):
```bash
docker compose exec backend python manage.py createsuperuser
```

4. To stop the application:
```bash
docker compose down
```

### Local Development

#### Frontend

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

4. Access the frontend at http://localhost:3000

#### Backend

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Start the development server:
```bash
python manage.py runserver
```

5. Access the API at http://localhost:8000/api

## Available Make Commands

We've included a Makefile with the following commands for easier management:

- `make build` - Build all Docker containers
- `make up` - Start all Docker containers in detached mode
- `make down` - Stop all Docker containers
- `make restart` - Restart all Docker containers
- `make logs` - View logs from all containers
- `make shell` - Open a shell in the backend container
- `make migrate` - Run Django migrations
- `make makemigrations` - Create new Django migrations
- `make superuser` - Create a Django superuser
- `make test` - Run Django tests
- `make clean` - Remove all containers, volumes, and networks

## API Endpoints

### Authentication
- `POST /api/users/register/` - Register a new user
- `POST /api/users/login/` - Login user and get JWT token
- `GET /api/users/profile/` - Get user profile
- `POST /api/users/token/refresh/` - Refresh JWT token

### Tasks
- `GET /api/tasks/` - List all tasks
- `POST /api/tasks/` - Create a new task
- `GET /api/tasks/<id>/` - Retrieve a specific task
- `PUT /api/tasks/<id>/` - Update a task
- `DELETE /api/tasks/<id>/` - Delete a task

## Project Structure

```
cloud-system-challenge/
├── backend/
│   ├── docker/
│   │   ├── Dockerfile
│   │   └── .env
│   └── src/
│       ├── apps/
│       │   ├── tasks/
│       │   └── users/
│       ├── config/
│       ├── domain/
│       └── infrastructure/
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── auth/
│   │   │   └── tasks/
│   │   ├── context/
│   │   ├── services/
│   │   └── types/
│   ├── Dockerfile
│   └── package.json
├── .env
├── docker-compose.yml
├── Makefile
├── manage.py
└── README.md
```

## Troubleshooting

### Database Connection Issues
- Ensure the `DB_HOST` is set to `db` in the Docker environment
- Check that the database service is running with `docker compose ps`
- Verify the database credentials in the `.env` file

### Port Conflicts
- If you have services already using ports 3000, 8000, or 5432, change the port mappings in the `.env` file

### Docker Volume Issues
- If you encounter database compatibility issues, try removing the volumes with `make clean` or `docker compose down -v`

## License

This project is licensed under the MIT License.
