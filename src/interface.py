import json
import traceback
import streamlit as st
import pandas as pd

from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import os

def create_agent(debug: bool = False):
    mysql_uri = 'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}'

    db = SQLDatabase.from_uri(
        mysql_uri.format(
            username=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASS"),
            host=os.getenv("MYSQL_HOST"),
            port=os.getenv("MYSQL_PORT"),
            database=os.getenv("MYSQL_DBNAME"),
        )
    )

    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)

    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    tools = toolkit.get_tools()

    from langchain import hub

    prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")
    assert len(prompt_template.messages) == 1

    system_message = prompt_template.messages[0].format(dialect=db.dialect, top_k=10)
    if debug:
        prompt_template.messages[0].pretty_print()

    agent = create_react_agent(llm, tools=tools, prompt=system_message)
    return agent


def query_agent(agent, query: str, debug: bool = False):
    question_template = """ For the following query, respond as follows: 
            If the query returns a column that has numbers, place that column last in the response. 
            If it requires drawing a table, reply as follows:
            {"table": {"columns": ["column1", "column2", ...], "data": [[value1, value2, ...], [value1, value2, ...], ...]}}

            If it is just asking a question that requires neither, reply as follows:
            {"answer": "answer"}
            Example:
            {"answer": "The title with the highest rating is 'Gilead'"}"
            If you do not know the answer, reply as follows:
            {"answer": "I do not know."}
            if the query asks for a column that does not exist, reply as follows: 
            {"answer": "Column does not exist."}

            Return all output as a string.

            All strings in "columns" list and data list, should be in double quotes, 

            For example: {"columns": ["title", "ratings_count"], "data": [["Gilead", 361], ["Spider's Web", 5164]]}

            Lets think step by step.

            Below is the query.
            Query:
            """
    question = question_template + query
    if debug:
        print(question)
    latest_message = None
    inputs = {"messages": [{"role": "user", "content": question}]}
    for step in agent.stream(inputs, stream_mode="updates"):
        if 'agent' in step:
            if debug:
                print(step['agent']["messages"][-1])
            latest_message = step['agent']["messages"][-1].content
    if debug:
        print(latest_message)
    return latest_message


def decode_response(response: str) -> dict:
    return json.loads(response)


def write_response(response_dict: dict):

    if "answer" in response_dict:
        st.write(response_dict["answer"])

    # Check if the response is a table.
    if "table" in response_dict:
        data = response_dict["table"]
        df = pd.DataFrame(data["data"], columns=data["columns"])
        print(df)
        st.table(df)
        if df.dtypes[df.columns[-1]] in ["int64", "float64"]:
            if len(df.columns) > 2:
                merged_column = df[df.columns[:-1]].apply(
                    lambda x: ','.join(x.astype(str)),
                    axis=1
                )
                df.insert(0, ",".join(data["columns"][0:-1]), merged_column)
                print(df)
                st.bar_chart(df, x=",".join(data["columns"][0:-1]), y=data["columns"][-1])
                st.line_chart(df, x=",".join(data["columns"][0:-1]), y=data["columns"][-1])
            elif len(df.columns) == 2:
                st.bar_chart(df, x=data["columns"][0], y=data["columns"][1])
                st.line_chart(df, x=data["columns"][0], y=data["columns"][1])

if __name__ == "__main__":
    load_dotenv()
    debug = False
    print(os.getenv("DEBUG"))
    debug = os.getenv("DEBUG", False)
    print(debug)
    st.title("Chat with your database")
    query = st.text_area("Ask a question")
    agent = create_agent(debug)
    if st.button("Submit Query", type="primary"):
        print("Question: " + query)
        try:
            response = query_agent(agent=agent, query=query, debug=debug)
            decoded_response = decode_response(response)
            write_response(decoded_response)
        except Exception as e:
            if debug:
                print(traceback.format_exc())
            st.write(repr(e))
