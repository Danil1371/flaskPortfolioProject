# Portfolio (Backend)


## About

The project is a RESTful API web application developed in Python using the Flask framework. It includes the following main routes and functions:

- User registration and authentication
- User profile management (CRUD operations)
- Getting a list of users
- Admin panel
- Tests
- Documentation


## Technologies

The project uses the following main libraries and tools:

- Flask - a microframework for web applications in Python
- SQLAlchemy - ORM for database operations
- PostgreSQL - a relational database management system
- Flask-JWT-Extended - Flask extension for working with JWT tokens
- Flask-Admin - admin panel for data management
- Pytest - a framework for writing and running tests
- Swagger - a tool for automatic API documentation generation


## Database Usage

Two different PostgreSQL databases are used for projects and tests. The application will use the main database to process queries, and the tests will run on a separate test database to ensure data isolation and testing reliability.


## Accessing the Admin Panel

To access the administrative panel (Flask-Admin), use the following link after launching the application:

http://127.0.0.1:5000/admin


## Documentation

The API documentation is available after running the application at the following address:

http://127.0.0.1:5000/apidocs


## Running Tests

To run the tests, execute the following command in the project's root directory. This command will run the tests from the tests directory, providing detailed information about test execution:

```bash
pytest -v -s tests
```
