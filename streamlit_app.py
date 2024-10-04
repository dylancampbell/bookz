import streamlit as st
import requests
import urllib.parse
import json

# --- Function to clean up author/title using Google Books API ---
def clean_up_book_details(book_title=None, author=None):
    query = ""
    if book_title:
        query += f"intitle:{book_title}"
    if author:
        if query:
            query += "+"
        query += f"inauthor:{author}"

    # Retrieve the API key from Streamlit secrets
    api_key = st.secrets["google_books"]["api_key"]
    google_books_api = f"https://www.googleapis.com/books/v1/volumes?q={urllib.parse.quote(query)}&key={api_key}"
    
    try:
        response = requests.get(google_books_api)
        response.raise_for_status()  # Raises an error for bad status codes
        data = response.json()
        
        if 'items' in data and len(data['items']) > 0:
            book_data = data['items'][0]['volumeInfo']
            # Handle case where only author is provided
            if author and not book_title:
                cleaned_title = ""
                cleaned_author = ', '.join(book_data.get('authors', [author]))
            else:
                cleaned_title = book_data.get('title', book_title)
                cleaned_author = ', '.join(book_data.get('authors', [author])) if book_title else author
            return cleaned_title, cleaned_author
        else:
            st.error("No matching books found. Check the input or try again later.")
            return book_title, author

    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the Google Books API: {e}")
        return book_title, author


# --- URL GENERATION FUNCTIONS ---
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
    return base_url + "?" + urllib.parse.urlencode(query_params)

def generate_libby_url(book_title=None, author=None):
    base_url = "https://libbyapp.com/search/lapl/search/query-"
    search_query = f"{urllib.parse.quote(book_title)}%20{urllib.parse.quote(author)}" if book_title and author else urllib.parse.quote(book_title or author)
    return base_url + search_query + "/page-1"

def generate_bookshop_url(book_title=None, author=None):
    base_url = "https://bookshop.org/books"
    query_params = {"keywords": f"{book_title} {author}"}
    return base_url + "?" + urllib.parse.urlencode(query_params)

def generate_storygraph_url(book_title=None, author=None):
    base_url = "https://app.thestorygraph.com/browse"
    query_params = {"search_term": f"{book_title} {author}"}
    return base_url + "?" + urllib.parse.urlencode(query_params)

def generate_goodreads_url(book_title=None, author=None):
    base_url = "https://www.goodreads.com/search"
    query = f"{book_title} {author}" if book_title and author else book_title or author
    query_params = {"q": query, "search_type": "books"}
    return base_url + "?" + urllib.parse.urlencode(query_params)

def generate_amazon_url(book_title=None, author=None):
    base_url = "https://www.amazon.com/s"
    query = f"{book_title} {author}" if book_title and author else book_title or author
    query_params = {"k": query}
    return base_url + "?" + urllib.parse.urlencode(query_params)

def generate_lapl_url(book_title=None, author=None):
    base_url = "https://ls2pac.lapl.org/?section=search"
    search_data = {
        "isAnd": True,
        "searchTokens": [
            {"searchString": author, "type": "Contains", "field": "Author"} if author else None,
            {"searchString": book_title, "type": "Contains", "field": "Title"} if book_title else None,
        ]
    }
    search_query = urllib.parse.quote(json.dumps(search_data))
    return f"{base_url}&term={search_query}&page=0&pageSize=10&sortKey=Relevancy&db=ls2pac"

# --- STREAMLIT UI ---

# Store input in session state to persist across refreshes
if 'book_title' not in st.session_state:
    st.session_state['book_title'] = ""
if 'author' not in st.session_state:
    st.session_state['author'] = ""
if 'links_generated' not in st.session_state:
    st.session_state['links_generated'] = False

# Title and description
st.title('Bookworm 📚')
st.write("Enter the book title and/or author's name. We'll clean it up before generating search links.")

# Input fields for book title and author
st.session_state['book_title'] = st.text_input("Book Title", value=st.session_state['book_title'])
st.session_state['author'] = st.text_input("Author", value=st.session_state['author'])

book_title = st.session_state['book_title']
author = st.session_state['author']

# Re-enable the "Generate Links" button if inputs are modified
if book_title != st.session_state.get('previous_title') or author != st.session_state.get('previous_author'):
    st.session_state['links_generated'] = False

# Store the current values for comparison
st.session_state['previous_title'] = book_title
st.session_state['previous_author'] = author

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

# Generate URLs and buttons if links are generated
if st.session_state['links_generated']:
    cleaned_title = st.session_state['cleaned_title']
    cleaned_author = st.session_state['cleaned_author']

    # Generate URLs for each platform using cleaned_title and cleaned_author
    abebooks_url = generate_abebooks_url(cleaned_title, cleaned_author)
    bookshop_url = generate_bookshop_url(cleaned_title, cleaned_author)
    storygraph_url = generate_storygraph_url(cleaned_title, cleaned_author)
    goodreads_url = generate_goodreads_url(cleaned_title, cleaned_author)
    amazon_url = generate_amazon_url(cleaned_title, cleaned_author)
    lapl_url = generate_lapl_url(cleaned_title, cleaned_author)
    libby_url = generate_libby_url(cleaned_title, cleaned_author)

    # Split links into three categories: Review, Borrow, Buy
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("<h3 style='text-align: center;'>Review</h3>", unsafe_allow_html=True)
        st.markdown(f'<a href="{goodreads_url}" target="_blank" class="button goodreads">Goodreads</a>', unsafe_allow_html=True)
        st.markdown(f'<a href="{storygraph_url}" target="_blank" class="button storygraph">StoryGraph</a>', unsafe_allow_html=True)

    with col2:
        st.markdown("<h3 style='text-align: center;'>Borrow</h3>", unsafe_allow_html=True)
        st.markdown(f'<a href="{libby_url}" target="_blank" class="button libby">Libby</a>', unsafe_allow_html=True)
        st.markdown(f'<a href="{lapl_url}" target="_blank" class="button lapl">LAPL</a>', unsafe_allow_html=True)

    with col3:
        st.markdown("<h3 style='text-align: center;'>Buy</h3>", unsafe_allow_html=True)
        st.markdown(f'<a href="{amazon_url}" target="_blank" class="button amazon">Amazon</a>', unsafe_allow_html=True)
        st.markdown(f'<a href="{abebooks_url}" target="_blank" class="button abebooks">AbeBooks</a>', unsafe_allow_html=True)
        st.markdown(f'<a href="{bookshop_url}" target="_blank" class="button bookshop">Bookshop.org</a>', unsafe_allow_html=True)

    # Styling for the buttons
    st.markdown("""
        <style>
        .button {
            display: block;
            padding: 0.75em 1.5em;
            text-decoration: none;
            font-weight: bold;
            border-radius: 5px;
            margin: 10px auto;
            color: white !important;
            text-align: center;
            width: 200px;
        }
        .goodreads {
            background-color: #D7A168;
        }
        .amazon {
            background-color: #FF9900;
        }
        .abebooks {
            background-color: #CC3333;
        }
        .libby {
            background-color: #8E5A9E;
        }
        .lapl {
            background-color: #003C71;
        }
        .bookshop {
            background-color: #017AFF;
        }
        .storygraph {
            background-color: #5B21B6;
        }
        </style>
    """, unsafe_allow_html=True)
