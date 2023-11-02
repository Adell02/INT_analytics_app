from flask import Blueprint, render_template,request,session
import pandas as pd

from app.routes.auth import login_required
from app.database.seeder import *
from app.utils.account.token import *
from app.utils.AI.openai_request import *

ai_chat_bp = Blueprint('aichat', __name__)

@ai_chat_bp.route('/aichat', methods=["GET", "POST"])
@login_required
def ai_chat():
    if 'chat' in session.keys():
        #session.pop('chat')
        pass
    if request.method == "POST":
        if request.form['data'] != '':            
            dataframe = pd.DataFrame(session['df'])
            #response_ai = ai_request(dataframe,request.form['data'],dataframe.columns)
            response_ai = 'City mode percentage: 623.8823872683247%\nSport mode percentage: 195.69808216863078%\nFlow mode percentage: 180.41953056304445%'
            if 'chat' not in session.keys():
                session['chat'] = [{'role':'user','value':request.form['data']},{'role':'assistant','value':response_ai}]
            else:
                session['chat'].append({'role':'user','value':request.form['data']})
                session['chat'].append({'role':'assistant','value':response_ai})
        return session['chat']
    chat = session['chat'] if 'chat' in session.keys() else []

    return render_template("ai_chat.html",chat = chat)