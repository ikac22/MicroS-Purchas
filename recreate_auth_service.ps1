docker-compose -f deployment.yaml stop
docker container rm projekat-auth-service-1
docker rmi auth-service-image
docker build --file AuthServiceDockerfile -t auth-service-image .