# Backend
❗ Make sure that Python, Bash and Docker Desktop is installed on your system before continuing.

## How to run the project 🏇
### To run services as a docker container 🐳

* Enter directory

    ``` cd flaskr```

* Set environment variables
    
    ```cp .env.example .env```

* Run using

    ```docker-compose up -d```

* Head over to `http://localhost:8500`

### To run **a particular service** as a docker container 🐳

* To run flask application

     ```docker-compose up -d flask_app  ```

* To run postgres database (Do not forget to upgrade database scheme, if needed)

    ```docker-compose up -d postgres  ```

## Data Models 📈

There are mainly five models 

* **User** - which contains details about the users
* **Webshop** - which contains details about the webshops
* **Screenshot** - which contains details about the screenshots
* **Product** - which contains details about the products
* **Scraper** - which contains details about the scrapers

## Endpoints 🛣️

**Authentication**

The backend uses JWT tokens for authentication.
* POST `/register` - to register a new user

    Request body:
    ```
    {
        "email": "string",
        "username": "string",
        "password": "string"
    }
    ```

* POST `/login` - to login as a user

    Request body:

  ```
    {
        "username": "string",
        "password": "string"
    }
    ```
    
    If the username and password succesfully match, the response output will contain:
     ```
    {
        "access_token": "string",
        "refresh_token": "string"
    }
    ```

    Now, you can call endpoints with the access token:
    ```
    axios
        .get(
            "https://localhost:8500/scrapers",
            {
                headers: {
                Authorization: `Bearer ${access_token}`,
                },
            }
        );
    ```

❗ These paths require authentication before use
* DELETE `/logout`- to logout
* POST `/refresh` - to refresh access token
* GET `/user` - to get user information of the logged-in user
* GET `/scrapers/user` - to get a list of scrapers added by the logged-in user

**CRUD**

❗ These paths require authentication before use
* GET `/start-scraper/{id}` - to start a specific scraper resource
* POST `/scrapers` - to add a new scraper resource
* GET `/scrapers` - to get the list of all scraper resources
* GET `/scrapers/{id}` - to get a specific scraper resource
* DELETE `/scrapers/{id}` - to delete a specific scraper resource
* GET `/scrapers/{id}/results` - to get the list of all products tied to a specific scraper resource
* GET `/scrapers/{id}/export` - to get the list of all products tied to a specific scraper resource + screenshots in a zip file
* GET `/products` - to get the list of all products
