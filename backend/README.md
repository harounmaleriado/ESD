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
`cd backend/kong`
`docker compose up -d`
`cd backend/authentication`
`docker build -t <dockername>/auth:1.0`
`cd backend/profile`
`docker build -t <dockername>/profile:1.0`
`cd backend/review`
`docker build -t <dockername>/review:1.0`
## Run docker compose
Make sure you are in /backend folder
`docker compose up`