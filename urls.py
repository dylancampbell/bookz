import streamlit as st
import urllib.parse

def generate_urls(cleaned_title, cleaned_author):
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

# Individual URL generation functions
def generate_abebooks_url(book_title, author):
    base_url = "https://www.abebooks.com/servlet/SearchResults"
    query_params = {"an": author, "tn": book_title}
    return base_url + "?" + urllib.parse.urlencode(query_params)

def generate_libby_url(book_title, author):
    base_url = "https://libbyapp.com/search/lapl/search/query-"
    search_query = f"{urllib.parse.quote(book_title)}%20{urllib.parse.quote(author)}"
    return base_url + search_query + "/page-1"

# Add other URL generation functions similarly...
