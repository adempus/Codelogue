# backend

All dependencies for backend are packaged and managed with Poetry. Setup requires Poetry be installed first.
If it's not, run: ```pip install --user poetry``` to install it. More details: https://python-poetry.org/docs/#installing-with-pip

### Installing Project Dependencies
If you have Poetry installed, To install dependencies for backend, just run: ``` poetry install ```

### Checking dependencies
enter ```poetry show``` in the terminal to check what python packages the backend depends on.

### Installing Packages
To install new packages for use in the project, run: ```poetry add package-name```. Newly added packages will be included
in the `poetry.lock` and `pyproject.toml` files. So make sure they're included to commit in repo. 

### IDE Integration
If you IDE cannot resolve the project's dependencies, you have to specify the project's interpreter in your IDE's settings.
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

You then finalize the migrations by running:
```
flask db upgrade
```

### .env file
Before running the server, you must create a .env file, It contains credentials like database access info, and application 
key data that is read into enviornment variables on app startup. 

It should look like this:   
```
# database credentials
DB_DRIVER="mysql"
DB_USER="username"
DB_NAME="db_name"
DB_PASSWORD="db_password123"
DB_HOST="127.0.0.1"
DB_PORT=3306

#app key
APP_KEY="secretkey123"
```
Just change the quoted values to match credentials provided for your test db and app key. 
##### NOTE: the `.env` file should be gitignored!

### Running the server
Specify app entrypoint: ```export FLASK_APP=main```  
Specify debug mode: ```export FLASK_ENV=development```  
Start server: ```flask run```
