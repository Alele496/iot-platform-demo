# Example config.py for open source use
# Copy this file to config.py and fill in your own credentials

class Config:
    # TDengine configuration
    TDENGINE_URL = "http://tdengine:6041/rest/sql"  # Use your TDengine REST API URL
    TDENGINE_AUTH = ('your_tdengine_user', 'your_tdengine_password')

    # MQTT configuration
    MQTT_BROKER = "your_broker"  # e.g. emqx or IP address
    MQTT_PORT = 1883
    MQTT_TOPIC = "sensors/dht11"
    MQTT_USERNAME = "your_username"
    MQTT_PASSWORD = "your_password"

    # Flask configuration
    SECRET_KEY = "your-secret-key-here"
    CORS_ORIGINS = "*"
    FLASK_ENV = "development"
    FLASK_DEBUG = True
    FLASK_HOST = "0.0.0.0"
    FLASK_PORT = 5000
