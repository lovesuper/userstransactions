# Users-Transactions API Demo

A demo project for managing users and transactions using FastAPI. 

## Functionality

### Authentication
- **POST /v1/auth/users** 
- **POST /v1/auth/staff**

### Users
- **POST /v1/users** 
- **GET /v1/users** 
- **PATCH /v1/users/{user_id}**
- **POST /v1/users/{user_id}/verify** 
- **DELETE /v1/users/{user_id}**
- **GET /v1/users/{user_id}/transactions**
- **GET /v1/users/{user_id}/balance** 

### Transactions
- **POST /v1/transactions** 

## API Documentation

Documentation is available at:
[http://localhost:8000/docs](http://localhost:8000/docs)