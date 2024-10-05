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

# Initialize previous inputs to track changes
if 'previous_title' not in st.session_state:
    st.session_state['previous_title'] = ""
if 'previous_author' not in st.session_state:
    st.session_state['previous_author'] = ""

# Title and description
st.title('Bookworm 📚')
st.write("Enter the book title and/or author's name. We'll clean it up before generating search links.")

# Checkbox to toggle Google API ping
use_google_api = st.checkbox("Use Google Books API to clean up title and author?", value=False)

# Input fields
st.session_state['book_title'] = st.text_input("Book Title", value=st.session_state['book_title'])
st.session_state['author'] = st.text_input("Author", value=st.session_state['author'])

book_title = st.session_state['book_title']
author = st.session_state['author']

# Check if the user has changed the input text
if book_title != st.session_state['previous_title'] or author != st.session_state['previous_author']:
    st.session_state['links_generated'] = False  # Reset links if inputs change
    st.session_state['previous_title'] = book_title  # Update the previous title
    st.session_state['previous_author'] = author  # Update the previous author

# Generate Links button logic
if not st.session_state['links_generated']:
    if st.button("Generate Links") and (book_title or author):
        if use_google_api:
            cleaned_title, cleaned_author = clean_up_book_details(book_title, author)
        else:
            cleaned_title, cleaned_author = book_title, author  # Use raw inputs if Google API is off

        st.session_state['cleaned_title'] = cleaned_title
        st.session_state['cleaned_author'] = cleaned_author
        st.session_state['links_generated'] = True

# Only display cleaned title/author if Google API was used
if st.session_state['links_generated']:
    if use_google_api:
        st.markdown(f"**Cleaned Title**: {st.session_state['cleaned_title']}")
        st.markdown(f"**Cleaned Author**: {st.session_state['cleaned_author']}")

    # Column Headers
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<h3 style='text-align: center;'>Rate</h3>", unsafe_allow_html=True)
    with col2:
        st.markdown("<h3 style='text-align: center;'>Borrow</h3>", unsafe_allow_html=True)
    with col3:
        st.markdown("<h3 style='text-align: center;'>Buy</h3>", unsafe_allow_html=True)

    # Generate and display URLs
    generate_urls(st.session_state['cleaned_title'], st.session_state['cleaned_author'])

st.markdown("""
    <style>
    .button {
        display: inline-block;
        padding: 10px 20px;
        margin: 10px auto;  /* Center button horizontally */
        font-size: 16px;
        color: white !important;  /* Ensure button text is white */
        text-align: center;
        text-decoration: none;
        border-radius: 8px;
        width: 200px;  /* You can adjust the width of the buttons as needed */
    }
    .goodreads { background-color: #D7A168; }
    .amazon { background-color: #FF9900; }
    .abebooks { background-color: #CC3333; }
    .libby { background-color: #8E5A9E; }
    .lapl { background-color: #003C71; }
    .bookshop { background-color: #017AFF; }
    .storygraph { background-color: #5B21B6; }
    </style>
""", unsafe_allow_html=True)

