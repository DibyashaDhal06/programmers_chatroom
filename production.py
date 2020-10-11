from app import create
import waitress
import os
if __name__ == '__main__':
	application = create()
	port = int(os.environ.get("PORT", 5000))
	#application.run(host='0.0.0.0', port = port, debug = False)
	waitress.serve(application, host='0.0.0.0', port=port, threads=8, )
