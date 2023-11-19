# Andmebaaside_Projekt_Beta

# Requirments

-   NodeJS
-   Python 3.11
-   MySQL
-   Docker
-   Docker-compose

## Install Docker Desktop

Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)

This will install Docker Engine, Docker CLI client, Docker Compose, Docker Machine, and Kitematic.

## Install Python

## Install NodeJS

## Install MySQL

## Setup

### Mysql

> ```bash
> mysql -u root -p
> ```
>
> ```mysql
> create database hotel;
> SET @@global.sql_mode= '';
> exit
> ```
>
> ```bash
> mysql -u @USER -p hotel < ./hotel.sql
> ```
>
> modify [docker-compose.yml](docker-compose.yml) line 21 if needed

### Docker

> ```bash
> docker pull python:3.11
> docker pull node:14
> docker-compose build
> docker-compose up
> ```
