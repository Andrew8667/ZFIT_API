"""
This file contains Flask API endpoints
"""
from flask import Flask, request
from flask_cors import CORS
from services.ollama_service import generate_plan,alter_program
from processing.workout_processing import clean_csv,structure_csv,insert_workouts
from services.supabase_client import supabase
import logging

app = Flask(__name__)
CORS(app)

@app.route("/generateProgram",methods=['POST'])
def generate_program():
    """
    Generates a workout plan for the week based on user details and sends it to the front end

    Returns:
        List containing a structured workout plan to be displayed in the front end
    """
    try:
        data = request.get_json() #data contains user information
        age = data['age']
        gender = data['gender']
        level = data['level']
        goal = data['goal']
        days = data['days']
        startdate = data['startdate'].split('T')[0]
        equipment = data['equipment']
    except Exception as e:
        logging.error(f'Issue extracting user data:{e}')
        return []
    generate_plan(age, level, gender, goal, days, equipment, startdate) #generates plan into unfiltered_program.csv
    clean_csv() #processes unfiltered_program.csv info into filtered_program.csv
    return structure_csv() #structures workout program for front end to process

@app.route("/updateProgram",methods=['POST'])
def update_program():
    """
    Alters original program based on user changes

    returns:
        New program with changes made by the user
    """
    try:
        data = request.get_json()
        original_program = data[0]
        changes = data[1]
        return alter_program(original_program,changes)
    except Exception as e:
        logging.error(f'Could not alter program:{e}')
        return []

@app.route("/insertProgram",methods=['POST'])
def insert_program():
    """
    Inserts the workouts and sets of the customized program into the database

    returns:
        Confirmation that the function has been executed
    """
    data = request.get_json()
    insert_workouts(data)
    return 'Insert Program Executed'

@app.route("/getInsights/<name>",methods=['GET'])
def get_exercise_insights(name):
    """
    Generates actionable insights based on the workout history for an exercise

    Args:
        name(str)-name of exercise we want insights for

    Returns:
        Actionable insights for the exercise to be displayed in the front end
    """
    from services.ollama_service import generate_insights
    insights = generate_insights(name)
    return insights

if __name__ == "__main__":
    """
    Executes when app.py is ran
    """
    app.run(debug=True)