# Workout Tracker API

A RESTful backend API for a personal trainer workout tracking application. Built with Flask, SQLAlchemy, and Marshmallow, the API manages workouts and reusable exercises, connecting them through a join table that stores per-session details such as sets, reps, and duration.

---

## Installation

1. **Clone the repository and navigate into the project folder:**
   ```bash
   git clone <repo-url>
   cd workout-tracker-api
   ```

2. **Install dependencies with Pipenv:**
   ```bash
   pipenv install
   pipenv shell
   ```

3. **Navigate to the server directory:**
   ```bash
   cd server
   ```

4. **Apply the database migrations to create all tables:**
   ```bash
   flask db upgrade
   ```

5. **Seed the database with example data:**
   ```bash
   python seed.py
   ```

---

## Running the Application

```bash
cd server
flask run --port 5555
```

The API will be available at `http://127.0.0.1:5555`.

---

## API Endpoints

### Exercises

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/exercises` | List all exercises |
| `GET` | `/exercises/<id>` | Get a single exercise with its associated workouts |
| `POST` | `/exercises` | Create a new exercise |
| `DELETE` | `/exercises/<id>` | Delete an exercise (cascades to WorkoutExercises) |

**POST /exercises — request body:**
```json
{
  "name": "Push Up",
  "category": "strength",
  "equipment_needed": false
}
```
Valid categories: `strength`, `cardio`, `flexibility`, `balance`, `endurance`.

---

### Workouts

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/workouts` | List all workouts |
| `GET` | `/workouts/<id>` | Get a single workout with its exercises and sets/reps/duration data |
| `POST` | `/workouts` | Create a new workout |
| `DELETE` | `/workouts/<id>` | Delete a workout (cascades to WorkoutExercises) |

**POST /workouts — request body:**
```json
{
  "date": "2024-03-10",
  "duration_minutes": 45,
  "notes": "Optional session notes"
}
```

---

### WorkoutExercises

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout with optional reps/sets/duration |

**POST request body (all fields optional):**
```json
{
  "sets": 3,
  "reps": 12,
  "duration_seconds": 60
}
```

---

## Data Validations

**Table constraints:** `name` on exercises is unique and non-null; `duration_minutes` and `date` on workouts are non-null; `workout_id`/`exercise_id` on workout_exercises are non-null; a `UniqueConstraint` prevents adding the same exercise to the same workout twice.

**Model validations:** exercise `name` must be at least 2 characters; `category` must be one of the valid options; workout `duration_minutes` must be between 1 and 600; `sets`, `reps`, and `duration_seconds` must be positive when provided.

**Schema validations:** mirror the above constraints and are applied before any data reaches the database, returning descriptive 422 error responses on failure.
