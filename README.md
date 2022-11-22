# eCommerce
Free open source microservices eCommerce Application with django and vue.js. 

### Prerequisites:

- GIT (latest)
- Python ≥ 3.8
- Node.js ≥ 14.0.0
- Docker Desktop or (Docker Engine and Docker Compose)
- Any code editor or IDE (PyCharm recommended for Python and Django)
- Any database client (optional)

## Installation

Clone the project

Via SSH:
```bash
git clone git@github.com:abdoohossamm/eCommerce.git
```
Via HTTPS:
```bash
git clone https://github.com/abdoohossamm/eCommerce.git
```

Change directory to the cloned project

```bash
cd eCommerce
```



## Run the project

### Production environment (Docker):
Make a copy of the example environment variables file and call it `.env`

```bash
cp .env.example .env
```
Edit the .env file and enter you own environmental variables.

##### Make sure the ports you use are free to use for backend, database, and frontend application.

There are two ways to use docker compose depends on the docker version:

* first:
```bash
docker compose up
```
* second:
```bash
docker-compose up
```

* if there was an error try to use `--build` to build the images that is stored in dockerfile

### Development environment environment:

- For main_app application read [Main App README](https://github.com/abdoohossamm/eCommerce/tree/main/main_backend#readme) for more details
- For frontend application read [Frontend README](https://github.com/abdoohossamm/eCommerce/tree/main/frontend#readme) for more details

## Version History

* Under Development
    * The project still under development