import streamlit as st
import os
from cohere_utils import generate_sql_query, generate_natural_language_response
from db_test import run_sql_query

# streamlit page config
st.set_page_config(page_title="Cartie", layout="centered")

# app title and description 
st.title("Cartie")
st.markdown("Ask anything ✨ Cartie knows your data's story.")

# input box for user query 
question = st.text_input("Ask a question", placeholder="What is the name of Client ID 102?")

# button to trigger query processing  
if st.button("Generative Answer"):
    if not question.strip():
        st.warning("Please enter a valid question.")
    else:
        try:
            # step 1: generate sql from question using cohere
            with st.spinner("Generating SQL with Cohere..."):
                sql_query = generate_sql_query(question)
            
            # Show the generated SQL in an expander (collapsed by default)
            with st.expander("View Generated SQL Query"):
                st.code(sql_query, language="sql")
                       
            # step 2: running the sql query on the database
            with st.spinner("Fetching results from database..."):
                results = run_sql_query(sql_query)
            
            # step 3: showing the results
            if results:
                st.success("Query executed Successfully !!")
                
                # step 4: generate natural language response
                with st.spinner("Generating natural language response..."):
                    natural_response = generate_natural_language_response(question, sql_query, results)
                
                # Display the natural language answer prominently
                st.markdown("### Answer:")
                st.markdown(f"**{natural_response}**")
                
                # Show raw data in an expander
                with st.expander("View Raw Data"):
                    st.dataframe(results)
                    
            else:
                st.info("No results were found for your query.")
                
        except Exception as e:
            st.error(f"Failed to process your question:\n{str(e)}")
            
st.markdown("---")

# Add some example questions
st.markdown("### Example Questions to Try:")
example_questions = [
    "What is the name of Client ID 102?",
    "How many employees work in each branch?",
    "Who are the highest paid employees?",
    "Which clients have the highest total sales?",
    "What are all the branch names?",
    "Show me employee details for branch 1"
]

cols = st.columns(2)
for i, example in enumerate(example_questions):
    col = cols[i % 2]
    if col.button(example, key=f"example_{i}"):
        st.rerun()

st.caption("Built with Streamlit, Cohere & MySQL | ©2025 TMLC")