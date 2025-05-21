import streamlit as st
import pacuare

db = pacuare.Client(st.secrets["PACUARE_API_KEY"])

def get_data(id):
  sql = "select injuries, turtle_occurrences from unique_turtles where turtle_id = $1"
  params = [id]
  if id == '' or id is None:
    sql = "select injuries, turtle_occurrences from unique_turtles"
    params = []
  return (
    db.query(sql, params)
    .apply(
      lambda row: {
        **row, 
        'n_injuries': len(
          [injury for injury in row['injuries'].split(',') if injury.strip() != '']
        )
      },
      axis=1,
      result_type='expand'
    )
  )

st.title("🎈 Pacuare API Demo")
st.write(
    "See below a scatter plot of turtle occurrences vs. injuries."
)

turtle_id = st.text_input("Turtle ID")

st.scatter_chart(
  data=get_data(turtle_id),
  x='turtle_occurrences',
  y='n_injuries'
)