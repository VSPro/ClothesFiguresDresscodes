### For install app
pipenv shell
pipenv install

### For run app
FLASK_ENV=development FLASK_APP=app pipenv run python -m flask run --port=8080

### For start/stop db container
docker-compose up -d
docker-compose down

### For connecting to db container
docker-compose exec postgresw psql -U postgres -d workshop

### For building and starting Docker images
sudo docker build -t ubuntu-test:latest -f rabbit.dockerfile .
sudo docker run -it -p 15672:15672  rabbitmq:3-management

 sudo docker run -it -p 15672:15672 -p 5672:5672  rabbitmq:3-management