# AllHere App
> Web app for [AllHere][0]

## Backend setup
```bash
# allhere/
cd backend && \
python3 -m venv && \
venv/bin/activate && \
pip install -r requirements.txt
```

### Start DEV server 
```bash
# allhere/backend/ (venv)
python manage.py runserver
```
### Create SuperUser
You can use this account to login the the admin panel at [http://localhost:8000/admin][1]
```bash
# allhere/backend/ (venv)
python manage.py createsuperuser
```

[0]: http://www.allhere.co
[1]: http://localhost:8000/admin
