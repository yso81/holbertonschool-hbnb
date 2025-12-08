# Part 2: Implementation of Business Logic and API Endpoints #

**0. Project Setup and Package Initialization**
## Project directory structure ##

The project setup will comprise of the **Presentation**(API Endpoints, Services, Request Handlers), **Business Logic**(User Model, Place Model, Review Model, Amenity Model), and **Persistence**(Database Access, Repository) layers with the necessary folders, packages, and files.

```
hbnb/
├── venv/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       ├── amenities.py
│   │       ├── auth.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   │   ├── base_model.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── facade.py
│   │   ├── amenity_service.py
│   │   ├── place_service.py
│   │   ├── review_service.py
│   │   ├── user_service.py
│   ├── persistence/
│       ├── __init__.py
│       ├── repository.py
├── sql/
│   ├── hbnb_schema.sql
│   ├── hbnb_data.sql
│   └── hbnb_test.sql
├── run.py
├── config.py
├── requirements.txt
├── README.md
├── setup_admin.py
├── test_amenity.py
├── test_place.py
├── test_review.py
├── test_user.py
```

Explanation:

1. The app/ directory contains the core application code.
2. The api/ subdirectory houses the API endpoints, organized by version (v1/).
3. The models/ subdirectory contains the business logic classes (e.g., user.py, place.py).
4. The services/ subdirectory is where the Facade pattern is implemented, managing the interaction between layers.
5. The persistence/ subdirectory is where the in-memory repository is implemented. This will later be replaced by a database-backed solution using SQL Alchemy.
6. run.py is the entry point for running the Flask application.
7. config.py will be used for configuring environment variables and application settings.
8. requirements.txt will list all the Python packages needed for the project.

The **in-memory repository** (hbnb/app/persistence/repository.py) handle object storage and validation. It follows a consistent interface that will later be replaced by a 
database-backed repository.

The **Facade Pattern** (hbnb/app/services/facade.py) handle communication between the 
Presentation, Business Logic, and Persistence layers.

In the requirements.txt file, the Python packages needed for the project:
```
flask
flask-restx
```
Install the dependencies using:
```
pip install -r requirements.txt
```
Activate the `venv` module (use: `source venv/bin/activate`) before running the application in a new terminal window using:
```
python run.py
```

**1. Core Business Logic Classes**
## Core Business Logic Classes ##
A fully implemented core business logic classes (User, Place, Review, Amenity) with the appropriate attributes, methods, and 
relationships. The implemented classes support the necessary validation, relationships, and data integrity checks required 
for the application’s core functionality. Additionally, the relationships between entities are fully operational, allowing 
seamless interactions like linking reviews to places or associating amenities with places.

### Activate the environment: ###
To run the test files (e.g. test_user.py, test_place.py, test_amenity.py, test_review.py )in an `venv` module, use:
```
source venv/bin/activate
```
### Deactivate the environment: ###
When you're finished, you can exit the environment with the command:
```
deactivate
```

**2. User Endpoints**
## Implement the User Endpoints ##
The API endpoints needed for managing users in the HBnB application. The implementation of the core user management endpoints, including the ability to create, read, and update users. The DELETE operation will not be implemented for users in this part.

### `POST /api/v1/users/`: Registers a new user and performs a check for email uniqueness ###

**Explanation:**

- The POST endpoint registers a new user and performs a check for email uniqueness.
- If the email is already registered, the API returns a 400 status code with an error message.
- If input data is missing or invalid, a 400 status code is returned with a relevant error message by the framework thanks to the validate=True parameter.
- The Facade handles all interactions between layers.

### `GET /api/v1/users/<user_id>`: Retrieves user details by ID ###

**Explanation:**

- The GET endpoint retrieves user details by ID.
- If the user does not exist, the API returns a 404 status code with an error message.

### `Update a User (PUT /api/v1/users/<user_id>)` : Updates user details ###

**Explanation:**

- Users may update their own profiles on the application, changing details such as their name, email, or preferences.

**3. Amenity Endpoints**
## Implement the Amenity Endpoints ##
The endpoints handle CRUD operations (Create, Read, Update) for amenities, while ensuring integration with the Business Logic layer via the Facade pattern.

## Database Diagrams ##
**ER diagram**
<pre class="mermaid">
erDiagram
    %% USER TABLE
    User {
        CHAR(36) id PK "UUID"
        VARCHAR(255) email UK "Unique"
        VARCHAR(255) password
        VARCHAR(255) first_name
        VARCHAR(255) last_name
        BOOLEAN is_admin "Default FALSE"
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }

    %% PLACE TABLE
    Place {
        CHAR(36) id PK "UUID"
        VARCHAR(255) title
        TEXT description
        DECIMAL price "Precision 10,2"
        FLOAT latitude
        FLOAT longitude
        CHAR(36) owner_id FK "Ref: User.id"
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }

    %% REVIEW TABLE
    Review {
        CHAR(36) id PK "UUID"
        TEXT text
        INT rating "Check: 1-5"
        CHAR(36) user_id FK "Ref: User.id"
        CHAR(36) place_id FK "Ref: Place.id"
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }

    %% AMENITY TABLE
    Amenity {
        CHAR(36) id PK "UUID"
        VARCHAR(255) name UK "Unique"
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }

    %% PLACE_AMENITY (ASSOCIATION TABLE)
    Place_Amenity {
        CHAR(36) place_id PK,FK
        CHAR(36) amenity_id PK,FK
    }

    %% RELATIONSHIPS
    
    %% A User can own many Places (1 to Many)
    User ||--o{ Place : "owns"

    %% A User can write many Reviews (1 to Many)
    User ||--o{ Review : "writes"

    %% A Place can have many Reviews (1 to Many)
    Place ||--o{ Review : "receives"

    %% Many-to-Many Relationship between Place and Amenity
    %% Broken down into two One-to-Many relationships via the Join Table
    Place ||--o{ Place_Amenity : "has"
    Amenity ||--o{ Place_Amenity : "included in"
</pre>

!(images/ERdiagram.png)
![ER diagram](part2/hbnb/images/ERdiagram.png)
