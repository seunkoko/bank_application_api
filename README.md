[![CircleCI](https://circleci.com/gh/seunkoko/bank_application_api.svg?style=svg)](https://circleci.com/gh/seunkoko/bank_application_api)

# bank_application_api

API for a simple bank application that lets a user creates an account by signing up with his email, password, firstname, lastname, middlename and 
account amount (a starting amount for his/her account, which should not be less than 500). On create, an account number is automatically generated for the 
new user. With this account number, the user (owner) or any other user can deposit money into the account. 

Also, the user can withdraw money from his/her account. All features covered in this api are listed below.

> Note: For learning purposes, you can follow the commit history of this repo.

### Features
---

* Users can create an account.
* Users can login to their account.
* Users can get their profile.
* Users can edit their account.
* Users can delete their account.
* Users can deposit to their account.
* Users can withdraw from their account.

**Authorization**:
Users are authorized by using JSON web token (JWT).
By generating a token on registration and login, API endpoints are protected from unauthorised access.
Requests to protected routes are validated using the generated token.

### Endpoints
---

This is the [link](https://banking-app-api.herokuapp.com) in which to access the api. 

Below are the collection of routes.


#### Users
EndPoint          |   Functionality    |    Request body/params
------------------|--------------------|--------------------------------------------------------------
POST /signup     | Create a user account   | body [email, password, firstname, lastname, middlename, account_amount]
POST /login       | Logs in a user.    | body [email, password]        
GET /user      | Gets a user     | *token
PUT /user     | Edits a user   | *token, body [password, firstname, lastname, middlename]
DELETE /user  | Deletes a user | *token
POST /deposit | Deposits an amount to a user's account | *token, body [account_number, amount]
POST /withdraw | Withdraws from a user's account | *token , body [amount]


### Technologies Used
---

- Python
- Flask
- Flask-Restful
- Flask-Sqlalchemy
- Postgresql
- Sequelize ORM


### Installation
---

- Clone the project repository.
- Run git clone hhttps://github.com/seunkoko/bank_application_api.git.
- Change directory into the bank_application_api directory.
- Create a virtual environment for the python app. You can refer to this [link](https://packaging.python.org/guides/installing-using-pip-and-virtualenv/).
- Activate your vitual environment.
- Install all necessary packages in the requirements.txt file. You can use the command `pip install -r requirements.txt`.
- Create your postgres database. You can checkout [ElephantSql](https://www.elephantsql.com/) or create a database locally.
- Set up your environment variable. Checkout `.env.sample`  in the root folder to do this.
- Export your FLASK_APP `main.py`.
- Upgrade your database by running `flask db upgrade`.
> Note: You do not need to initialize and run migrations because there is a migrations folder already in the application `./migrations`.
- To start your app locally, run `python main.py runserver`.
- Use Postman or any API testing tool of your choice to access the endpoints defined above.
- To run tests, run `pytest -v`.


#### Contributing
---

1. Fork this repository to your account.
2. Clone your repository: git clone https://github.com/seunkoko/bank_application_api.git.
4. Commit your changes: git commit -m "did something".
5. Push to the remote branch: git push origin new-feature.
6. Open a pull request.


#### Suggested Contribution
---

1. Build a `/transfer` endpoint for users to transfer from one account to another. Refer to the comment in the `./api/views/transaction.py` file.
2. Build a frontend that consumes this api.

#### Licence
ISC

Copyright (c) 2018 Oluwaseun Owonikoko
