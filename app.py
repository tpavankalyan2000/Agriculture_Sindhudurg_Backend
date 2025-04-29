# from flask import Flask
# from flask_cors import CORS
# from auth.routes import *
# from Weather_details.weather_details import *
# from Forest.prediction import *

# app = Flask(__name__)
# CORS(app)  

# app.register_blueprint(auth_bp)
# app.register_blueprint(weather_sd)
# app.register_blueprint(forest_sd)



# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=5050)


from source import create_app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5050)

