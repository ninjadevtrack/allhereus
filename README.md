# AllHere App
> Web app for [AllHere][0]

### DEV Setup
The django and frontend source files are mounted in docker so changes made locally will update the docker container.
```bash
# allhere/
docker-compose -f docker-compose-dev.yml up

# teardown
docker-compose -f docker-compose-dev.yml down
```

### PROD Setup
Be sure to Rename the `.env-example` file to `.env` and add the secrets for production.
```bash
# allhere/
# start as daemon
docker-compose -f docker-compose-prod.yml up -d

# teardown

docker-compose -f docker-compose-prod.yml down
```
**NOTE:** To run this locally on your machine *add* the following line to your hosts file. **DO NOT** change the existing entries!
```bash
# /etc/hosts
# exiting host file data here (DON'T TOUCH)
# add the following
127.0.0.1       platform.allhere.co
```



### Create SuperUser
You can use this account to login the the admin panel at [http://localhost:8000/admin][1]
```bash
# allhere/
# dev
docker-compose -f docker-compose-dev.yml exec web python manage.py createsuperuser

# prod
docker-compose -f docker-compose-prod.yml exec web python manage.py createsuperuser
```

### Run Tests
```bash
# allhere/
docker-compose -f docker-compose-dev.yml exec web python manage.py test
```

### Dependencies

#### Frontend

- http://getbootstrap.com
- https://popper.js.org/
- https://bootstrap-datepicker.readthedocs.io/en/stable/


[0]: http://www.allhere.co
[1]: http://localhost:8000/admin
