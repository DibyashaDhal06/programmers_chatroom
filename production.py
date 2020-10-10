from app import create

if __name__ == '__main__':
	application = create()
	application.run(host='0.0.0.0', port = 8000, debug = False)
