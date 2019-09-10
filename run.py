from app import dashapp
import routes
import callbacks


if __name__ == "__main__":
	dashapp.app.run_server(debug=False)