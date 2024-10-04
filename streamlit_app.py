import streamlit as st
import urllib.parse

# Function to generate AbeBooks search URL
def generate_abebooks_url(book_title, author):
    base_url = "https://www.abebooks.com/servlet/SearchResults"
    query_params = {
        "an": author,
        "tn": book_title,
        "bi": 0,
        "bx": "off",
        "cm_sp": "SearchF-_-Advs-_-Result",
        "recentlyadded": "all",
        "sortby": 17
    }
    url = base_url + "?" + urllib.parse.urlencode(query_params)
    return url

# Function to generate Libby search URL
def generate_libby_url(book_title, author):
    base_url = "https://libbyapp.com/search/lapl/search/query-"
    search_query = f"{urllib.parse.quote(book_title)}%20{urllib.parse.quote(author)}"
    url = base_url + search_query + "/page-1"
    return url

# Function to generate Goodreads search URL
def generate_goodreads_url(book_title, author):
    base_url = "https://www.goodreads.com/search"
    query_params = {
        "q": f"{book_title} {author}",
        "search_type": "books"
    }
    url = base_url + "?" + urllib.parse.urlencode(query_params)
    return url

# Function to generate Amazon search URL
def generate_amazon_url(book_title, author):
    base_url = "https://www.amazon.com/s"
    query_params = {
        "k": f"{book_title} {author}"
    }
    url = base_url + "?" + urllib.parse.urlencode(query_params)
    return url

# Streamlit UI
st.title('Book Search App')
st.write('Enter a book title and author to generate search links for various platforms.')

# Input form
book_title = st.text_input("Book Title")
author = st.text_input("Author")

# Perform search and display results when the button is clicked
if st.button("Search"):
    if book_title and author:
        st.write(f"Searching for '{book_title}' by {author}...")

        # Generate URLs for each platform
        abebooks_url = generate_abebooks_url(book_title, author)
        libby_url = generate_libby_url(book_title, author)
        goodreads_url = generate_goodreads_url(book_title, author)
        amazon_url = generate_amazon_url(book_title, author)

        # Display the search result links
        st.subheader("Results:")
        st.markdown(f"[Goodreads]({goodreads_url})")
        st.markdown(f"[Amazon]({amazon_url})")
        st.markdown(f"[AbeBooks]({abebooks_url})")
        st.markdown(f"[Libby]({libby_url})")
    else:
        st.warning("Please enter both the book title and author.")
