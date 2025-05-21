import streamlit as st
import pacuare
from dotenv import load_dotenv
import os

load_dotenv()

db = pacuare.Client(os.getenv("PACUARE_API_KEY"))

def get_data():
  return (
    db
    .query("select injuries, turtle_occurrences from unique_turtles")
    .apply(
      lambda row: {**row, 'n_injuries': len(row['injuries'].split(','))},
      axis=1,
      result_type='expand'
    )
  )

st.title("🎈 Pacuare API Demo")
st.write(
    "See below a scatter plot of turtle occurrences vs. injuries."
)

st.scatter_chart(
  data=get_data(),
  x='turtle_occurrences',
  y='n_injuries'
)