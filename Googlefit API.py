# Import necessary libraries
import json
import pandas as pd
from datetime import datetime
import requests

# Defining the api urls for steps and calories data
baseurl_steps = 'https://www.googleapis.com/fitness/v1/users/me/dataSources/derived:com.google.step_count.delta:com.google.android.gms:merge_step_deltas/datasets/1532476800000000000-1633345410000000000'
baseurl_calories = 'https://www.googleapis.com/fitness/v1/users/me/dataSources/derived:com.google.calories.expended:com.google.android.gms:merge_calories_expended/datasets/1532476800000000000-1633345410000000000'

# Specify certain parameters needed to retrieve api calls
params = {
    "access_token": "Enter token here",
    "scope": "https://www.googleapis.com/auth/fitness.activity.read",
    "token_type": "Bearer",
    "expires_in": 3599,
    "refresh_token": "Enter refresh token here"
}


# Response function returns a JSON output and writes it to a file
def response(url, filename):
    response = requests.get(url, params=params)
    response_json = response.json()
    open_file = open(filename, 'w')
    open_file.write(json.dumps(response_json, indent=4))
    open_file.close()
    return 'JSON was written to the specified file'


# Writing the json output to a specified file
response(baseurl_steps, 'Steps_googlefit.json')
response(baseurl_calories, 'Calories_googlefit.json')

# Reading the files and loading it as a JSON to query results
data_calorie = open('Calories_googlefit.json').read()
data_steps = open('Steps_googlefit.json').read()
data_weight = open('Body weight user inputted.json').read()
data_height = open('Body height user inputted.json').read()
openjson_calories, openjson_steps, openjson_weight, openjson_height = json.loads(
    data_calorie), json.loads(data_steps), json.loads(data_weight), json.loads(data_height)

# Defining lists for storing the data
list_of_lists_calories = []
list_of_lists_steps = []

# Querying the calorie information
for rows in openjson_calories['point']:
    list_of_indi_calories = []

    def values(tag):
        return rows[tag]

    calories_startime, calories_endtime = values(
        "startTimeNanos"), values("endTimeNanos")
    calories = rows["value"][0]["fpVal"]

    int_starttime_calories, int_endtime_calories = int(
        calories_startime)//1000000000, int(calories_endtime)//1000000000

    starttime_calories = datetime.fromtimestamp(
        int_endtime_calories).strftime('%Y-%m-%d %H:%M:%S')

    endtime_calories = datetime.fromtimestamp(
        int_endtime_calories).strftime('%Y-%m-%d %H:%M:%S')

    # Storing the calories columns in a list
    list_of_indi_calories.append(starttime_calories)
    list_of_indi_calories.append(endtime_calories)
    list_of_indi_calories.append(calories)
    list_of_lists_calories.append(list_of_indi_calories)

# Querying the steps information
for rows_steps in openjson_steps['point']:
    list_of_indi_steps = []

    def values_steps(tag):
        return rows_steps[tag]
    steps_startime, steps_endtime = values_steps(
        "startTimeNanos"), values_steps("endTimeNanos")
    steps = rows_steps["value"][0]["intVal"]
    steps_int_starttime, steps_int_endtime = int(
        steps_startime)//1000000000, int(steps_endtime)//1000000000
    starttime_steps = datetime.fromtimestamp(
        steps_int_starttime).strftime('%Y-%m-%d %H:%M:%S')
    endtime_steps = datetime.fromtimestamp(
        steps_int_endtime).strftime('%Y-%m-%d %H:%M:%S')

    # Storing the steps columns in a list
    list_of_indi_steps.append(starttime_steps)
    list_of_indi_steps.append(endtime_steps)
    list_of_indi_steps.append(steps)
    list_of_lists_steps.append(list_of_indi_steps)


# Converting the lists into pandas dataframe
df_calories = pd.DataFrame(list_of_lists_calories, columns=[
    "starttime_calories", "endtime_calories", "calories"])
df_steps = pd.DataFrame(list_of_lists_steps, columns=[
    "starttime_steps", "endtime_steps", "steps"])

# Storing the dataframe in csv files
df_calories.to_csv('calories.csv')
df_steps.to_csv('steps.csv')
