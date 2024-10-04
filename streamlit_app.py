# streamlit_app.py

import streamlit as st
from api import clean_up_book_details  # Importing from api.py
from urls import generate_urls  # Importing from urls.py

# Initialize session state for inputs
if 'book_title' not in st.session_state:
    st.session_state['book_title'] = ""
if 'author' not in st.session_state:
    st.session_state['author'] = ""
if 'links_generated' not in st.session_state:
    st.session_state['links_generated'] = False

# Title and description
st.title('Bookworm 📚')
st.write("Enter the book title and/or author's name. We'll clean it up before generating search links.")

# Input fields
st.session_state['book_title'] = st.text_input("Book Title", value=st.session_state['book_title'])
st.session_state['author'] = st.text_input("Author", value=st.session_state['author'])

book_title = st.session_state['book_title']
author = st.session_state['author']

# Generate Links button logic
if not st.session_state['links_generated']:
    if st.button("Generate Links") and (book_title or author):
        cleaned_title, cleaned_author = clean_up_book_details(book_title, author)
        st.session_state['cleaned_title'] = cleaned_title
        st.session_state['cleaned_author'] = cleaned_author
        st.session_state['links_generated'] = True

# Display cleaned-up title and author
if st.session_state['links_generated']:
    st.markdown(f"**Cleaned Title**: {st.session_state['cleaned_title']}")
    st.markdown(f"**Cleaned Author**: {st.session_state['cleaned_author']}")

    # Generate and display URLs
    generate_urls(st.session_state['cleaned_title'], st.session_state['cleaned_author'])
