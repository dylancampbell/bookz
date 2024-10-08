import streamlit as st
import requests
import urllib.parse

def clean_up_book_details(book_title=None, author=None):
    query = ""
    if book_title:
        query += f"intitle:{book_title}"
    if author:
        if query:
            query += "+"
        query += f"inauthor:{author}"

    # Retrieve API key securely from Streamlit secrets
    api_key = st.secrets["google_books"]["api_key"]
    google_books_api = f"https://www.googleapis.com/books/v1/volumes?q={urllib.parse.quote(query)}&key={api_key}"

    try:
        # Make the API request
        response = requests.get(google_books_api)
        response.raise_for_status()  # Raises error for bad status codes
        data = response.json()

        if 'items' in data and len(data['items']) > 0:
            book_data = data['items'][0]['volumeInfo']
            cleaned_title = book_data.get('title', book_title)
            cleaned_author = ', '.join(book_data.get('authors', [author])) if book_title else author
            return cleaned_title, cleaned_author
        else:
            st.error("No matching books found.")
            return book_title, author

    except requests.exceptions.RequestException as e:
        # User-friendly error message
        st.error("Error connecting to the Google Books API. Please try again later.")
        # Log the error without exposing sensitive information
        print(f"API request failed: {e}")
        return book_title, author
