import streamlit as st
import pandas as pd
from olga_file_generator import process_data
import csv

def main():
    st.title("File Generator App")

    # Upload file
    uploaded_file = st.file_uploader("Upload .opi File", type=["opi"])

    st.header("Enter Details")
    year = st.text_input("Year", key='2')
    diameter = st.text_input("Diameter", key='3')
    wgr = st.text_input("WGR", key='4')
    cgr = st.text_input("CGR", key='5')
    neq = st.text_input("NEQUIPIPE", key='6')
        
    colA, colB, colC= st.columns(3)
    with colB:
        st.markdown("<p style='text-align:center;'><br></p>", unsafe_allow_html=True)
        if st.button("Generate File"):
            if uploaded_file is not None:
                # Process data using backend logic
                processed_data = process_data(uploaded_file, year, diameter, wgr, cgr, neq)

                # Download the processed data as a CSV file
                csv_data = processed_data.to_csv(sep='\t', index=False, quoting=csv.QUOTE_NONE, header=False).encode("utf-8")
                #st.write("Working till here!!")
                st.download_button(
                    label="Download File",
                    data=csv_data,
                    file_name="olga_case_file.genkey",
                    key="download_button"
                )

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.write(e)

