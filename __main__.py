from app import create

if __name__ == '__main__':
	application = create()
	port = int(os.environ.get("PORT", 5000))
	application.run(host='0.0.0.0', port = port, debug = True)
