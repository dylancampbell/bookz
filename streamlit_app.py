import streamlit as st
import urllib.parse
import webbrowser

# Function to generate AbeBooks search URL
def generate_abebooks_url(book_title=None, author=None):
    base_url = "https://www.abebooks.com/servlet/SearchResults"
    query_params = {
        "an": author if author else "",  # Only include if provided
        "tn": book_title if book_title else "",  # Only include if provided
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
    
    # Combine both title and author if available, otherwise use whatever is provided
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
st.write("Fill in **either** the book title, the author's name, or both. We're not too picky! 😉")

# Input form
book_title = st.text_input("Book Title (Optional)")
author = st.text_input("Author (Optional)")

# Checkbox for opening all links in new tabs
open_all_tabs = st.checkbox("Open all links in new tabs")

# Perform search and display results when the button is clicked
if st.button("Search"):
    if book_title or author:
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

        # Open all links in new tabs if the user checks the box
        if open_all_tabs:
            webbrowser.open_new_tab(goodreads_url)
            webbrowser.open_new_tab(amazon_url)
            webbrowser.open_new_tab(abebooks_url)
            webbrowser.open_new_tab(libby_url)
    else:
        st.warning("Please enter at least the book title or the author’s name. You can't get away with leaving both empty! 😜")
