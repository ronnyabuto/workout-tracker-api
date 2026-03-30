#!/usr/bin/env python3

from datetime import date
from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():
    # Clear existing data (order matters due to foreign keys)
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    # --- Exercises ---
    push_up = Exercise(name="Push Up", category="strength", equipment_needed=False)
    squat = Exercise(name="Squat", category="strength", equipment_needed=False)
    treadmill = Exercise(name="Treadmill Run", category="cardio", equipment_needed=True)
    plank = Exercise(name="Plank", category="endurance", equipment_needed=False)
    yoga_stretch = Exercise(name="Yoga Stretch", category="flexibility", equipment_needed=False)
    dumbbell_curl = Exercise(name="Dumbbell Curl", category="strength", equipment_needed=True)

    db.session.add_all([push_up, squat, treadmill, plank, yoga_stretch, dumbbell_curl])
    db.session.commit()

    # --- Workouts ---
    workout1 = Workout(
        date=date(2024, 3, 1),
        duration_minutes=45,
        notes="Morning upper body session",
    )
    workout2 = Workout(
        date=date(2024, 3, 3),
        duration_minutes=30,
        notes="Quick cardio before work",
    )
    workout3 = Workout(
        date=date(2024, 3, 5),
        duration_minutes=60,
        notes="Full body strength day",
    )

    db.session.add_all([workout1, workout2, workout3])
    db.session.commit()

    # --- WorkoutExercises ---
    we1 = WorkoutExercise(workout_id=workout1.id, exercise_id=push_up.id, sets=3, reps=15)
    we2 = WorkoutExercise(workout_id=workout1.id, exercise_id=dumbbell_curl.id, sets=3, reps=12)
    we3 = WorkoutExercise(workout_id=workout1.id, exercise_id=plank.id, sets=3, duration_seconds=60)
    we4 = WorkoutExercise(workout_id=workout2.id, exercise_id=treadmill.id, duration_seconds=1800)
    we5 = WorkoutExercise(workout_id=workout3.id, exercise_id=squat.id, sets=4, reps=10)
    we6 = WorkoutExercise(workout_id=workout3.id, exercise_id=push_up.id, sets=3, reps=20)
    we7 = WorkoutExercise(workout_id=workout3.id, exercise_id=yoga_stretch.id, duration_seconds=300)

    db.session.add_all([we1, we2, we3, we4, we5, we6, we7])
    db.session.commit()

    print("Database seeded successfully!")
    print(f"  Exercises: {Exercise.query.count()}")
    print(f"  Workouts:  {Workout.query.count()}")
    print(f"  WorkoutExercises: {WorkoutExercise.query.count()}")
