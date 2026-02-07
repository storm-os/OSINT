from storm.core import *
from storm.localuseragent import *


async def ebay(email, client, out):
    name = "ebay"
    domain = "ebay.com"
    method = "login"
    frequent_rate_limit=True

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Origin': 'https://www.ebay.com',
        'DNT': '1',
        'Connection': 'keep-alive',
    }
    try:
        req = await client.get("https://www.ebay.com/signin/", headers=headers) 
        token_match = re.search(r'["\']csrfAjaxToken["\']\s*:\s*["\']([^"\']+)["\']', req.text)  
        if token_match:
            srt = token_match.group(1)
            headers["X-EBAY-CSRF-TOKEN"] = srt 
        else:
            raise ValueError("eBay CSRF Token not found - Possible security challenge")
    except IndexError:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
        return None

    data = {
        'identifier': email,
        'srt': srt
    }

    req = await client.post(
        'https://signin.ebay.com/signin/srv/identifer',
        data=data, headers=headers)
    results = json.loads(req.text)
    if "err" in results.keys():
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": False,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    else:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": False,
                    "exists": True,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})

