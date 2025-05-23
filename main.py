from waitress import serve
from app import app  # Make sure this matches your Flask file and object

serve(app, host='0.0.0.0', port=80)