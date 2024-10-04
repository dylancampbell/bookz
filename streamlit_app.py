import streamlit as st
import requests
from bs4 import BeautifulSoup

# Function to search Goodreads with better error handling and header
def search_goodreads(book_title, author):
    try:
        search_url = f"https://www.goodreads.com/search?q={book_title}+{author}&search_type=books"
        response = requests.get(search_url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.content, 'html.parser')

        # Debugging output
        st.write("Goodreads HTML content (truncated):", soup.prettify()[:500])

        # Find the first result link (improved)
        result = soup.find("a", class_="bookTitle")
        if result:
            link = "https://www.goodreads.com" + result['href']
            return link
    except Exception as e:
        st.error(f"Goodreads search failed: {e}")
    return None

# Function to search Amazon with better error handling and user-agent
def search_amazon(book_title, author):
    try:
        search_url = f"https://www.amazon.com/s?k={book_title}+{author}"
        response = requests.get(search_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
        soup = BeautifulSoup(response.content, 'html.parser')

        # Debugging output
        st.write("Amazon HTML content (truncated):", soup.prettify()[:500])

        # Find the first product link
        result = soup.find("a", class_="a-link-normal a-text-normal")
        if result:
            link = "https://www.amazon.com" + result['href']
            return link
    except Exception as e:
        st.error(f"Amazon search failed: {e}")
    return None

# Function to search AbeBooks with better error handling
def search_abebooks(book_title, author):
    try:
        search_url = f"https://www.abebooks.com/servlet/SearchResults?sts=t&tn={book_title}&an={author}"
        response = requests.get(search_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Debugging output
        st.write("AbeBooks HTML content (truncated):", soup.prettify()[:500])

        # Find the first result link
        result = soup.find("a", class_="result-link")
        if result:
            link = result['href']
            return link
    except Exception as e:
        st.error(f"AbeBooks search failed: {e}")
    return None

# Function to search Libby (direct link to library search)
def search_libby():
    return "https://libbyapp.com/library"

# Streamlit UI
st.title('Book Search App')
st.write('Enter a book title and author to find its pages on various platforms.')

# Input form
book_title = st.text_input("Book Title")
author = st.text_input("Author")

# Perform search and display results when the button is clicked
if st.button("Search"):
    if book_title and author:
        st.write(f"Searching for '{book_title}' by {author}...")

        # Perform searches
        goodreads_link = search_goodreads(book_title, author)
        amazon_link = search_amazon(book_title, author)
        abebooks_link = search_abebooks(book_title, author)
        libby_link = search_libby()

        # Display the results
        st.subheader("Results:")
        if goodreads_link:
            st.markdown(f"[Goodreads]({goodreads_link})")
        else:
            st.write("Goodreads page not found.")

        if amazon_link:
            st.markdown(f"[Amazon]({amazon_link})")
        else:
            st.write("Amazon page not found.")

        if abebooks_link:
            st.markdown(f"[AbeBooks]({abebooks_link})")
        else:
            st.write("AbeBooks page not found.")

        if libby_link:
            st.markdown(f"[Libby]({libby_link})")
    else:
        st.warning("Please enter both the book title and author.")
