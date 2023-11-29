import os.path
from flask import Blueprint, render_template,url_for
import pandas as pd

from app import Config,socketio
from app.routes.auth import login_required
from app.utils.DataframeManager.load_df import load_current_df_memory

production_bp = Blueprint("production",__name__)

@production_bp.route('/production')
@login_required
def production():
    table=""
    if os.path.isfile(Config.PATH_PRODUCTION_DATA):
        df = pd.read_parquet(Config.PATH_PRODUCTION_DATA)
        table = df.to_html(classes="table_class",header=True)
    else:
        table = "No data available yet in this session."    

    return render_template('production.html',table=table)


    

