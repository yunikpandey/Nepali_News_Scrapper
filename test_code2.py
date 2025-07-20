import streamlit as st 
import requests 
from bs4 import BeautifulSoup
from processor import *
from io import StringIO


def url_process(url, get_res):
    """Process URL and return extracted content"""
    papers = ['onlinekhabar', 'setopati', 'ratopati', 'annapurnapost', 'nagariknews', 'ekantipur']
    
    try:
        # Extract domain (works for both http:// and https://)
        domain = url.split('//')[-1].split('/')[0].split('.')
        
        # Handle both 'www.example.com' and 'example.com' cases
        site_name = domain[-2] if domain[-2] in papers else domain[-1]
        
        if site_name in papers:
            soup = BeautifulSoup(get_res.text, 'html.parser')
            st.info(f"Processing {site_name} article...")
            
            # Safely get the processor function
            processor = globals().get(f"process_{site_name}")
            if processor:
                return processor(soup)
            return f"No processor available for {site_name}"
        return "Unsupported news website"
    
    except Exception as e:
        return f"Error processing URL: {str(e)}"

# Streamlit UI
st.title("Nepali News Article Extractor")
url = st.text_input("Paste article URL here:", placeholder="https://example.com/news")

if st.button("Extract Content"):
    if url:
        try:
            with st.spinner("Fetching article..."):
                # Set timeout and headers to mimic browser
                headers = {'User-Agent': 'Mozilla/5.0'}
                get_res = requests.get(url, headers=headers, timeout=10)
                
                if get_res.status_code == 200:
                    text = url_process(url, get_res)
                    st.subheader("Extracted Text")
                    st.text_area("Content", text, height=400)
                    # add download button 
                    txt_file=StringIO()
                    txt_file.write(text)
                    st.download_button(
                        label="Download as Txt file", 
                        data=txt_file.getvalue(), 
                        file_name=f"artile_{url}.txt",
                        mime="text/plain"
                    )
                else:
                    st.error(f"Failed to fetch URL (Status {get_res.status_code})")
        
        except requests.exceptions.RequestException as e:
            st.error(f"Connection error: {str(e)}")
        except Exception as e:
            st.error(f"Error occurred: {str(e)}")
    else:
        st.warning("Please enter a URL")

st.info("Thank you for using our service!")