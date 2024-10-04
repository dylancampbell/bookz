# Render buttons for each platform
st.markdown("""
    <style>
    .button {
        display: inline-block;
        padding: 10px 20px;
        margin: 10px;
        font-size: 16px;
        color: white;
        text-align: center;
        text-decoration: none;
        border-radius: 8px;
    }
    .goodreads { background-color: #D7A168; }
    .amazon { background-color: #FF9900; }
    .abebooks { background-color: #CC3333; }
    .libby { background-color: #8E5A9E; }
    .lapl { background-color: #003C71; }
    .bookshop { background-color: #017AFF; }
    .storygraph { background-color: #5B21B6; }
    </style>

    <a href="{goodreads_url}" target="_blank" class="button goodreads">Goodreads</a>
    <a href="{amazon_url}" target="_blank" class="button amazon">Amazon</a>
    <a href="{abebooks_url}" target="_blank" class="button abebooks">AbeBooks</a>
    <a href="{libby_url}" target="_blank" class="button libby">Libby</a>
    <a href="{lapl_url}" target="_blank" class="button lapl">LAPL</a>
    <a href="{bookshop_url}" target="_blank" class="button bookshop">Bookshop.org</a>
    <a href="{storygraph_url}" target="_blank" class="button storygraph">StoryGraph</a>
""", unsafe_allow_html=True)
