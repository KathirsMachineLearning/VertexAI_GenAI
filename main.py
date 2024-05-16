import functions_framework
import app

@functions_framework.http
def predictions(request):
    print("Running predictions...")
    print(request)
    # Call the run_predictions method from app.py
    app_instance = app.App()
    app_instance.run_predictions()
    return "Predictions started."

if __name__ == "__main__":
    # This is required for the Functions Framework to be able to serve the function
    functions_framework.main()
