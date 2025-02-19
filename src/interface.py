import json
import streamlit as st
import pandas as pd

from langchain_community.utilities import SQLDatabase;
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import os

from typing_extensions import Annotated


# def save_memory(memory: str, *, config: RunnableConfig, store: Annotated[BaseStore, InjectedStore()]) -> str:
#     '''Save the given memory for the current user.'''
#     # This is a **tool** the model can use to save memories to storage
#     user_id = config.get("configurable", {}).get("user_id")
#     namespace = ("memories", user_id)
#     store.put(namespace, f"memory_{len(store.search(namespace))}", {"data": memory})
#     return f"Saved memory: {memory}"
#
# def prepare_model_inputs(state: AgentState, config: RunnableConfig, store: BaseStore, system_message: str):
#     # Retrieve user memories and add them to the system message
#     # This function is called **every time** the model is prompted. It converts the state to a prompt
#     user_id = config.get("configurable", {}).get("user_id")
#     namespace = ("memories", user_id)
#     memories = [m.value["data"] for m in store.search(namespace)]
#     system_msg = f"User memories: {', '.join(memories)}"
#     return [{"role": "system", "content": system_msg}] + state["messages"]


def create_agent():
    load_dotenv()

    mysql_uri = 'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}'
    db = SQLDatabase.from_uri(
        mysql_uri.format(
            username=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASS"),
            host=os.getenv("MYSQL_HOST"),
            port=os.getenv("MYSQL_PORT"),
            database=os.getenv("MYSQL_DBNAME")
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

    # store = InMemoryStore()
    system_message = prompt_template.messages[0].format(dialect=db.dialect, top_k=10)
    agent = create_react_agent(llm, tools=tools, prompt=system_message)
    return agent

def query_agent(agent, query: str):
    question_template = """For the following query, if it requires drawing a table, reply as follows:
            {"table": {"columns": ["column1", "column2", ...], "data": [[value1, value2, ...], [value1, value2, ...], ...]}}

            If the query requires creating a bar chart, reply as follows:
            {"bar": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}

            If the query requires creating a line chart, reply as follows:
            {"line": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}

            There can only be two types of chart, "bar" and "line".

            If it is just asking a question that requires neither, reply as follows:
            {"answer": "answer"}
            Example:
            {"answer": "The title with the highest rating is 'Gilead'"}"
            If you do not know the answer, reply as follows:
            {"answer": "I do not know."}

            Return all output as a string.

            All strings in "columns" list and data list, should be in double quotes,

            For example: {"columns": ["title", "ratings_count"], "data": [["Gilead", 361], ["Spider's Web", 5164]]}

            Lets think step by step.

            Below is the query.
            Query:
            """
    question = question_template + query
    latest_message = None
    inputs = {"messages": [{"role": "user", "content": question}]}
    for step in agent.stream(inputs, stream_mode="updates"):
        if 'agent' in step:
            latest_message = step['agent']["messages"][-1].content
    print(latest_message)
    return latest_message


def decode_response(response : str) -> dict:
    return json.loads(response)

def write_response(response_dict: dict):
    """
    Write a response from an agent to a Streamlit app.

    Args:
        response_dict: The response from the agent.

    Returns:
        None.
    """

    # Check if the response is an answer.
    if "answer" in response_dict:
        st.write(response_dict["answer"])

    # Check if the response is a bar chart.
    if "bar" in response_dict:
        data = response_dict["bar"]
        df = pd.DataFrame(data["data"], columns=data["columns"])
        st.table(df)
        df = pd.DataFrame(data)
        df.set_index("columns", inplace=True)
        st.bar_chart(df)

    # Check if the response is a line chart.
    if "line" in response_dict:
        data = response_dict["line"]
        print("data: ")
        print(data)
        df1 = pd.DataFrame(data, columns=data["columns"])
        st.table(df1)
        df = pd.DataFrame(data["data"], columns=data["columns"])
        st.line_chart(df)

    # Check if the response is a table.
    if "table" in response_dict:
        data = response_dict["table"]
        df = pd.DataFrame(data["data"], columns=data["columns"])
        st.table(df)
        st.bar_chart(df, x=data["columns"][0], y=data["columns"][-1])

if "more_stuff" not in st.session_state:
    st.session_state.more_stuff = False
st.title("Chat with your database")
query = st.text_area("Ask a question")
agent = create_agent()
if st.button("Submit Query", type="primary"):
    print("Question: " + query)
    try:
        response = query_agent(agent=agent, query=query)
        decoded_response = decode_response(response)
        write_response(decoded_response)
    except Exception as e:
        st.write(repr(e))
