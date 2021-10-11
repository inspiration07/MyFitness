import json
import pandas as pd
from datetime import datetime
import requests

baseurl_steps = 'https://www.googleapis.com/fitness/v1/users/me/dataSources/derived:com.google.step_count.delta:com.google.android.gms:merge_step_deltas/datasets/1532476800000000000-1633345410000000000'
baseurl_calories = 'https://www.googleapis.com/fitness/v1/users/me/dataSources/derived:com.google.calories.expended:com.google.android.gms:merge_calories_expended/datasets/1532476800000000000-1633345410000000000'
params = {
    "access_token": "ya29.a0ARrdaM-z_fawN70pLinOpEFGMHJ9ii0-7J3RjfuXT2m4V9HLqqv20K8vfl6cGAT_4dGAmrJ34-yq1o1kGSTHbW9iKurcTmGtPSpoxbXCNy7nE_ZURZZCS68ZF98ZqtBmaeQqwJBt8Uqz8clTqnFs3e6e3NNY",
    "scope": "https://www.googleapis.com/auth/fitness.activity.read",
    "token_type": "Bearer",
    "expires_in": 3599,
    "refresh_token": "1//04DzqSi4pWWfdCgYIARAAGAQSNwF-L9Irr8UI2OwUYr9EYa0XZn2heOmPAHxjzAsKBKDhh1Sg_hST7BAw4nG3wV3WjC2Gopo7AMo"
}


def response(url, filename):
    response = requests.get(url, params=params)
    response_json = response.json()
    open_file = open(filename, 'w')
    open_file.write(json.dumps(response_json, indent=4))
    open_file.close()
    return 'JSON was written to the specified file'

#response(baseurl_steps, 'Steps_googlefit.json')
#response(baseurl_calories, 'Calories_googlefit.json')


# Gettting the calorie data
data_calorie = open('Calories_googlefit.json').read()
data_steps = open('Steps_googlefit.json').read()
data_weight = open('Body weight user inputted.json').read()
data_height = open('Body height user inputted.json').read()
openjson_calories, openjson_steps, openjson_weight, openjson_height = json.loads(
    data_calorie), json.loads(data_steps), json.loads(data_weight), json.loads(data_height)
list_of_lists_calories = []
list_of_lists_steps = []
list_of_lists_weight = []
list_of_lists_height = []
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
    list_of_indi_calories.append(starttime_calories)
    list_of_indi_calories.append(endtime_calories)
    list_of_indi_calories.append(calories)
    # print(list_of_indi_calories)
    list_of_lists_calories.append(list_of_indi_calories)


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
    list_of_indi_steps.append(starttime_steps)
    list_of_indi_steps.append(endtime_steps)
    list_of_indi_steps.append(steps)
    list_of_lists_steps.append(list_of_indi_steps)


df_calories = pd.DataFrame(list_of_lists_calories, columns=[
    "starttime_calories", "endtime_calories", "calories"])

df_steps = pd.DataFrame(list_of_lists_steps, columns=[
    "starttime_steps", "endtime_steps", "steps"])

df_calories.to_csv('calories.csv')
df_steps.to_csv('steps.csv')