"""
This file contains functions that involving prompting llama3(LLM) 

Functions include:
-creating a workout plan for the week
-altering that plan
-finding past exercises that match a provided exercise
"""
import ollama
from utils.util import get_dates_list
from services.supabase_client import supabase
import pandas as pd
import logging
import textwrap
import json

client = ollama.Client()
model = 'llama3'

logging.basicConfig(level=logging.INFO)

def generate_plan(age, level, gender, goal, dates, equipment_available, startdate):
    """
    Creates csv file containing a workout plan for the week given user inputs

    Args:
        age(str): the age of the user
        level(str): experience level in the gym: beginner, intermediate, expert
        goal(str): focus of the workouts
        dates(list[str]): contains all the days from Monday-Sunday to create a workout for
        equipment_available(list[str]): contains all the gym equipment the user has at their disposal
        startdate(str): the first day('YYYY-MM-DD') of the week workout plan 

    Returns:
        string containing the workout plan in csv format
    """
    dates_list = get_dates_list(startdate, dates)  # list of dates('YYYY-MM-DD') to generate workouts for
    prompt = textwrap.dedent(
        f"""
            You are an expert exercise scientist that creates workout plans. 
            User details:
            - The user is a {age} year old {gender} who is a {level} lifter
            - Their goal is: {goal}
            - They only have access to the following equipment: {equipment_available}
            The output must be in csv format and include the header at the top of the output: title,date,musclegroups,exercise,sets 
            title is the name of the workout, date is when the workout takes place.
            musclegroups must have exactly one muscle trained in the exercise.
            exercise is the name of the exercise. sets is the number of sets the exercise should be performed.
            An example of a row in the csv is: Workout Title,YYYY-MM-DD,musclegroup,exercise,sets.
            Output requirements:
            - Choose exercises for the workouts based on user details
            - Only one workout can be performed each day
            - Each line in the csv represents an exercise in a workout
            - Each date in {dates_list} must have its own workout (required).
            - Each workout must have at least 3 different exercises (required). 
            Do not output any explanation, context, or anything that isn't the csv or header
        """
    )
    try:    
        csv_string = client.generate(model=model, prompt=prompt).response # a string with the csv workout plan
        with open('data/unfiltered_program.csv', 'w') as f:  
            f.write(csv_string)
        logging.info('Workout plan successfully generated and added to csv file!')
        return csv_string
    except Exception as e:
        logging.error(f'Failed to generate a workout plan or write to csv: {e}')
        return None

def find_closest_exercise(exercise):
    """
    Finds the exercise from past workouts that is most similar to the provided exercise

    Args:
        exercise(str): the name of the exercise we want to find closest exercise for

    Returns:
        string containing the most similar past exercise to parameter exercise
    """
    try:
        response = supabase.table('set').select('*').execute()
        if not response.data:
            logging.warning("There are no past exercises in the database")
            raise ValueError("No past exercises available")
        df = pd.DataFrame.from_dict(response.data)
        past_exercises = df['exercise'].drop_duplicates().tolist() #list of unique exercise names
        prompt = textwrap.dedent(
            f"""The list of past exercises is: {past_exercises}.
                Select exactly one exercise from this list that is most comparable to "{exercise}" based only on similarity of typical weight lifted.
                - Ignore muscle groups, movement patterns, or equipment differences.
                - Return only the exercise name, copied exactly from the list.
                - The output must be exactly one of the items from {past_exercises}, with the exact capitalization.
                - Do not add anything else. No commas, quotes, or extra text.
                - Example output: Bench Press
            """
        )
        response = client.generate(model=model, prompt=prompt).response
        logging.info(f'The most similar past exercise: {response}')
        return response
    except Exception as e:
        logging.error(f'Could not find the closest exercise: {e}')
        return None


def alter_program(past_program, changes):
    """
    Alters the generated program with requested changes

    Args:
        past_program(list[dict]): list containing workouts and their info
        changes(str): the changes to be made to the program

    Returns:
        return(list): list containing altered workouts, empty list otherwise
    """
    prompt = textwrap.dedent(
            f"""
                {past_program} is a list where each item represents a workout. The list has the structure:
                [{{
                    date: day the workout took place in the form YYYY-MM-DD,
                    musclegroups:list of muscle groups trained in the workout,
                    sets:{{
                        exercise: name of the exercise performed,
                        set_num: the set number of the exercise ** set_num must be an integer**,
                        lbs:number of lbs lifted for set set_num of the exercise ** lbs must be an integer**,
                        reps:number of repetitions performed in set set_num for the exercise  ** reps must be an integer**
                    }}[],
                    title:name of the workout,
                }},...]
                Perform the changes {changes} on the list.
                Output must only contain {past_program} with the changes applied in valid json format. 
                No explanations, commentary, or extra text. Ensure the output is strictly valid JSON with double quotes only.
            """
        )
    try:
        response = client.generate(model=model, prompt=prompt).response
        first_bracket_index = response.find('[') #index of workout list start
        last_bracket_index = response.rfind(']') #index of workout list end
        just_workout = response[first_bracket_index:last_bracket_index+1] #contains just the workout list as a string
        logging.info(f'The altered program: {just_workout}')
        return json.loads(just_workout)
    except Exception as e:
        logging.error(f'Failed to alter program: {e}')
        return []

def generate_insights(exercise):
    """
    Generates actionable insights for a given exercise

    Args:
        exercise(str)- name of exercise we want insights for
    
    Returns:
        String containing the actionable insights to be displayed
    """
    from processing.workout_processing import get_past_exercise_data
    past_exercise_data = get_past_exercise_data(exercise)
    if past_exercise_data is None:
        return f'Error generating insights for {exercise}'
    prompt = f"""
                You are a professional fitness trainer who is given the past exercise history of a client.
                The client's past exercise history is a list with the following format.
                [
                    {{
                        "date": "YYYY-MM-DD",   # The date that the user performed the exercise
                        "set": [
                            {{
                                "lbs": int or float,        # How many lbs the user lifted for this set
                                "reps": int or float,       # How many repetitions were performed for this set
                                "set_num": int or float     # The set number in the workout on that date
                            }},
                            ...
                        ]  # "set" is a list containing all sets for the exercise on that date
                    }},
                    ...
                ]
                Here is the client's past history: {past_exercise_data}
                1. Analyze trends in the user's lifting numbers across sessions (how has the weight and reps changed?).
                2. Suggest the optimal lbs and reps the user should aim for in their **next session** based on past performance.
                3. Provide actionable advice on how to safely increase lbs and reps over time for {exercise}(progression strategies, tips for improvement, etc.).

                Output format:  
                - Use numbered recommendations (1, 2, 3).  
                - Do not include anything other than the recommendations.  
                - Keep it concise, actionable, and easy to understand.
            """
    try:
        response = client.generate(model=model, prompt=prompt).response
        return response
    except Exception as e:
        logging.error(f'Failed to generate actionable insights: {e}')
        return []
