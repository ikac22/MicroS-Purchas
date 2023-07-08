# MicroS-Purchas 
(srb. mikros-purćas)

Micros-Purchas is an app written for university class called Infrastructure for Electronic Business.
The application has 3 types of users:
  - Buyers:
    - search for products
    - order products
    - pay for order
    - mark order as delivered
  - Owners:
    - create new products
    - get product statistics
    - get products category statistics
  - Couriers:
    - take products for delivery
    - search for waiting orders

Couriers and Buyers must register and login on system before interacting with it.
Every user can delete own account.

The app is consiting of 4 services:
  - Authentication service: responsible for authenticating user. (User is then identified via Json Web Token)
  - Buying service: responsible for handling buyers actions
  - Order management service: responsible for handling couriers actions
  - Product management service: responsible for handling owners actions

# Data

The data is separated in two databases:
  - Authentication database
  - Product and Order database

# Containarization

All services are realised using __docker containers__ aswell as databases and paying system(ethernium blockchain).
Services can all be started using docker-compose(using deployment.yml).

# Statistics query

Pruduct statistics aswel as Category statistics are calculated using paralellization in the __Spark Cluster__ of containers.

# Paying system

Paying is realised through smart contracts using __Ethernium Blockchain__.



