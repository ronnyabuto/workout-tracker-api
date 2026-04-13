from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from models import db, Exercise, Workout, WorkoutExercise
from schemas import (
    exercise_schema,
    exercises_schema,
    workout_schema,
    workouts_schema,
    workout_exercise_schema,
)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()
    return make_response(jsonify(exercises_schema.dump(exercises)), 200)


@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return make_response(jsonify({"error": "Exercise not found."}), 404)
    return make_response(jsonify(exercise_schema.dump(exercise)), 200)


@app.route("/exercises", methods=["POST"])
def create_exercise():
    data = request.get_json()
    try:
        validated = exercise_schema.load(data)
    except ValidationError as err:
        return make_response(jsonify({"errors": err.messages}), 422)

    try:
        exercise = Exercise(**validated)
        db.session.add(exercise)
        db.session.commit()
    except ValueError as err:
        db.session.rollback()
        return make_response(jsonify({"error": str(err)}), 422)
    except IntegrityError:
        db.session.rollback()
        return make_response(jsonify({"error": "An exercise with that name already exists."}), 422)

    return make_response(jsonify(exercise_schema.dump(exercise)), 201)


@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return make_response(jsonify({"error": "Exercise not found."}), 404)

    db.session.delete(exercise)
    db.session.commit()
    return make_response(jsonify({"message": "Exercise deleted successfully."}), 200)


@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    return make_response(jsonify(workouts_schema.dump(workouts)), 200)


@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return make_response(jsonify({"error": "Workout not found."}), 404)
    return make_response(jsonify(workout_schema.dump(workout)), 200)


@app.route("/workouts", methods=["POST"])
def create_workout():
    data = request.get_json()
    try:
        validated = workout_schema.load(data)
    except ValidationError as err:
        return make_response(jsonify({"errors": err.messages}), 422)

    try:
        workout = Workout(**validated)
        db.session.add(workout)
        db.session.commit()
    except ValueError as err:
        db.session.rollback()
        return make_response(jsonify({"error": str(err)}), 422)

    return make_response(jsonify(workout_schema.dump(workout)), 201)


@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return make_response(jsonify({"error": "Workout not found."}), 404)

    db.session.delete(workout)
    db.session.commit()
    return make_response(jsonify({"message": "Workout deleted successfully."}), 200)


@app.route(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",
    methods=["POST"],
)
def create_workout_exercise(workout_id, exercise_id):
    workout = Workout.query.get(workout_id)
    if not workout:
        return make_response(jsonify({"error": "Workout not found."}), 404)

    exercise = Exercise.query.get(exercise_id)
    if not exercise:
        return make_response(jsonify({"error": "Exercise not found."}), 404)

    data = request.get_json() or {}
    try:
        validated = workout_exercise_schema.load(data)
    except ValidationError as err:
        return make_response(jsonify({"errors": err.messages}), 422)

    try:
        workout_exercise = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            reps=validated.get("reps"),
            sets=validated.get("sets"),
            duration_seconds=validated.get("duration_seconds"),
        )
        db.session.add(workout_exercise)
        db.session.commit()
    except ValueError as err:
        db.session.rollback()
        return make_response(jsonify({"error": str(err)}), 422)
    except IntegrityError:
        db.session.rollback()
        return make_response(
            jsonify({"error": "This exercise is already added to the workout."}), 422
        )

    return make_response(jsonify(workout_exercise_schema.dump(workout_exercise)), 201)


if __name__ == "__main__":
    app.run(port=5555, debug=True)
