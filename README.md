# MicroS-Purchas 
(srb. mikros-purćas)

Micros-Purchas is an app written for university class called Infrastructure for Electronic Business.

## Users

The application has 3 types of users:
  - __Customer__:
    - search for products 
    - order products
    - pay for order
    - mark order as delivered
  - __Owners__:
    - create new products
    - get product statistics
    - get products category statistics
  - __Couriers__:
    - take products for delivery
    - search for waiting orders

Couriers and Buyers must register and login on system before interacting with it.
Every user can delete own account.

## Services

The app is consiting of 4 services:
  - __Authentication service__: responsible for authenticating user. (User is then identified via Json Web Token)
  - __Customer service__: responsible for handling buyers actions
  - __Courier service__: responsible for handling couriers actions
  - __Owner service__: responsible for handling owners actions

All of the services are realized using __Flask framework__.

## Endpoints
- json object is the data sent via POST requests (_fields_ represents json fields)
- __Auth service__:
  - __POST__ `<auth_service_host>/register_customer` - register customer user
    - fields: __forename, surname, email, password__ 
  - __POST__ `<auth_service_host>/register_courier` - register courier user
    - fields: __forename, surname, email, password__
  - __POST__ `<auth_service_host>/login` - login
    - fields: __email, password__
    - returns jwt access token
  - __POST__ `<auth_service_host>/delete` - delete who is sending request
    - http headers: `Authorization: Bearer <ACCESS_TOKEN>`
- __Owner service__:
  - __POST__ `<owner_service_host>/update`
    - http headers: `Authorization: Bearer <ACCESS_TOKEN>`
    - 
## Data

The data is separated in two databases:
  - Authentication database
  - Product and Order database

Working with database is realized using __SQLAlchemy library__.

## Containarization

All services are realised using __docker containers__ aswell as databases and paying system (ethernium blockchain).
Services can all be started using docker-compose (using deployment.yml).

## Statistics query

Pruduct statistics aswel as Category statistics are calculated using paralellization in the __Spark Cluster__ of containers.

## Paying system

Paying is realised through smart contracts using __Ethernium Blockchain__.



