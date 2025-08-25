"""
This file contains general utility functions
"""
from datetime import datetime, timedelta
import logging
import csv

DAYS_IN_WEEK = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")

def get_dates_list(date_string, valid_dates):
    """
    Gets list of dates to generate workouts for.

    Args:
        date_string(str): the start of the week's workout plan(YYYY-MM-DD)
        valid_dates(list[str]): list of days(Monday-Sunday) to generate a workout for

    Returns:
        List of dates(YYYY-MM-DD) within the next 7 days to generate workouts for  
    """
    dates_list = []  #holds the dates to create workouts for

    try:
        date = datetime.strptime(date_string, "%Y-%m-%d").date()  #convert 'YYYY-MM-DD' to date object 
    except Exception as e:
        logging.error(f'Could not convert date string into date object: {e}')
        return dates_list

    for i in range(7): 
        date_val = date + timedelta(days=i)
        day_name = DAYS_IN_WEEK[date_val.weekday()]
        if day_name in valid_dates:
            dates_list.append(date_val.isoformat())
    return dates_list

def list_from_csv():
    """
    Gets a list of exercises from unfiltered_program.csv

    Returns:
        List of rows from unfiltered_program.csv that are exercises 
    """
    filtered_rows = []
    try:
        with open('data/unfiltered_program.csv',newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) != 5 or row == ['title', 'date', 'musclegroups', 'exercise', 'sets']: 
                    #Skips rows that don't represent exercises
                    continue
                filtered_rows.append(row)
        logging.info('Successfully loaded plan into csv')
    except Exception as e:
        logging.error(f'Failed to read unfiltered_program.csv:{e}')
    return filtered_rows