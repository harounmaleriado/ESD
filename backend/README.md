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

## listings
- **add listing** : POST /listings
- **get listing** : GET /listings/<int:user_id>
- **compare listings** : POST /compare
- **get all listings** : GET /listings 


# How to run in Docker
## Build the images
1. `cd backend/kong` 
2. `docker compose up -d`
3. `cd backend/authentication`
4. `docker build -t <dockername>/auth:1.0 ./`
5. `cd backend/profile`
6. `docker build -t <dockername>/profile:1.0 ./`
7. `cd backend/review`
8. `docker build -t <dockername>/review:1.0 ./`
9. Ensure you are in backend root and run `docker build -t <dockername>/amqp_setup:1.0 ./`
10. `cd backend/listings`
11. `docker build -t <dockername>/listing:1.0 ./`
12. Change the compose.yaml file in the backend root folder to update image name to yours.
## Run docker compose
Make sure you are in /backend folder
1. `docker compose up`

# Alternative way
## Download my images directly from the hub
**No need to edit compose.yaml file**
1. `docker pull tshaun/profile:1.6`
2. `docker pull tshaun/auth:1.8`
3. `docker pull tshaun/review:1.3`
4. `docker pull tshaun/amqp_setup:1.0`
5. `docker pull tshaun/listing:1.4`
5. `docker compose up`
6. Remember to docker compose up kong as well see step 1 and 2 under **"Build the images"**