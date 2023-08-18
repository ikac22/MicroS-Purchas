docker-compose -f deployment.yaml stop
docker container rm projekat-sparkapp-1
docker rmi sparkapp
docker build --file sparkapp/Dockerfile -t sparkapp sparkapp/