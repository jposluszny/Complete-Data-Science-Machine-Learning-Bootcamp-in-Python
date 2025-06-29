import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

@st.cache
def load_data(): 
    df = pd.read_csv('kiva_el.csv')
    return df

df = load_data()
def main():
    page = st.sidebar.selectbox("Select a Page", ["Homepage", "Scatter Plot",'Line Plot','Line Chart'])

    if page == "Homepage":
        st.header("Data Science App")
        st.write("Please select a page on the left.")
        st.table(df)
    elif page == "Scatter Plot":
        st.title("Scatter Plot")
        visualize_scatter()
    elif page == "Line Plot":
        st.title("Line Plot")
        visualize_line()
    elif page == "Line Chart":
        st.title("Line Chart")
        line_chart()



def visualize_scatter():
    sns.scatterplot(x='funded_amount',y='lender_count',data=df)
    st.pyplot()

def visualize_line():
    sns.lineplot(x='funded_amount',y='lender_count',data=df)
    st.pyplot()

def line_chart():
    st.line_chart(df[['lender_count']])
    
if __name__ == "__main__":
    main()