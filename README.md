## Overview

Data Query Expert is a Streamlit web application designed to help users convert natural language prompts into SQL queries and retrieve data from a MySQL database. The application leverages the LangChain library, specifically the Ollama language model, to interpret user prompts and generate corresponding SQL queries.

## Features

- **Natural Language to SQL Conversion**: Users can input their data-related tasks in natural language, and the application will generate the corresponding SQL query.
- **Database Query Execution**: The generated SQL query is executed on a MySQL database, and the results are displayed in a tabular format.

## Requirements

- Python 3.8+
- Streamlit
- mysql-connector-python
- langchain
- langchain_community

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/data-query-expert.git
    cd data-query-expert
    ```

2. **Install the required Python packages**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Set up the MySQL Database**:
    - Ensure you have MySQL installed and running.
    - Create a database named `Company` and a table named `employee` with the following structure:
      ```sql
      CREATE DATABASE Company;
      USE Company;
      
      CREATE TABLE employee (
          s_no INT PRIMARY KEY,
          name VARCHAR(30),
          dob DATE,
          joining_date DATE,
          salary DECIMAL(10, 2),
          department VARCHAR(25)
      );
      ```

4. **Run the Streamlit application**:
    ```sh
    streamlit run app.py
    ```

## Usage

1. **Open the application**: In your web browser, navigate to the URL provided by Streamlit (usually `http://localhost:8501`).
2. **Enter a prompt**: In the input box, type a natural language prompt describing the data query you want to perform.
3. **Extract Data**: Click the "Extract Data" button to generate and execute the SQL query.
4. **View Results**: The results of the query will be displayed in a table.

## Code Explanation

### 1. Prompt Template

The `data_analyst_template` defines the format for the language model prompt. It includes the database structure and instructs the model to generate SQL queries.

```python
data_analyst_template = """You are a data analyst. You are working on a database named Company, which has a table named employee and the table has the following columns,
s_no INT PRIMARY KEY,
name VARCHAR(30),
dob DATE,
joining_date DATE,
salary DECIMAL(10, 2),
department VARCHAR(25)

Your job is to perform the given task {prompt} by converting the prompt into sql queries.The result should be the sql query in single line string format excluding any sort of definition or explanation. 
Result: 
"""
```

### 2. PromptTemplate and LLMChain

We use `PromptTemplate` from LangChain to structure the prompt and `LLMChain` to invoke the language model.

```python
data_analyst_prompt_template = PromptTemplate(
    input_variables=["prompt"],
    template=data_analyst_template
)

gemma = Ollama(model="llama3")

llm_chain = LLMChain(llm=gemma, prompt=data_analyst_prompt_template)
```

### 3. Helper Functions

- `query_llm(prompt)`: Invokes the language model to generate the SQL query.
- `extract_sql_code(input_string)`: Cleans up the generated SQL query.
- `query_db(sql_query)`: Executes the SQL query on the MySQL database and returns the results.

```python
def query_llm(prompt):
    return llm_chain.invoke({"prompt":prompt})["text"]

def extract_sql_code(input_string):
    sql_code = input_string.replace("'''sql", "").replace("'''", "").strip()
    return sql_code

def query_db(sql_query):
    con = ms.connect(host="localhost", user="#####", password="####", database="Company")
    cursor = con.cursor()
    
    cursor.execute(sql_query)
    data = cursor.fetchall()
   
    cursor.close()
    con.close()
    return data
```

### 4. Streamlit App

The Streamlit app takes user input, processes it, and displays the query results.

```python
st.title("Data Query Expert")
user_input = st.text_input("Enter the Prompt....")

if st.button("Extract Data"):
    result = query_llm(user_input)
    sql_query = extract_sql_code(result)
    st.table(query_db(sql_query))
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

- [LangChain](https://www.langchain.com)
- [Streamlit](https://streamlit.io)
- [MySQL](https://www.mysql.com)
