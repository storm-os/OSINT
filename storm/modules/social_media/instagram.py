from storm.core import *
from storm.localuseragent import *


async def instagram(email, client, out):
    name = "instagram"
    domain = "instagram.com"
    method = "register"
    frequent_rate_limit=True

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Origin': 'https://www.instagram.com',
        'DNT': '1',
        'Connection': 'keep-alive',
    }

    try:
        freq = await client.get("https://www.instagram.com/accounts/emailsignup/", headers=headers)
        csrf_match = re.search(r'csrf_token["\']\s*:\s*["\']([^"\']+)', freq.text)
        if csrf_match:
            token = csrf_match.group(1)
        else:
            # If it fails, try the backup pattern for the latest Instagram.
            token_alt = re.search(r'\"csrf_token\":\"(.*?)\"', freq.text)
            token = token_alt.group(1) if token_alt else None

        if not token:
            print("[!] Instagram Security Updated. CSRF Token missing.")
    except Exception:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
        return None

    data = {
        'email': email,
        'username': ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(random.randint(6, 30))),
        'first_name': '',
        'opt_into_one_tap': 'false'
    }
    headers["x-csrftoken"] = token
    check = await client.post(
        "https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/",
        data=data,
        headers=headers)
    check = check.json()
    if check["status"] != "fail":
        if 'email' in check["errors"].keys():
            if check["errors"]["email"][0]["code"] == "email_is_taken":
                out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                            "rateLimit": False,
                            "exists": True,
                            "emailrecovery": None,
                            "phoneNumber": None,
                            "others": None})
            elif "email_sharing_limit" in str(check["errors"]):
                out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                            "rateLimit": False,
                            "exists": True,
                            "emailrecovery": None,
                            "phoneNumber": None,
                            "others": None})
        else:
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
