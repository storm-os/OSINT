from storm.core import *
from storm.localuseragent import *
import html

def smart_extract(response_text, keys=["csrf_token", "csrfToken", "csrf-token", "token"]):
    """
    Ekstraktor cerdas untuk mengambil token dari berbagai format (JSON, HTML, atau Entities).
    """
    # 1. Normalize HTML
    clean_text = html.unescape(response_text)
    
    for key in keys:
        # This regex searches for a key, ignoring spaces, quotes, and finds its value.
        pattern = rf'{key}["\']?\s*[:=]\s*["\']?([^"\'\s&>]+)'
        match = re.search(pattern, clean_text, re.IGNORECASE)
        if match:
            return match.group(1)
            
    return None
    

async def aboutme(email, client, out):
    name = "aboutme"
    domain = "about.me"
    method= "register"
    frequent_rate_limit=False

    try:
        reqToken = await client.get("https://about.me/signup", headers=my_headers)
        token = smart_extract(reqToken.text, keys=["csrf", "token", "_token"])

        if token:
            print(f"[+] Token found: {token}")
        else:
            print("[!] Failed to get token. Probably blocked by WAF.")
    except Exception:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
        return None
    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'X-Auth-Token': reqToken.text.split(',"AUTH_TOKEN":"')[1].split('"')[0],
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://about.me',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    data = '{"user_name":"","first_name":"","last_name":"","allowed_features":[],"counters":{"id":"counters"},"settings":{"id":"settings","compliments":{"id":"compliments"},"follow":{"id":"follow"},"share":{"id":"share"}},"email_address":"' + email + \
        '","honeypot":"","actions":{"id":"actions"},"apps":[],"contact":{"id":"contact"},"contact_me":{"id":"contact_me"},"email_channels":{"id":"email_channels"},"flags":{"id":"flags"},"images":[],"interests":[],"jobs":[],"layout":{"version":1,"id":"layout","color":"305B90"},"links":[],"locations":[],"mapped_domains":[],"portfolio":[],"roles":[],"schools":[],"slack_teams":[],"spotlight":{"type":null,"text":null,"url":null,"id":"spotlight"},"spotlight_trial":{"type":null,"text":null,"url":null,"id":"spotlight_trial"},"store":{"id":"store","credit_card":{"number":"","exp_month":"","exp_year":"","cvc":"","address_zip":"","last4":"","id":"credit_card"},"charges":[],"purchases":[]},"tags":[],"testimonials":{"header":"0","id":"testimonials","items":[]},"video":{"id":"video"},"signup":{"id":"signup","step":"email","method":"email"}}'

    response = await client.post('https://about.me/n/signup', headers=headers, data=data)
    if response.status_code == 409:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": False,
                    "exists": True,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    elif response.status_code == 200:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": False,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    else:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
