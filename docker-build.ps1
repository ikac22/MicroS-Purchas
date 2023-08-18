docker build --file BaseDockerfile . -t service-base
docker build --file AuthServiceDockerfile . -t auth-service-image
docker build --file BuyerServiceDockerfile . -t buyer-service-image
docker build --file CourierServiceDockerfile . -t courier-service-image
docker build --file OwnerServiceDockerfile . -t owner-service-image
docker build --file sparkapp/Dockerfile -t sparkapp sparkapp/