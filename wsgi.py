# Application entry point.
# Gunicorn calls this process to start it up.
# Use the startup script provided for understanding it better
import os
import app

if __name__ == "__main__":
	production = "gunicorn" in os.environ.get("SERVER_SOFTWARE", "")
	print('Application loaded as ', 'PROD' if production else 'DEBUG')
	application = app.create()
	serve(application, host='0.0.0.0', port=8000)
