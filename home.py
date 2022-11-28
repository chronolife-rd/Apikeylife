import streamlit as st
from template.style import set_footer_style
from version import VERSION
import requests
import json

st.header("Get Chronolife API key")


username    = st.text_input("Username", placeholder="Ex: John")
password    = st.text_input("Password", type="password")
otp_token   = st.text_input("Double Authentication")

button_get_api_key = st.button('Get my API key')

if button_get_api_key:
    
    message = ''
    try:
        otp_token = int(otp_token)
        
    except:
        message = "Invalid Double Authentication"
        st.error()
        st.stop()
        
    # Build the payload with the otp_token given by Google Authenticator.
    request_body = {'otp_token': otp_token}
    
    url = "https://prod.chronolife.net/api/2/user/{userId}/token".format(userId=username)
    
    # Perform the POST request authenticated with the "Basic" authentication scheme. 
    reply = requests.post(url, auth=(username, password), json=request_body)
    
    message = ''
    if reply.status_code == 200: # We chose 200 OK for successful request instead of 201 Created!
        json_reply = json.loads(reply.text)
        message = "API Key: ", json_reply['apiKey']
    elif reply.status_code == 400:
        message = 'Part of the request could not be parsed or is incorrect.'
    elif reply.status_code == 401:
        message = 'Invalid authentication'
    elif reply.status_code == 403:
        message = 'Not authorized.'
    elif reply.status_code == 404:
        message = 'Invalid url'
    elif reply.status_code == 500:
        message = "Invalid Authentication"
        
    if reply.status_code != 200:
        st.error(message)
    else:
        st.success('Please find your API key:   ' + json_reply['apiKey'])
    
footer = set_footer_style()
footer +="""
<div class="footer">
<p style="color: grey;">Version
"""
footer += VERSION
footer +="""
</p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)
