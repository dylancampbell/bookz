import streamlit as st
import urllib.parse

# Function to generate AbeBooks search URL
def generate_abebooks_url(book_title=None, author=None):
    base_url = "https://www.abebooks.com/servlet/SearchResults"
    query_params = {
        "an": author if author else "",
        "tn": book_title if book_title else "",
        "bi": 0,
        "bx": "off",
        "cm_sp": "SearchF-_-Advs-_-Result",
        "recentlyadded": "all",
        "sortby": 17
    }
    url = base_url + "?" + urllib.parse.urlencode(query_params)
    return url

# Function to generate Libby search URL
def generate_libby_url(book_title=None, author=None):
    base_url = "https://libbyapp.com/search/lapl/search/query-"
    search_query = f"{urllib.parse.quote(book_title)}%20{urllib.parse.quote(author)}" if book_title and author else urllib.parse.quote(book_title or author)
    url = base_url + search_query + "/page-1"
    return url

# Function to generate Goodreads search URL
def generate_goodreads_url(book_title=None, author=None):
    base_url = "https://www.goodreads.com/search"
    
    if book_title and author:
        query = f"{book_title} {author}"
    else:
        query = book_title or author

    query_params = {"q": query, "search_type": "books"}
    url = base_url + "?" + urllib.parse.urlencode(query_params)
    return url

# Function to generate Amazon search URL
def generate_amazon_url(book_title=None, author=None):
    base_url = "https://www.amazon.com/s"
    query = f"{book_title} {author}" if book_title and author else book_title or author
    query_params = {"k": query}
    url = base_url + "?" + urllib.parse.urlencode(query_params)
    return url

# Streamlit UI
st.title('Book Search App 📚')
st.write("Fill in **either** the book title, the author's name, or both. Then click the button for the platform you'd like to search.")

# Input form
book_title = st.text_input("Book Title (Optional)")
author = st.text_input("Author (Optional)")

# Only show the buttons when either title or author is provided
if book_title or author:
    # Generate URLs for each platform
    abebooks_url = generate_abebooks_url(book_title, author)
    libby_url = generate_libby_url(book_title, author)
    goodreads_url = generate_goodreads_url(book_title, author)
    amazon_url = generate_amazon_url(book_title, author)

    # Create clickable links styled as buttons for each platform
    st.markdown(f"""
        <style>
        .button {{
            display: inline-block;
            padding: 0.5em 1em;
            text-decoration: none;
            color: white;
            background-color: #007bff;
            border-radius: 5px;
        }}
        </style>
        <a href="{goodreads_url}" target="_blank" class="button">Search on Goodreads</a>
        <a href="{amazon_url}" target="_blank" class="button">Search on Amazon</a>
        <a href="{abebooks_url}" target="_blank" class="button">Search on AbeBooks</a>
        <a href="{libby_url}" target="_blank" class="button">Search on Libby</a>
    """, unsafe_allow_html=True)
else:
    st.warning("Please enter at least the book title or the author’s name to generate search links.")
