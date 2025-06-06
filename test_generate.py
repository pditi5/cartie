from cohere_utils import generate_sql_query


question = "Which employees work at the Mumbai branch?"

sql = generate_sql_query(question)

print("User Question:" , question)
print("Generated SQL:", sql)