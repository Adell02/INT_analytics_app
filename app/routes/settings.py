from flask import Blueprint, render_template,request,url_for,session

from app.routes.auth import login_required
from app.database.seeder import *
from app.utils.account.token import *

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/settings', methods=["GET", "POST"])
@login_required
def settings():
    if request.method == 'POST':
        print(request.form)
        if 'entity_name' in request.form:
            entity_name = request.form['entity_name']
            entity_token = request.form['entity_token']
            
            if entity_name != session['org_name']:
                edit_user(session['user_email'],'org_name',entity_name)            
                session['org_name'] = entity_name
                # show in screen message saying entity name has been updated

            if entity_token != session['external_token']:
                admin_user = check_existance("personal_token",entity_token)
                if admin_user:
                    edit_user(session['user_email'],'external_token',entity_token)                
                    session['external_token'] = entity_token  
                    # show in screen message saying entity token has been updated 
        elif 'data_read' in request.form:
            data_read = request.form.get('data_read')
            number_rows = request.form.get('number_rows')
            downsampling = request.form.get('downsampling')

            print(data_read, downsampling, number_rows)

            


    url_change_password = url_for("auth.change_password",token_user=generate_token(session['user_email']) )

    return render_template('settings.html', url_change_password = url_change_password)

