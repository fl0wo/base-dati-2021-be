# base-dati-2021-be
Progetto Base Dati BackEnd

# pre-alpha 0.1 

TODO : 

1) database.conf should not be inside this repo (all passwords users ecc should be crypted (see Volt ecc...))

2) i would like to supplement Liquidbase framework to create some database-schema-migrations during development of the database logic.

3) buy OVH server and put everything online

4) setup FE-github free hosting 

5) create blue-red pipeline for CI/CD

6) allow Dockerfile POSTGRES_HOST env variable to work even with 'localhost' or '127.0.0.1'

## Architecture : 

This is a really really basic project based on a single postgreSQL database which is connected from a single flask rest-applications server which in turn communicates with the basic front-end webpage.

The purpose of this project is also to dockerize as much as possible, in order to, after-all enable a easy blue-red pipeline for CI/CD scope.

Everything will be deployed in a OVH virtual private server, with port fowarding only for the FE.

The BE and BD components will be placed in the remote OVH private server, but the FE code will be free-hosted by a GitHub repository.

## Init in localhost : 

You should have installed Docker[https://docs.docker.com/get-docker/] in your local machine.

And also docker-compose[https://docs.docker.com/compose/install/].

Before proceeding with the build and run of the project be carefull on setting correctly the POSTGRES_HOST env variable inside the Dockerfile file.

In order to set it correctly check your own local machine ip, and set it as you see (please don't set 127.0.0.1 or localhost as local ip cause could not work. (TODO))

### PostgreSQL(docker)

Command line for the PostgreSQL docker container : 

In the same folder of docker-compose.yml run : 
```
docker-compose up
```

To see the image and container you just created :
```
docker image ls
docker ps
```

### Flask Application(docker)

Command list for the Flask docker container : 

In the same folder of the Dockerfile run : 
```
docker build -t flask:0.1 .
docker run -dit -p 5000:5000 flask:0.1
docker container logs -f {id}
```

### End

Now you can interact with the rest-application server with Postman, for example : 

curl --location --request POST 'http://127.0.0.1:5000/add' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name" : "Ivan",
    "price" : 3000,
    "breed" : "type"
}'

curl --location --request GET 'localhost:5000/'