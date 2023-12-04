import openai
import pandas
import numpy

def ai_request(df:pandas.DataFrame,request:str,columns:list) -> str:
    error_log = "Service not available"
    not_answerable = "I can't answer your request"
    is_checked = check_user_input(request,columns)
    is_checked = "yes"

    if is_checked == -1:
        return error_log
    
    if is_checked == 'No':
        return not_answerable
    
    python_code = request_python_function(request,columns)

    if python_code == -1:
        return error_log
    try:
        result_raw = {}  
        exec(python_code+"\nresult = ai_process(df)",locals(),result_raw)    
        return result_raw['result']
    except:
       return error_log

    
def parse_response(response):
    try:
        response = response['choices'][0]['message']['content']
        if len(response):
            return response
    except:
        return -1
    return -1
        
def check_user_input(request:str,columns:list):
    s = "Given a pandas dataframe with the following columns: "+",".join(map(str,columns)) + ". Is it reasonable to ask for: "+request+"?\nAnswer 'Yes' if affirmative, 'No' if negative."
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": s
        }
    ],
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0)

    return parse_response(response)  
  

def request_python_function(request:str,columns:list):
    s = "Give a python function named ai_process(df), where \"df\" is a pandas dataframe with the following columns: " +",".join(map(str,columns))+". This function will compute the following request: \'"+request+"\'. return a string containing the answer. (PRINT JUST THE CODE)"
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {
          "role": "user",
          "content": s
        }        
      ],
      temperature=0.4,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    return parse_response(response)  
