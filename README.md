# Sherlock 🕵🏽
Sherlock is the main program for fetching prices from various sources to the panprices database.

## How to run
### Dev Envoirment
1. Start the Cloud SQL Proxy by executing `~/Documents/rand_dev/cloud_sql_proxy -instances=panprices:europe-west1:panprices-psql=tcp:5432`. You might get prompted to sign in to Google Cloud. If so make sure that you log in to the panprices project. The proxy will then enable connection to the database locally via port 5432.
2. Then run the application with the starter script `bash run_dev.bash` that sets envoirment variables with the proper database connection info.
### Deployment
1. Then simply execute `gcloud app deploy`
2. Optionaly show the logs via `gcloud app logs tail -s sherlock`

### Run in Docker
1. Build the image: `sudo docker build -t sherlock .`
2. Run the image, everything after the image name will be passed in as variables to the sherlock program: `sudo docker run -t --net=host sherlock --amazon true`
3. Control that the now container is running with `docker ps`
4. Check logs on a running container with `docker logs <CONTAINER ID>`
5. End a running container with `docker kill <CONTAINER ID>`
6. Remove all Docker images `sudo docker rmi -f $(sudo docker images -q)`