#docker-compose -f deployment.yaml stop
docker container rm projekat-owner-service-1
docker container rm projekat-buyer-service-1
docker container rm projekat-courier-service-1
docker rmi buyer-service-image
docker rmi courier-service-image
docker rmi owner-service-image
docker build --file BuyerServiceDockerfile -t buyer-service-image .
docker build --file CourierServiceDockerfile -t courier-service-image .
docker build --file OwnerServiceDockerfile -t owner-service-image .
