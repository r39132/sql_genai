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
      OPENAI_API_KEY=<create your key on https://platform.openai.com/api-keys>
    ```

4. __Load a demo dataset into MySQL__
    1. For demo purposes, I used [Chinook](https://github.com/lerocha/chinook-database), a popular dataset referenced in langchain demos. I have already downloaded a [release](https://github.com/lerocha/chinook-database/releases) for MySQL to this repo.
    2. The data set has artists, albums, tracks, and invoices, customers, and employees for stores selling albums.
    1. Log into MySQL
        ```bash
          mysql -u root -p
        ```
    1. To import the dataset (i.e., schema and data( into the database run the following command within the MySQL shell.
        ```mysql
          source Chinook_MySql.sql
        ```
    1. __Datamodel__ 
        ![image](https://github.com/user-attachments/assets/e7c28796-10bf-4e66-a2c4-200fe9705c70)


----

## Usage
This project has the 3 components:
### 1. Text-to-SQL Agent with Web Interface
This Agent uses the [SQLDatabase Toolkit](https://python.langchain.com/docs/integrations/tools/sql_database/) to
1. Understand the database tables and their schemas (i.e. structure)
2. Reason about which tables and columns can answer the query!
3. Convert user natural language prompts into SQL queries!
4. Executes the query!
5. Return results in natural language, displaying results as a table and graph!
    
 To play with the Web UI, run
    ```bash
      streamlit run src/interface.py
    ```

Here are some screenshots showing interactions with the Text-to-SQL agent:
<img width="634" alt="Screenshot 2025-02-18 at 10 47 45 PM" src="https://github.com/user-attachments/assets/9493cb6a-158b-4b28-98c7-7b831521b623" />
<img width="620" alt="Screenshot 2025-02-18 at 10 06 56 PM" src="https://github.com/user-attachments/assets/3107c761-4b97-4730-ae7c-711754a342d5" />
<img width="605" alt="Screenshot 2025-02-18 at 10 25 06 PM" src="https://github.com/user-attachments/assets/30c766df-e772-48bf-8266-46ab01fcf48c" />
<img width="618" alt="Screenshot 2025-02-18 at 10 27 33 PM" src="https://github.com/user-attachments/assets/b92bb371-c202-461d-93dd-09cf3bef80ea" />
<img width="598" alt="Screenshot 2025-02-18 at 10 31 32 PM" src="https://github.com/user-attachments/assets/d14bd744-57a7-426e-a02b-c0350469ba0b" />
<img width="641" alt="Screenshot 2025-02-18 at 10 34 05 PM" src="https://github.com/user-attachments/assets/c51a84ea-139f-4a9d-bf24-4418838bcc37" />


### 2. Text-to-SQL Agent via Python Notebook
SQL Query Agent available in a Jupyter notebook, where each cell can be executed in a sequence. 

### 3. Text-to-SQL Chatbot via Python Notebook
SQL Query Chatbot available in a Jupyter notebook, where each cell can be executed in a sequence. 

### 4. DDL to populate tables with dummy Python Notebook
SQL DDL Agent available in a Jupyter notebook to add dummy data to existing tables.

## Next Steps
1. Update project remember context across prompts

