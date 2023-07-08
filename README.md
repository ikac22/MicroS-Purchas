# MicroS-Purchas 
(srb. mikros-purćas)

## Users

Micros-Purchas is an app written for university class called Infrastructure for Electronic Business.
The application has 3 types of users:
  - __Buyers__:
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
  - __Buying service__: responsible for handling buyers actions
  - __Order management service__: responsible for handling couriers actions
  - __Product management service__: responsible for handling owners actions

All of the services are realized using __Flask framework__.

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



