from storm.core import *
from storm.localuseragent import *


async def github(email, client, out):
    name = "github"
    domain = "github.com"
    method = "register"
    frequent_rate_limit=False

    try:
        freq = await client.get("https://github.com/join", headers=headers)

        token_match = re.search(
            r'<auto-check[^>]*?src="/signup_check/email"[^>]*?>[\s\S]*?value="([^"]+)"', 
            freq.text
        )
        if token_match:
            auth_token = token_match.group(1)
            data = {"value": email, "authenticity_token": auth_token}
            headers["X-Requested-With"] = "XMLHttpRequest"
        else:
            raise ValueError("GitHub Email Token not found - Structure changed or Blocked")
    except Exception:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": None,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
        return None

    req = await client.post("https://github.com/signup_check/email", data=data, headers=headers)
    if "Your browser did something unexpected." in req.text:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": None,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    elif req.status_code == 422:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": False,
                    "exists": True,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    elif req.status_code == 200:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": False,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    else:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": None,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
