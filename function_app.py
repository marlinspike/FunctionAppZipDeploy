import azure.functions as func

app = func.FunctionApp()

# Import the blueprints
from http_function import bp as http_bp
from timer_function import bp as timer_bp

# Register the blueprints
app.register_functions(http_bp)
app.register_functions(timer_bp)