from . import create_app

app = create_app()


@app.route('/') 
def index():  
     return "Welcome to the backend server"

if __name__ == '__main__': 
     app.run(debug=True)