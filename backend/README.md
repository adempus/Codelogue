# backend

### IDE Integration
If your IDE cannot resolve the project's dependencies, you have to specify the project's interpreter in your IDE's settings.
Run: ```poetry env info --path``` and copy the output.

This path includes the interpreter configured for the project. In an IDE like Pycharm for example, you:
1. Go to settings.
2. Then go into `Project Interpreter`, click the gear icon to the right of dropdown at the top, and click `Add...` 
3. When the window opens, select `Existing enviornment`, and click `...` to paste the path you copied.  
4. In the bin folder depicted for that path, double click the file  named `python`. 

Pycharm should now recognize the project's dependencies, clearing all errors. 

### DB Migration
Backend uses MySQL for the database. Though python packages are included via Poetry to interact with it, you might need 
to do additional setup on your end to get MySQL working locally. Flask-Migrate is used for database migrations which are 
specified in the `migrations` folder. 
 
##### NOTE: if the ```migrations``` folder is present, then skip this step)
if not, you can initialize migrations by running:
```
flask db init
```

After the migrations folder is created with the above command, you can run them with 

```
flask db migrate -m"sample comment for the migration"
```

Before doing so, make sure flask env variables are set first. You then finalize the migrations by running:
```
flask db upgrade
```

### .env file
Before running the server, you must create a .env file, It contains credentials like database access info, and application 
key data that is read into enviornment variables on app startup. 

It should look like this:   
```
# database credentials
DB_DRIVER="postgresql"
DB_USER="username"
DB_NAME="db_name"
DB_PASSWORD="db_password123"
DB_HOST="127.0.0.1"
DB_PORT=5432

#app key
APP_KEY="secretkey123"
```

### Testing
Use a client like GraphQL Playground or Apollo explorer with included graphql queries and mutations to test API endpoints.

### Docker Compose

In project root folder, there is a docker-compose.yml file. Navigate to project root.

Install everthing the project needs: 

```docker-compose build```

Run all the project containers (for the first time): 

```docker-compose up```

Get into the shell for backend container: 

```docker-compose run backend bash```

Run manage.py command to create the database tables

```python manage.py create_db```

Run manage.py command to seed the database with default records

```python manage.py seed_db```

That should set the backend up properly for use. The database can be accessed directly through the db container shell:

```docker-compose run db bash```

Then running postgres in the container, where a password will be prompted: 

```psql -h db -p 5432 -U username -d codelogue_db``` 

To stop running project containers: 

```docker stop codelogue_db_container codelogue_server_container codelogue_client_container``` 

For subsequent runs of the project container:

```docker start codelogue_db_container codelogue_server_container codelogue_client_container```

To remove the containers with their storage volumes (this deletes all data from database container):
```docker-compose down -v```


### Rebuild a single container

To rebuild a single container, first remove it:

```docker rm codelogue_server_container```

Then rebuild it:

```docker-compose build backend```

Then re-run it: 

```docker-compose up backend```
