from main.app import create_app
from main.mysql_retry import wait_for_mysql

app = create_app()

if __name__ == "__main__":
    if wait_for_mysql():
        app.run(debug=True)
    else:
        print("Exiting due to MySQL failure.")
