import streamlit as st
import pandas as pd
import time
import webbrowser
from geutils import DataQuality

def main():
    # Set the app title
    st.title("Data Quality APP")

    # Step 4: Implement the app components
    # Select the data source
    data_source = st.selectbox("Select the data source", ["", "california_housing_test.csv", "dataset1.csv", "dataset2.csv", "dataset3.csv"])

    DQ_APP = None  # Initialize DQ_APP object

    checks_input = None  # Initialize checks_input variable
    if data_source:
        # Display a preview of the data
        st.subheader("Preview of the data:")
        data = pd.read_csv(f"great_expectations/data/{data_source}")
        st.write(data.head())

        if DQ_APP is None:  # Create DQ_APP object if not already created
            DQ_APP = DataQuality(data_source, data)
        # Perform data quality checks
        st.subheader("Perform Data Quality Checks")

        checks_input = st.text_area("Describe the checks you want to perform")

        # Button to get started
        if checks_input:
            submit_button = st.button("Submit")
            if submit_button:
                with st.spinner('Running your data quality checks'):
                    time.sleep(5)
                    expectation_result = DQ_APP.run_checks(checks_input)
                    st.success('Your test has successfully been run! Get results')

                    with st.expander("Show Results"):
                        st.subheader("Data Quality Checkpoint result")
                        st.write(expectation_result)

            open_docs_button = st.button("Open Data Docs")
            if open_docs_button:
                st.write("Open button clicked")
                #DQ_APP.get_data_docs()

                # Get the URL to the Data Docs
                data_docs_url = DQ_APP.context.get_docs_sites_urls()[0]['site_url']
                st.write(data_docs_url)

                # Open the URL in the browser
                webbrowser.open_new_tab(data_docs_url)

# Run the app
if __name__ == "__main__":
    main()
