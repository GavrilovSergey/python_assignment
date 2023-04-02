# A brief project description

A take-home assignment is to evaluate my abilities to use API, data processing and transformation, SQL, and implement a new API service in Python.
Forked from [here](https://github.com/G123-jp/python_assignment) where the original tasks description can be found.

# Tech stack used in this project

-Docker
-Python
-Postgres
-FastAPI and other packages listed in requirements.txt

# How to run your code in local environment

1. As requested in the original description the two services (Database and your API) are up and running if one performs the following action (assuming docker-compose is available locally):

    ```bash
    docker-compose up
    ```

2. the file `get_raw_data.py` contains the code for **Task1** (Retrieves the financial data of Two given stocks (IBM, Apple Inc.)for the most recently two weeks using a free API provider named AlphaVantage and stores it in the DB)
It can be called as: 

    ```bash
    python get_raw_data.py
    ```

As the above mentioned code to run requires all the dependencies to be installed locally, a cleaner solution is to use the other file `get_raw_data_local.py` which single function is to execute a shell script from `get_data.sh`:

    ```bash
    python get_raw_data_local.py
    ```

This will execute the same code as in `get_raw_data.py` within the service environment leaving your local environment untouched.

3. [http://localhost:5000/docs](http://localhost:5000/docs) has the built-in documentation and aslo allows to test the APIs from **Task2** in a web interface.

Other specifications are as described in the original tasks description. 


# A description of how to maintain the API key to retrieve financial data from AlphaVantage in both local development and production environment

Development environment:

The API key to retrieve financial data from AlphaVantage and other secure information shall be kept in the `.env` file which shall not be added to the git repository.
Here the `.env` file is added to the repository intentionally for simplicity purpose.

Production environment:

The API key to retrieve financial data from AlphaVantage and other secure information shall be kept in the **environment variables** or **cloud key management services**; or using **configuration files** or **secrets management tools**.  


## Additional Notes:

1. Tests are not included.
2. Any feedback appreciated.