# news-board-api-app
_A Web API for news publish_
### _Before you start:_
I used Docker to build this app and it requires to install some dependencies to manage this project on your local machine. So be confident in your OS (Windows 10 Pro or any Unix system) which has installed packeges of [python3](https://www.python.org/downloads/), [git](https://www.atlassian.com/git/tutorials/install-git), [Docker](https://docs.docker.com/get-docker/).
### _Requirements:_
* Django
* Django REST Framework
* psycopg2
* flake8
* black
### _Lets begin!_
1. Clone this repository to your local machine with specific project name
      ```
      git clone http://github.com/crocodundee/news-board-api-app.git
      ```
2. Open terminal in project's root directory and build Docker container with
    ```
    docker-compose build
    ```
3. Init database schema with
    ```
    docker-compose run app sh -c "python manage.py makemigrations"
    ```
4. Create admin user to manage site with
    ```
    docker-compose run app sh -c "python manage.py createsuperuser"
    ```
5. Run project and view result in your browser on _0.0.0.0:8000_ :
    ```
    docker-compose up
    ```

### _Demo-version:_  [news-board-api-app](https://news-board-api-app.herokuapp.com/)
### _Postman docs_ : [api-collection](https://www.getpostman.com/collections/476f834f47fa04dabc99)
