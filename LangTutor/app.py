from flask import Flask, render_template, request
import openai
import os 
from dotenv import load_dotenv
load_dotenv()
import regex as re

app = Flask(__name__)

# Set up OpenAI API credentials
openai.api_key = os.environ["OPENAI_API_KEY"]

# Initialize conversation list
conversation = [{'role':'system', 'content':"""
You are a Language tutor for teaching human speaking languages.
Your first task is to greet and ask the my name.
You ask which language do I want to learn.

Give me options like [Spanish , French , German , Russian , Mexican or ask their personal choises of languages]

...wait for my response
You then ask my proficiecy level.

... wait for my response
Based on my language prefernce prepare a course for that language 


start the course by describing how you are going to teach


Strictly follow the below steps
give examples at every step and then provide few exercise for practise in each conversation 
give two line space before staring the exercise for clearner paragraph 
Generate google translate link for the words used for prefered language by me 
strictly print those links in form of JSON format at the last of every conversation

 
"""}]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    # Get user input from the form
    user_input = request.form['user_input']
    
    # Append user input to conversation
    conversation.append({'role':'user', 'content':f"{user_input}"})
    
    # Get response from OpenAI API
    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        temperature=0.0,
        messages = conversation,
    )
    
    # Append OpenAI's response to conversation
    assistant_response = response.choices[0].message["content"]
    
    #extracting link using regex
    deli = str(assistant_response)
    print(deli)
    stri = re.findall('\{.*\}' , deli)
    print(stri)
    if len(stri) == 0:
        print("None")
    else:
        pattern = r'"([^"]*)"'
        links = re.findall(pattern, stri[0])
        print(links)

    


    # senti = openai.ChatCompletion.create(
    #     model = 'gpt-3.5-turbo',
    #     temperature=0.0,
    #     messages = [{'role':'system', 'content':f"""If the paragraph given in triple quotes '''{assistant_response}''' is of type that it has no acces to the data then give output "NO" """}],
    # )
    # sentiment = senti.choices[0].message["content"]
    # print(sentiment)

    if len(conversation) == 7:
        conversation.pop(1)
        conversation.pop(2)

    conversation.append({'role':'assistant', 'content':f"{assistant_response}"})
    
    return {'response': assistant_response}

if __name__ == '__main__':
    app.run(debug=True)

