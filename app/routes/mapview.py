from flask import Blueprint, render_template

from app.routes.auth import login_required


mapview_bp = Blueprint("mapview",__name__)

@mapview_bp.route('/mapview')
@login_required
def mapview():
    return render_template('mapview.html')



