from storm.core import *
from storm.localuseragent import *


async def bitmoji(email, client, out):
    name = "bitmoji"
    domain = "bitmoji.com"
    method = "login"
    frequent_rate_limit=False

    try:
        req = await client.get("https://accounts.snapchat.com", headers=headers)
        
        xsrf_match = re.search(r'data-xsrf=["\']([^"\']+)["\']', req.text)
        client_id_match = re.search(r'data-web-client-id=["\']([^"\']+)["\']', req.text)
    
        if xsrf_match and client_id_match:
            xsrf = xsrf_match.group(1)
            web_client_id = client_id_match.group(1)
            
            headers["X-XSRF-TOKEN"] = xsrf
            headers["X-Web-Client-Id"] = web_client_id
        else:
            raise ValueError("Snapchat/Bitmoji security tokens not found")
            
        url = "https://accounts.snapchat.com/accounts/merlin/login"
        headers = {
            "Host": "accounts.snapchat.com",
            "User-Agent": random.choice(ua["browsers"]["firefox"]),
            "Accept": "*/*",
            "X-XSRF-TOKEN": xsrf,
            "Accept-Encoding": "gzip, late",
            "Content-Type": "application/json",
            "Connection": "close",
            "Cookie": "xsrf_token=" + xsrf + "; web_client_id=" + webClientId
        }
        data = '{"email":' + email + ',"app":"BITMOJI_APP"}'

        response = await client.post(url, data=data, headers=headers)
        if response.status_code != 204:
            data = response.json()
            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": False,
                        "exists": data["hasBitmoji"],
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
            return None
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": False,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    except Exception:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
