from app import dashapp
import callbacks

if __name__ == "__main__":
	dashapp.app.run_server(debug=False)