# fastapi-crud

1) Create your MYSQL/MARIADB database name, in this script for example 'aham'
2) Update MYSQL/MARIADB database name and configurations/setup in .env file
3) Run below command to install python packages

pip install fastapi uvicorn sqlalchemy pydantic pydantic[dotenv] pydantic[email] mysqlclient pymysql pyjwt[encryption] passlib[bcrypt] python-decouple config

4) Go to fastapi-crud-main folder(cd fastapi-crud-main) and run below command to invoke FastAPI

uvicorn app.main:app --host localhost --port 8000 --reload 

5) Open browser and open urlhttp://localhost:8000/docs

6) Create new user under route/endpoint POST api/users. 
-> Click 'Try it out' button, fill in username and password and click Execute button.

7) Copy access_token hash in response body and click Authorize lock on top right screen. Paste the hash in the value and click Authorize button

8) Now you are able to add, view and delete customers under route/endpoint POST api/customers
