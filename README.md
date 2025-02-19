<!--
 Licensed to the Apache Software Foundation (ASF) under one
 or more contributor license agreements.  See the NOTICE file
 distributed with this work for additional information
 regarding copyright ownership.  The ASF licenses this file
 to you under the Apache License, Version 2.0 (the
 "License"); you may not use this file except in compliance
 with the License.  You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing,
 software distributed under the License is distributed on an
 "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 KIND, either express or implied.  See the License for the
 specific language governing permissions and limitations
 under the License.
-->
[![License](https://img.shields.io/:license-Apache%202-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0.txt)

# SQL GenAI

SQL GenAI is a simple Python library to understand the langgraph sql agent that interact with relational databases.

----

## Installation & Setup
1. __Install a Database__
    1. For the purposes of this demo, I used MySQL, though any database supported by [SQLAlchemy](https://docs.sqlalchemy.org/en/20/dialects/) will work!
        1. if running on Mac, [Homebrew is a good option for installing MySQL](https://formulae.brew.sh/formula/mysql).
1.  __Set up Local Project__
    1. To clone the repo on your local machine and set up a [virtual env](https://docs.python.org/3/library/venv.html), follow these steps:
    1. Create a `.env` file to hold the following DB connection params
    ```bash
      gh repo clone r39132/sql_genai
      cd sql_genai
      python -m venv sql_genai_env
      source sql_genai_env/bin/activate
      pip install --upgrade pip
      pip install -r requirements.txt
    ```
1. __Create a `.env` file to hold the following DB connection params__  
    ```
      MYSQL_USER=root
      MYSQL_PASS=password
      MYSQL_HOST=localhost
      MYSQL_PORT=3306
      MYSQL_DBNAME=Chinook
    ```

4. __Load a demo dataset into MySQL__
    1. For demo purposes, I used [Chinook](https://github.com/lerocha/chinook-database), a popular dataset referenced in langchain demos. I have already downloaded a [release](https://github.com/lerocha/chinook-database/releases) for MySQL to this repo.
    1. Log into MySQL
        ```bash
          mysql -u root -p
        ```
    1. To import the dataset (i.e., schema and data( into the database run the following command within the MySQL shell.
        ```mysql
          source Chinook_MySql.sql
        ```
----

## Usage
This project has the following components:
1. SQL Query Agent available in a Jupyter notebook, where each cell can be executed in a sequence. This provides more detailed interactions with the SQL agent
1. SQL Query Agent integrated into streamlit web app, which can be run using the following command:
    ```bash
      streamlit run src/interface.py
    ```
1. SQL DML Agent that is able to insert data into the database. This is also available as a jupyter notebook

## Next Steps
1. Update project to be more interfactive and create a more interactive chat interface with context to allow the user to ask questions based on the response of the SQL agent.

