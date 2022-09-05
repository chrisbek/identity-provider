# Identity Provider
Read the full docs at: [authentication-as-a-service](https://christopher.bekos.click/portfolio/authentication-as-a-service).

This is a simple identity provider service, responsible for managing the lifecycle of:
- users
- roles
- resources and operations
It provides an API to easily create users, creates roles that grant specific operations to resources, and the
allows the assignment of roles to users.

The project is created to be used as part of a set of microservices, that achieve authentication & authorization in a larger
system (detailed explanations can be found in the full docs).

## Technologies used
- `FastAPI`: for the api creation
- `Poetry`: for dependency management
- [Dependency Injector](https://python-dependency-injector.ets-labs.org/) for dependency injection, singleton pattern
implementation, and project structure.
- `Alembic`, and `SqlAlchemy` for migrations and orm, respectively.
- `Docker` and `DockerComposer` for containerization.


## Local Setup
- Add the following line to your `/etc/hosts`:
```
172.30.0.5	identity-provider.local
```

- Clone the [local-stack](https://github.com/chrisbek/local-stack) and start a MySQL server by running:
```
make start-databases
```

- Run `./start.sh` to start the project (along with the db) and `./stop.sh` to stop it

- Find the openapi spec at http://identity-provider.local/docs
