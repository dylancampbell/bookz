import streamlit as st
import urllib.parse
import json

# --- URL GENERATION FUNCTIONS ---

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

# Function to generate Bookshop.org search URL
def generate_bookshop_url(book_title=None, author=None):
    base_url = "https://bookshop.org/books"
    query_params = {"keywords": f"{book_title} {author}"}
    url = base_url + "?" + urllib.parse.urlencode(query_params)
    return url

# Function to generate StoryGraph search URL
def generate_storygraph_url(book_title=None, author=None):
    base_url = "https://app.thestorygraph.com/browse"
    query_params = {"search_term": f"{book_title} {author}"}
    url = base_url + "?" + urllib.parse.urlencode(query_params)
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

# Function to generate LAPL search URL
def generate_lapl_url(book_title=None, author=None):
    base_url = "https://ls2pac.lapl.org/?section=search"
    if book_title and author:
        search_data = {
            "isAnd": True,
            "searchTokens": [
                {"searchString": author, "type": "Contains", "field": "Author"},
                {"searchString": book_title, "type": "Contains", "field": "Title"}
            ]
        }
    elif book_title:
        search_data = {
            "isAnd": True,
            "searchTokens": [{"searchString": book_title, "type": "Contains", "field": "Title"}]
        }
    else:
        search_data = {
            "isAnd": True,
            "searchTokens": [{"searchString": author, "type": "Contains", "field": "Author"}]
        }

    search_query = urllib.parse.quote(json.dumps(search_data))
    url = f"{base_url}&term={search_query}&page=0&pageSize=10&sortKey=Relevancy&db=ls2pac"
    return url

# --- STREAMLIT UI ---

# Title and description
st.title('Book Search App 📚')
st.write("Fill in **either** the book title, the author's name, or both. Then click 'Generate Links' to create buttons for each platform.")

# Input fields for book title and author
book_title = st.text_input("Book Title")
author = st.text_input("Author")

# Session state to track whether links have been generated
if 'links_generated' not in st.session_state:
    st.session_state['links_generated'] = False

# Reset the state if the user changes the input fields
if book_title != st.session_state.get('previous_title') or author != st.session_state.get('previous_author'):
    st.session_state['links_generated'] = False

# Store the current values for comparison on the next run
st.session_state['previous_title'] = book_title
st.session_state['previous_author'] = author

# Button to generate links
if not st.session_state['links_generated']:
    if st.button("Generate Links") and (book_title or author):
        st.session_state['links_generated'] = True

# Generate URLs and buttons if links are generated
if st.session_state['links_generated']:
    # Generate URLs for each platform
    abebooks_url = generate_abebooks_url(book_title, author)
    bookshop_url = generate_bookshop_url(book_title, author)
    storygraph_url = generate_storygraph_url(book_title, author)
    goodreads_url = generate_goodreads_url(book_title, author)
    amazon_url = generate_amazon_url(book_title, author)
    lapl_url = generate_lapl_url(book_title, author)
    libby_url = generate_libby_url(book_title, author)

    # Create clickable links styled as buttons for each platform with their branding colors
    st.markdown(f"""
        <style>
        .button {{
            display: block;
            padding: 0.75em 1.5em;
            text-decoration: none;
            font-weight: bold;
            border-radius: 5px;
            margin: 10px auto;
            color: white !important;
            text-align: center;
            width: 200px;
        }}
        .goodreads {{
            background-color: #D7A168; /* Goodreads beige */
        }}
        .amazon {{
            background-color: #FF9900; /* Amazon orange */
        }}
        .abebooks {{
            background-color: #CC3333; /* AbeBooks red */
        }}
        .libby {{
            background-color: #8E5A9E; /* Libby purple */
        }}
        .lapl {{
            background-color: #003C71; /* LAPL dark blue */
        }}
        .bookshop {{
            background-color: #017AFF; /* Bookshop.org blue */
        }}
        .storygraph {{
            background-color: #5B21B6; /* StoryGraph purple */
        }}
        </style>
        <a href="{goodreads_url}" target="_blank" class="button goodreads">Search on Goodreads</a>
        <a href="{amazon_url}" target="_blank" class="button amazon">Search on Amazon</a>
        <a href="{abebooks_url}" target="_blank" class="button abebooks">Search on AbeBooks</a>
        <a href="{libby_url}" target="_blank" class="button libby">Search on Libby</a>
        <a href="{lapl_url}" target="_blank" class="button lapl">Search on LAPL</a>
        <a href="{bookshop_url}" target="_blank" class="button bookshop">Search on Bookshop.org</a>
        <a href="{storygraph_url}" target="_blank" class="button storygraph">Search on StoryGraph</a>
    """, unsafe_allow_html=True)
