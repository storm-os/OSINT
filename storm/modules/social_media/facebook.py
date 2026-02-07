from storm.localuseragent import *
from storm.core import *
import random
import string
import requests  # Adjust if using a different HTTP library

async def facebook(email, client, out):
    name = "Facebook"
    domain = "facebook.com"
    method = "register"
    frequent_rate_limit = True

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Origin': 'https://www.facebook.com',
        'DNT': '1',
        'Connection': 'keep-alive',
    }

    try:
        response = await client.get("https://www.facebook.com/accounts/emailsignup/", headers=headers)
        
        if "checkpoint" in str(response.url):
            raise Exception("Detected by Facebook (Security Checkpoint)")

        token_match = re.search(r'["\']csrf_token["\']\s*:\s*["\']([^"\']+)["\']', response.text)
        lsd_match = re.search(r'["\']LSD["\']\s*,\s*\[\s*\]\s*,\s*\{["\']token["\']\s*:\s*["\']([^"\']+)["\']', response.text)

        if token_match:
            csrf_token = token_match.group(1)
            lsd_token = lsd_match.group(1) if lsd_match else None
        
            headers["X-FB-LSD"] = lsd_token
        else:
            raise ValueError("Facebook CSRF Token not found.")
    except Exception:
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
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

    try:
        check = await client.post(
            "https://www.facebook.com/api/v1/web/accounts/web_create_ajax/attempt/",
            data=data,
            headers=headers)
        check = check.json()

        if check["status"] != "fail":
            if 'email' in check["errors"].keys():
                if check["errors"]["email"][0]["code"] == "email_is_taken":
                    out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                                "rateLimit": False,
                                "exists": True,
                                "emailrecovery": None,
                                "phoneNumber": None,
                                "others": None})
                elif "email_sharing_limit" in str(check["errors"]):
                    out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                                "rateLimit": False,
                                "exists": True,
                                "emailrecovery": None,
                                "phoneNumber": None,
                                "others": None})
            else:
                out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                            "rateLimit": False,
                            "exists": False,
                            "emailrecovery": None,
                            "phoneNumber": None,
                            "others": None})
        else:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": True,
                        "exists": False,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
    except Exception as e:
        print(f"Error occurred during POST request: {e}")
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
