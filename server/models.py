from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

VALID_CATEGORIES = ["strength", "cardio", "flexibility", "balance", "endurance"]


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all, delete-orphan",
        overlaps="workouts",
    )
    workouts = db.relationship(
        "Workout",
        secondary="workout_exercises",
        back_populates="exercises",
        overlaps="workout_exercises",
    )

    @validates("name")
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Exercise name cannot be empty.")
        if len(value.strip()) < 2:
            raise ValueError("Exercise name must be at least 2 characters.")
        return value.strip()

    @validates("category")
    def validate_category(self, key, value):
        if value not in VALID_CATEGORIES:
            raise ValueError(
                f"Category must be one of: {', '.join(VALID_CATEGORIES)}."
            )
        return value

    def __repr__(self):
        return f"<Exercise id={self.id} name={self.name} category={self.category}>"


class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan",
        overlaps="exercises,workouts",
    )
    exercises = db.relationship(
        "Exercise",
        secondary="workout_exercises",
        back_populates="workouts",
        overlaps="workout_exercises",
    )

    @validates("duration_minutes")
    def validate_duration(self, key, value):
        if value is None or value <= 0:
            raise ValueError("Duration must be a positive integer.")
        if value > 600:
            raise ValueError("Duration cannot exceed 600 minutes.")
        return value

    def __repr__(self):
        return f"<Workout id={self.id} date={self.date} duration={self.duration_minutes}min>"


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(
        db.Integer, db.ForeignKey("workouts.id"), nullable=False
    )
    exercise_id = db.Column(
        db.Integer, db.ForeignKey("exercises.id"), nullable=False
    )
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    __table_args__ = (
        db.UniqueConstraint("workout_id", "exercise_id", name="uq_workout_exercise"),
    )

    workout = db.relationship(
        "Workout",
        back_populates="workout_exercises",
        overlaps="exercises,workouts",
    )
    exercise = db.relationship(
        "Exercise",
        back_populates="workout_exercises",
        overlaps="exercises,workouts",
    )

    @validates("sets")
    def validate_sets(self, key, value):
        if value is not None and value <= 0:
            raise ValueError("Sets must be a positive integer.")
        return value

    @validates("reps")
    def validate_reps(self, key, value):
        if value is not None and value <= 0:
            raise ValueError("Reps must be a positive integer.")
        return value

    @validates("duration_seconds")
    def validate_duration_seconds(self, key, value):
        if value is not None and value <= 0:
            raise ValueError("Duration (seconds) must be a positive integer.")
        return value

    def __repr__(self):
        return (
            f"<WorkoutExercise workout_id={self.workout_id} "
            f"exercise_id={self.exercise_id}>"
        )
