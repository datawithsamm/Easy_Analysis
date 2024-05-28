import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from stats.univariate import univariate
from stats.overview import overview
from stats.bivariate import bivariate

def main():
    st.set_page_config(page_title="Data Analysis")
    st.title("Data Analysis")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        # Dataframe section
        with st.expander("Dataframe", expanded=False):
            st.write("Dataframe:")
            st.write(df.head())

        # Overview section (baru ada missing nanti di update)
        with st.expander("Overview", expanded=False):
            st.write("Overview of Features with Missing Values:")
            missing_df = overview(df)
            st.write(missing_df)

        # Univariate Analysis section
        with st.expander("Univariate Analysis", expanded=False):
            st.write("Univariate Analysis Result:")
            output_df = univariate(df)
            st.write(output_df)

        with st.expander("Visualizations", expanded=False):
            st.write("Univariate Visualizations:")
            columns = st.columns(5)
            for i, col in enumerate(df.columns):
                with columns[i % 5]:
                    plt.figure()
                    if pd.api.types.is_numeric_dtype(df[col]):
                        sns.histplot(data=df, x=col)
                    else:
                        sns.countplot(data=df, x=col)
                    st.pyplot(plt.gcf())
                    plt.close()

        # Bivariate Analysis section
        with st.expander("Bivariate Analysis", expanded=False):
            st.write("Bivariate Analysis Result:")
            label_column = st.selectbox("Select a label column", df.columns)
            bivariate_df = bivariate(df, label_column)
            st.write(bivariate_df)                

if __name__ == "__main__":
    main()