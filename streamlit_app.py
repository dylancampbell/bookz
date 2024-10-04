import streamlit as st
import requests
import urllib.parse

# Function to clean up author/title using Google Books API
def clean_up_book_details(book_title=None, author=None):
    # Construct the query string
    query = ""
    if book_title:
        query += f"intitle:{book_title}"
    if author:
        if query:
            query += "+"
        query += f"inauthor:{author}"

    # Retrieve the API key from Streamlit secrets
    api_key = st.secrets["google_books"]["api_key"]
    
    # Build the API request URL
    google_books_api = f"https://www.googleapis.com/books/v1/volumes?q={urllib.parse.quote(query)}&key={api_key}"
    
    try:
        # Make the API request
        response = requests.get(google_books_api)
        response.raise_for_status()  # Raises an error for bad status codes
        data = response.json()

        if 'items' in data and len(data['items']) > 0:
            # Extract cleaned-up title and author
            book_data = data['items'][0]['volumeInfo']
            cleaned_title = book_data.get('title', book_title)
            cleaned_author = ', '.join(book_data.get('authors', [author]))
            return cleaned_title, cleaned_author
        else:
            st.error("No matching books found.")
            return book_title, author

    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the Google Books API: {e}")
        return book_title, author

# Streamlit UI
st.title('Book Search App 📚')

# Input fields for book title and author
book_title = st.text_input("Book Title")
author = st.text_input("Author")

# Button to generate links
if st.button("Generate Links"):
    cleaned_title, cleaned_author = clean_up_book_details(book_title, author)
    st.write(f"Cleaned Title: {cleaned_title}")
    st.write(f"Cleaned Author: {cleaned_author}")
