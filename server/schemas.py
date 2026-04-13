from marshmallow import Schema, fields, validate, validates, ValidationError
from models import VALID_CATEGORIES


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    reps = fields.Int(load_default=None)
    sets = fields.Int(load_default=None)
    duration_seconds = fields.Int(load_default=None)

    exercise = fields.Nested(lambda: ExerciseSchema(only=("id", "name", "category")), dump_only=True)

    @validates("sets")
    def validate_sets(self, value):
        if value is not None and value <= 0:
            raise ValidationError("Sets must be a positive integer.")

    @validates("reps")
    def validate_reps(self, value):
        if value is not None and value <= 0:
            raise ValidationError("Reps must be a positive integer.")

    @validates("duration_seconds")
    def validate_duration_seconds(self, value):
        if value is not None and value <= 0:
            raise ValidationError("Duration in seconds must be a positive integer.")


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    category = fields.Str(required=True)
    equipment_needed = fields.Bool(load_default=False)

    workouts = fields.Nested(
        lambda: WorkoutSchema(only=("id", "date", "duration_minutes", "notes")),
        many=True,
        dump_only=True,
    )

    @validates("name")
    def validate_name(self, value):
        if not value or not value.strip():
            raise ValidationError("Exercise name cannot be empty.")

    @validates("category")
    def validate_category(self, value):
        if value not in VALID_CATEGORIES:
            raise ValidationError(
                f"Category must be one of: {', '.join(VALID_CATEGORIES)}."
            )


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1, max=600))
    notes = fields.Str(load_default=None)

    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True, dump_only=True)


exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True, exclude=("workouts",))

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True, exclude=("workout_exercises",))

workout_exercise_schema = WorkoutExerciseSchema()
