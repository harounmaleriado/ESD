# Services:
## authentication
- **create user** : POST /register
- **login** : POST /login
- **get user**  : GET /user/<id>
- **get all users**  : GET /users

## profile
- **read profile** : GET /profile/<id>
- **update profile** : PUT /profile/<id>

## review
- **create review** : POST /reviews
- **get review** : GET /review/<id>
- **get all reviews** : GET /reviews


# How to run in Docker
## Build the images
1. `cd backend/kong` 
2. `docker compose up -d`
3. `cd backend/authentication`
4. `docker build -t <dockername>/auth:1.0`
5. `cd backend/profile`
6. `docker build -t <dockername>/profile:1.0`
7. `cd backend/review`
8. `docker build -t <dockername>/review:1.0`
## Run docker compose
Make sure you are in /backend folder
1. `docker compose up`