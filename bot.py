from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
from langchain.chains import LLMChain
import mysql.connector as ms
import streamlit as st


data_analyst_template = """You are a data analyst. You are working on a database named Company, which has a table named employee and the table has the following columns,s_no INT PRIMARY KEY,
    name VARCHAR(30),
    dob DATE,
   joining_date DATE,
   salary DECIMAL(10, 2),
   department VARCHAR(25)

    \n Your job is to perform the given task {prompt} by converting the prompt into sql queries.The result should be the sql query in single line string format excluding any sort of definition or explanation. 
    Result: 
    """

data_analyst_prompt_template = PromptTemplate(
    input_variables=["prompt"],
    template=data_analyst_template
)

gemma = Ollama(model="llama3")

llm_chain = LLMChain(llm=gemma,prompt=data_analyst_prompt_template)

def query_llm(prompt):
    return llm_chain.invoke({"prompt":prompt})["text"]

def extract_sql_code(input_string):
    sql_code = input_string.replace("'''sql", "").replace("'''", "").strip()
    return sql_code

def query_db(sql_query):
    con = ms.connect(host="localhost",user="####",password="####",database="Company")
    cursor = con.cursor()
    
    cursor.execute(sql_query)
    data = cursor.fetchall()
   
    cursor.close()
    con.close()
    return data
st.title("Data Query Expert")
user_input = st.text_input("Enter the Prompt....")

if st.button("Extract Data"):
    result = query_llm(user_input)
    sql_query = extract_sql_code(result)
    st.table(query_db(sql_query))
