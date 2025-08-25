"""
This file focuses on processing data related to workouts and sets
"""
import pandas as pd
from services.supabase_client import supabase
from utils.util import list_from_csv
import csv
import logging
from datetime import date

def find_exercise_lbs_reps(exercise):
    """
    Finds the user's highest volume set for the provided exercise

    Args:
        exercise(str): the name of the exercise we are examining

    Returns:
        best_set(dict): the best lbs and reps for a given exercise
    """
    best_set = {'lbs':0,'reps':0} #default lbs and reps
    try:
        response = supabase.table('set').select('lbs','reps').eq("exercise",exercise.title()).execute()
        if not response.data:
            logging.warning('There are no past sets of that exercise')
        else:
            for workout_set in response.data:
                if not isinstance(workout_set['lbs'],(int,float)) or not isinstance(workout_set['reps'],(int,float)):
                    logging.warning(f"Skipping invalid set: {workout_set}")
                    continue
                if workout_set['lbs']*workout_set['reps'] > best_set['lbs']*best_set['reps']:
                    best_set = workout_set
                elif workout_set['lbs']*workout_set['reps'] == 0 and best_set['lbs']*best_set['reps'] == 0:
                    best_set = workout_set
    except Exception as e:
        logging.error(f'Failed to find lbs and reps for that exercise: {e}')
    return best_set

def clean_csv():
    """
    Cleans the workout plan in unfiltered_program.csv and writes it to filtered_program.csv 
    """
    from services.ollama_service import find_closest_exercise
    filtered_rows = list_from_csv() #list of exercises in the plan
    closest_exercise_dict = {} #contains an exercise along with its closest exercise from past workouts and best lbs and reps
    new_rows = [['title', 'date', 'musclegroups', 'exercise', 'set_num','lbs','reps']] #Contains only header for now
    for row in filtered_rows:
        exercise = row[3]
        if exercise not in closest_exercise_dict.keys():
            closest_exercise = find_closest_exercise(exercise)
            if closest_exercise is None:
                logging.warning(f'Could not find closest exercise for {exercise}')
                closest_exercise_dict[exercise] = {
                    'closest_exercise':'',
                    'lbs_reps':{'lbs':0,'reps':0}
                }
            else:
                closest_exercise_dict[exercise] = {
                    'closest_exercise':closest_exercise,
                    'lbs_reps':find_exercise_lbs_reps(closest_exercise)
                }
        try:
            num_sets = int(row[4])#number of sets to perform of exercise
        except Exception as e:
            logging.error(f'Could not cast {row[4]} as an int:{e}')
            num_sets = 3 # default number of sets to 3
        for i in range(num_sets):
            new_rows.append([row[0],row[1],row[2],row[3],i+1,closest_exercise_dict[exercise]['lbs_reps']['lbs'],closest_exercise_dict[exercise]['lbs_reps']['reps']])
    try:
        with open('data/filtered_program.csv','w',newline='') as f:
            writer = csv.writer(f)
            writer.writerows(new_rows)
            logging.info('Filtered workout plan successfully written to filtered_program.csv')
    except Exception as e:
        logging.error(f'Failed to write workout plan to filtered_program.csv')

def structure_csv():
    """
    Structures filtered_program.csv in a way that can be easily parsed for display in the front end

    returns:
        Python dictionary containing workout information
    """
    try:
        df = pd.read_csv('filtered_program.csv')
    except Exception as e:
        logging.error(f'Failed to create dataframe from filtered_program.csv: {e}')
        return []

    workouts = []
    grouped_by_date = df.groupby(['date'])
    for date,data in grouped_by_date:
        workout = {
            'title':set(),
            'date':date,
            'musclegroups': set(),
            'sets':[]
        }
        for index,row in data.iterrows():
            workout['title'].add(row['title'])
            workout['musclegroups'].update(row['musclegroups'].split(';'))
            workout['sets'].append({
                'exercise':row['exercise'],
                'set_num':row['set_num'],
                'lbs':row['lbs'],
                'reps':row['reps']})
        workout['musclegroups'] = list(workout['musclegroups'])
        workout['title'] = '/'.join(list(workout['title']))
        workouts.append(workout)
    return workouts

def insert_workouts(data):
    """
    Inserts workouts into the database after user confirmation

    Args:
        data(list): list of workouts
    """
    for workout in data:
        workout_to_insert = {
            "title":workout['title'],
            "inprogress":True,
            "date":workout['date'],
            "musclegroups":', '.join(workout['musclegroups']),
            "duration":0
        }
        try:
            workout_response = supabase.table('workout').insert(workout_to_insert).execute()
            logging.info(f'Workout inserted: {workout_response}')
        except Exception as e:
            logging.error(f'Failed to insert workout: {workout_to_insert}. Error: {e}')
        for set in workout['sets']:
            set_to_insert = {
                "id":workout_response.data[0]['id'],
                "exercise":set['exercise'],
                "set_num":set['set_num'],
                "lbs":set['lbs'],
                "reps":set['reps']
            }
            try:
                response = supabase.table('set').insert(set_to_insert).execute()
                logging.info(f'Set inserted: {response}')
            except Exception as e:
                logging.error(f'Failed to insert set: {set_to_insert}. Error: {e}')

def get_past_exercise_data(exercise):
    """
    Retrieves set, lbs, and reps information for the provided exercise in the past 10 workouts 

    Args:
        exercise(str): exercise we want to find past info for
    
    returns:
        a list containing the past information for the exercise, none otherwise
    """
    today_iso = date.today().isoformat()
    try:
        response = supabase.table('workout').select('date,set(set_num,lbs,reps)').eq('set.exercise',exercise).lt('date',today_iso).order('date',desc=True).execute()
        filtered_workouts = list(filter(lambda workout:len(workout['set']) != 0,response.data))[0:10]
        logging.info(f'Successfully found past exercise info: {filtered_workouts}')
        return filtered_workouts
    except Exception as e:
        logging.error(f'Could not retrieve past exercise info: {e}')
        return None
