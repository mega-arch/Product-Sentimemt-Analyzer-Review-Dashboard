from flask import Flask
from routes.preprocessing_routes import preprocessing_bp
from routes.sentiment_routes import sentiment_bp
from routes.database_routes import db_bp

from flask import Flask
from routes.sentiment_routes import sentiment_bp
from routes.database_routes import db_bp

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(sentiment_bp)
app.register_blueprint(db_bp)

if __name__ == '__main__':
    app.run(debug=True)

