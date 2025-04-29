from flask import Flask
from flask_cors import CORS
from source.routes.auth.routes import auth_bp
# from source.routes.forest.prediction import forest_sd
from source.routes.weather_details.weather_details import weather_sd
from source.routes.forest.prediction import predictions_sd
from source.routes.forest.filtered_summary import filtered_summary_sd
from source.routes.forest.filter_options import filter_options_sd
from source.routes.forest.filter_damage import filter_damage_sd
from source.routes.forest.village_counts import village_counts_sd
from source.routes.forest.upload import upload_sd
from source.routes.parse.parse import parse_bp
from source.models.model import MongoDB

mongo = MongoDB()

def create_app():
    
    app = Flask(__name__)
    CORS(app)  

    app.register_blueprint(auth_bp)
    app.register_blueprint(weather_sd,url_prefix='/weather')
    # app.register_blueprint(forest_sd)
    app.register_blueprint(filter_damage_sd, url_prefix="/filter_damage")
    app.register_blueprint(village_counts_sd, url_prefix="/village_counts")
    app.register_blueprint(filter_options_sd, url_prefix="/filter_options")
    app.register_blueprint(filtered_summary_sd, url_prefix="/filtered_summary")
    app.register_blueprint(predictions_sd, url_prefix="/prediction")
    app.register_blueprint(upload_sd, url_prefix="/upload_excel")
    app.register_blueprint(parse_bp, url_prefix='/parser')
    
    @app.teardown_appcontext
    def close_db(exception=None):
        mongo.close()
    
    return app