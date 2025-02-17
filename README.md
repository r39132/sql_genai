# Play_With_LLM_SQL

play_with_llm_sql is a simple Python library to understand the langgraph sql agent that interact with relational databases.

## Installation

### MySQL
1. This project uses a local instance of [MySQL](https://dev.mysql.com/downloads/installer/) as the relational database. Download the appropriate installer and follow instructions to create a user and password.
2. Create a ```.env``` file in the project and add the following values:
```
MYSQL_USER=
MYSQL_PASS=
MYSQL_HOST=
MYSQL_PORT=
```
By default, most MySQL installers will have the following values:
```MYSQL_HOST=localhost```, ```MYSQL_PORT=3306```,  ```MYSQL_USER=root```. During the installation, you will be prompted to create a password.

3. Chinook is a popular test database that is available online. You can [download](https://github.com/lerocha/chinook-database/releases) the latest version of the database script or use the sql file that is available in this project.
To import the schema and data into the database run the following command within the mysql shell.

```mysql
source Chinook_MySql.sql
```
Now, you have the database up and running. Moving on to the python environment:

### Python
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required packages.


```bash
pip install -r requirements.txt
```

## Usage
This project has the following components:
1. SQL Query Agent available in a Jupyter notebook, where each cell can be executed in a sequence. This provides more detailed interactions with the SQL agent
2. SQL Quert Agent integrated into streamlit web app, which can be run using the following command:
```bash
streamlit run interface.py
```
3. SQL DML Agent that is able to insert data into the database. This is also available as a jupyter notebook

## Next Steps
The langgraph agent used here is a prebuilt agent. The next step would be to create an agent from scratch and replace the prebuilt agent. Also, use streamlit to create a more interactive chat interface with context to allow the user to ask questions based on the response of the SQL agent.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)