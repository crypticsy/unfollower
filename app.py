# ----------------------------------------------- Relevant Librarires -----------------------------------------------

import streamlit as st
import zipfile
import json

from bs4 import BeautifulSoup as bs


st.set_page_config(
    page_title="Instagram Unfollower",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Remove whitespace from the top of the page and sidebar
st.markdown("""
        <style>
               .block-container {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                    padding-left: 6vw;
                    padding-right: 6vw;
                }
        </style>
        """, unsafe_allow_html=True)

divider_color = "red"

# ----------------------------------------------- Main Page -----------------------------------------------

st.markdown("<br/><br/>", unsafe_allow_html=True)
st.subheader("Instagram Unfollower", divider=divider_color)
st.markdown("""
<p style="font-size: 13px; font-weight: 400;">
    A simple tool to help you identify the people on Instagram who don't follow you back! <br/>
    It is designed to help you manage your Instagram following list, 
    clearing out the accounts that don’t reciprocate your follow and letting you focus on people who genuinely care about your content. 💖
</p>
""", unsafe_allow_html=True)

# Steps inside a toggle
with st.expander("How to Download Instagram Follower and Following Data From Meta", icon="🤔"):
    st.divider()
    st.write("Follow the steps below to download your Instagram follower and following data from Meta.")
    
    steps = [
        "Log in to your Instagram account on the [Instagram website](https://www.instagram.com/) or the mobile app.",
        "Go to your profile and tap the **Menu** icon (three lines) in the top-right corner.",
        "Select **Settings and Privacy** and scroll down to click **Meta Account Center**.",
        "In the Account Center, go to **Privacy** and click **Your Information and Permissions**.",
        "Choose **Download Your Information**, then select **Some of your information**.",
        "Scroll down, check **Followers and Following**, and click **Next**.",
        "Select **Download to device**, choose **All time** for the date range.",
        "Click **Request a Download**. Wait for an email from Meta with your download link.",
        "Open the email, click the link, and log in to confirm your request.",
        "Download the ZIP file, and upload it to this webpage."
    ]

    for i, step in enumerate(steps, start=1):
        st.markdown(f"**Step {i}:** {step}")

st.markdown("<br/>", unsafe_allow_html=True)

# Data format
save_type = st.radio("Data Format", ["HTML", "JSON"], index=0, horizontal=True)

st.markdown("<br/>", unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("Upload your zip file here", type=["zip"])

if uploaded_file:
    with st.spinner("Processing the uploaded ZIP file..."):
        followers = ""
        following = ""
        unfollowers = []

        # Open the ZIP file in memory
        with zipfile.ZipFile(uploaded_file, "r") as zip_ref:    
            for file_name in zip_ref.namelist():            
                if save_type == "HTML" and file_name.endswith(".html"):
                    if "followers" in file_name.split("/")[-1]:
                        with zip_ref.open(file_name) as file:
                            followers = bs(file.read(), "html.parser")
                        
                    elif "following" in file_name.split("/")[-1]:
                        with zip_ref.open(file_name) as file:
                            following = bs(file.read(), "html.parser")
                
                elif save_type == "JSON" and file_name.endswith(".json"):
                    if "followers" in file_name.split("/")[-1]:
                        with zip_ref.open(file_name) as file:
                            followers = json.load(file)
                    
                    elif "following" in file_name.split("/")[-1]:
                        with zip_ref.open(file_name) as file:
                            following = json.load(file)

    if followers and following and save_type == "HTML":
        st.success("Data successfully extracted!")
        
        followers_list = [follower.text for follower in followers.find_all("a", {"target": "_blank"})] 
        following_list = [followin.text for followin in following.find_all("a", {"target": "_blank"})]
        unfollowers = [following for following in following_list if following not in followers_list]
    
    elif followers and following and save_type == "JSON":
        st.success("Data successfully extracted!")
        
        followers_list = [follower["string_list_data"][0]["value"] for follower in followers]
        following_list = [followin["string_list_data"][0]["value"] for followin in following["relationships_following"]]
        unfollowers = [following for following in following_list if following not in followers_list]
    
    else:
        st.error("Please ensure you have uploaded the correct ZIP file and selected the correct data format.")
    
    if unfollowers:
        st.markdown("<br/><br/>", unsafe_allow_html=True)
        st.subheader("Users that you follow but don't follow you back", divider=divider_color)
      
        col1, col2, col3 = st.columns(3)
        col1.metric("Users that meet the criteria", len(unfollowers))
        col2.metric("Total Followers", len(followers_list))   
        col3.metric("TotalF ollowing", len(following_list))
        
        search_term = st.text_input("Search for a specific user", "")
        st.markdown("<br/>", unsafe_allow_html=True)

        filtered_search = unfollowers
        if search_term: filtered_search = [user for user in unfollowers if search_term.lower() in user.lower()]
            
        for unfollower in filtered_search:
            st.markdown(f"👻  &nbsp; [{unfollower}](https://www.instagram.com/{unfollower})")

st.markdown("<br/><br/><br/>", unsafe_allow_html=True)