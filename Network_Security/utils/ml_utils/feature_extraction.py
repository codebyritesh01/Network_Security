import re
from urllib.parse import urlparse
import ipaddress
import pandas as pd

def get_features_from_url(url: str):
    """
    Extracts 30 features from a given URL to be used by the Phishing detection model.
    Returns a pandas DataFrame.
    """
    features = {}

    # Standardize URL
    if not url.startswith('http'):
        url = 'http://' + url
    
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    path = parsed_url.path

    # 1. having_IP_Address
    try:
        ipaddress.ip_address(domain)
        features['having_IP_Address'] = 1
    except:
        features['having_IP_Address'] = -1

    # 2. URL_Length
    if len(url) < 54:
        features['URL_Length'] = -1
    elif 54 <= len(url) <= 75:
        features['URL_Length'] = 0
    else:
        features['URL_Length'] = 1

    # 3. Shortining_Service
    match = re.search(r'bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                      r'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                      r'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                      r'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                      r'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                      r'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                      r'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|tr\.im|link\.zip\.net',
                      url)
    features['Shortining_Service'] = 1 if match else -1

    # 4. having_At_Symbol
    features['having_At_Symbol'] = 1 if "@" in url else -1

    # 5. double_slash_redirecting
    features['double_slash_redirecting'] = 1 if url.rfind("//") > 7 else -1

    # 6. Prefix_Suffix
    features['Prefix_Suffix'] = 1 if "-" in domain else -1

    # 7. having_Sub_Domain
    dot_count = domain.count('.')
    if dot_count <= 2:
        features['having_Sub_Domain'] = -1
    elif dot_count == 3:
        features['having_Sub_Domain'] = 0
    else:
        features['having_Sub_Domain'] = 1

    # 8. SSLfinal_State
    features['SSLfinal_State'] = 1 if parsed_url.scheme == 'https' else -1

    # 9. Domain_registeration_length
    # This usually requires WHOIS. For real-time we use a default/heuristic.
    features['Domain_registeration_length'] = -1 

    # 10. Favicon
    features['Favicon'] = -1

    # 11. port
    features['port'] = -1 if ":" in domain else 1

    # 12. HTTPS_token
    features['HTTPS_token'] = 1 if "https" in domain else -1

    # 13. Request_URL
    features['Request_URL'] = -1

    # 14. URL_of_Anchor
    features['URL_of_Anchor'] = -1

    # 15. Links_in_tags
    features['Links_in_tags'] = -1

    # 16. SFH
    features['SFH'] = -1

    # 17. Submitting_to_email
    features['Submitting_to_email'] = 1 if "mailto" in url else -1

    # 18. Abnormal_URL
    features['Abnormal_URL'] = -1 if domain in url else 1

    # 19. Redirect
    features['Redirect'] = 0

    # 20. on_mouseover
    features['on_mouseover'] = -1

    # 21. RightClick
    features['RightClick'] = -1

    # 22. popUpWidnow
    features['popUpWidnow'] = -1

    # 23. Iframe
    features['Iframe'] = -1

    # 24. age_of_domain
    features['age_of_domain'] = -1

    # 25. DNSRecord
    features['DNSRecord'] = -1

    # 26. web_traffic
    features['web_traffic'] = 0

    # 27. Page_Rank
    features['Page_Rank'] = -1

    # 28. Google_Index
    features['Google_Index'] = 1

    # 29. Links_pointing_to_page
    features['Links_pointing_to_page'] = 0

    # 30. Statistical_report
    features['Statistical_report'] = -1

    # Convert to DataFrame in the same order as the training data
    df = pd.DataFrame([features])
    
    # Ensure correct column order (from CSV)
    cols = ["having_IP_Address","URL_Length","Shortining_Service","having_At_Symbol","double_slash_redirecting","Prefix_Suffix","having_Sub_Domain","SSLfinal_State","Domain_registeration_length","Favicon","port","HTTPS_token","Request_URL","URL_of_Anchor","Links_in_tags","SFH","Submitting_to_email","Abnormal_URL","Redirect","on_mouseover","RightClick","popUpWidnow","Iframe","age_of_domain","DNSRecord","web_traffic","Page_Rank","Google_Index","Links_pointing_to_page","Statistical_report"]
    
    return df[cols]
