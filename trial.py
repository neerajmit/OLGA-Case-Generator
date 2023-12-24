import streamlit as st
import pandas as pd

def generate_and_download_file():
    # Replace this function with your logic to generate data
    data = {'Column1': [1, 2, 3], 'Column2': ['A', 'B', 'C']}
    df = pd.DataFrame(data)

    # Save the DataFrame to a text file
    file_path = "generated_file.txt"
    df.to_csv(file_path, sep='\t', index=False)

    # Trigger download
    st.download_button(
        label="Download File",
        data=file_path,
        file_name="generated_file.txt",
        key="download_button"
    )

def main():
    st.title("File Download Button Example")

    # Your app content here...

    # Create a button to generate and download the file
    if st.button("Generate and Download File"):
        generate_and_download_file()

if __name__ == "__main__":
    main()
