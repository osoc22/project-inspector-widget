## How to run the project 🏇
### To run locally

* Enter directory

    ``` cd flaskr```

* Install packages

    ```pip install -r requirements.txt```

* Set environment variables
    
    ```cp .env.example .env```

* Upgrade database scheme, if needed
    
    ```flask db upgrade```

* Start app

  ```flask run```

* Head over to `http://localhost:5000`


### To run services as a docker
* Set environment variables
    
    ```cp .env.example .env```

* Enter directory

    ``` cd flaskr```

* Run using

    ```docker-compose up -d```

* Head over to `http://localhost:5000`


There are mainly four models 

* **User** - which contains details about the users
* **Webshop** - which contains details about the webshops
* **Screenshot** - which contains details about the screenshots
* **Product** - which contains details about the products
