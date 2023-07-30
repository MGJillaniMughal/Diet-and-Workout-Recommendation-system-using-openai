from flask import Flask, render_template, request
import os
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
import re

# Set your OpenAI API key
os.environ['OPENAI_API_KEY'] = 'sk-######' #### replace this and past your api key here

app = Flask(__name__)

# Initializing OpenAI language model for diet recommendations
llm_resto = OpenAI(temperature=0.6)
prompt_template_resto = PromptTemplate(
    input_variables=['age', 'gender', 'weight', 'height', 'veg_or_nonveg', 'disease', 'region', 'allergics', 'foodtype', 'activity', 'calorie_goal', 'lunch', 'preferred_cuisine', 'dietary_restrictions'],
    template="Diet Recommendation System:\n"
             "I want you to recommend 6 restaurants names, 6 breakfast names, 5 lunch names, 5 dinner names, and 6 workout names, "
             "based on the following criteria:\n"
             "Person age: {age}\n"
             "Person gender: {gender}\n"
             "Person weight: {weight}\n"
             "Person height: {height}\n"
             "Person veg_or_nonveg: {veg_or_nonveg}\n"
             "Person generic disease: {disease}\n"
             "Person region: {region}\n"
             "Person allergics: {allergics}\n"
             "Person foodtype: {foodtype}\n"
             "Person activity level: {activity}\n"
             "Person calorie goal: {calorie_goal}\n"
             "Person lunch: {lunch}\n"
             "Person preferred cuisines: {preferred_cuisine}\n"
             "Person dietary restrictions: {dietary_restrictions}."
)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recommend', methods=['POST'])
def recommend():
    if request.method == "POST":
        # Extracting user input data from the form
        age = request.form['age']
        gender = request.form['gender']
        weight = request.form['weight']
        height = request.form['height']
        veg_or_noveg = request.form['veg_or_nonveg']
        disease = request.form['disease']
        region = request.form['region']
        allergics = request.form['allergics']
        foodtype = request.form['foodtype']
        activity = request.form['activity']
        calorie_goal = request.form['calorie_goal']
        lunch = request.form['lunch']
        preferred_cuisine = request.form['preferred_cuisine']
        dietary_restrictions = request.form['dietary_restrictions']

        # Initializing LLMChain with the OpenAI model and prompt template
        chain_resto = LLMChain(llm=llm_resto, prompt=prompt_template_resto)

        # Preparing input data dictionary
        input_data = {
            'age': age,
            'gender': gender,
            'weight': weight,
            'height': height,
            'veg_or_nonveg': veg_or_noveg,
            'disease': disease,
            'region': region,
            'allergics': allergics,
            'foodtype': foodtype,
            'activity': activity,
            'calorie_goal': calorie_goal,
            'lunch': lunch,
            'preferred_cuisine': preferred_cuisine,
            'dietary_restrictions': dietary_restrictions
        }

        # Generating diet and workout recommendations using the input data
        results = chain_resto.run(input_data)

        # Extracting the different recommendations using regular expressions
        restaurant_names = re.findall(r'Restaurants:(.*?)Breakfast:', results, re.DOTALL)
        breakfast_names = re.findall(r'Breakfast:(.*?)Lunch:', results, re.DOTALL)
        lunch_names = re.findall(r'Lunch:(.*?)Dinner:', results, re.DOTALL)
        dinner_names = re.findall(r'Dinner:(.*?)Workouts:', results, re.DOTALL)
        workout_names = re.findall(r'Workouts:(.*?)$', results, re.DOTALL)

      
        # Check if the lists are not empty before processing them
        if restaurant_names:
            restaurant_names = [name.strip() for name in restaurant_names[0].strip().split('\n') if name.strip()]
        else:
            restaurant_names = []

        if breakfast_names:
            breakfast_names = [name.strip() for name in breakfast_names[0].strip().split('\n') if name.strip()]
        else:
            breakfast_names = []

        if lunch_names:
            lunch_names = [name.strip() for name in lunch_names[0].strip().split('\n') if name.strip()]
        else:
            lunch_names = []

        if dinner_names:
            dinner_names = [name.strip() for name in dinner_names[0].strip().split('\n') if name.strip()]
        else:
            dinner_names = []

        if workout_names:
            workout_names = [name.strip() for name in workout_names[0].strip().split('\n') if name.strip()]
        else:
            workout_names = []




        return render_template('result.html', restaurant_names=restaurant_names, breakfast_names=breakfast_names,
                               lunch_names=lunch_names, dinner_names=dinner_names, workout_names=workout_names,
                               preferred_cuisine=preferred_cuisine, dietary_restrictions=dietary_restrictions)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
