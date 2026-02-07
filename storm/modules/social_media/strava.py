from storm.core import *
from storm.localuseragent import *


async def strava(email, client, out):
    name = "strava"
    domain = "strava.com"
    method = "register"
    frequent_rate_limit=False

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://www.strava.com/register/free?cta=sign-up&element=button&source=website_show',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    r = await client.get("https://www.strava.com/register/free?cta=sign-up&element=button&source=website_show", headers=headers)
    try:
        pattern = r'<meta[^>]*?name=["\']csrf-token["\'][^>]*?content=["\']([^"\']+)["\']'
        match = re.search(pattern, r.text)
        if not match:
            pattern_alt = r'<meta[^>]*?content=["\']([^"\']+)["\'][^>]*?name=["\']csrf-token["\']'
            match = re.search(pattern_alt, r.text)

        if match:
            csrf_token = match.group(1)
            headers['X-CSRF-Token'] = csrf_token
            headers['X-Requested-With'] = 'XMLHttpRequest'
        else:
            raise ValueError("Strava CSRF Token not found - Possible WAF protection")
    except Exception:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    headers['X-Requested-With'] = 'XMLHttpRequest'

    params = {
        'email': email
    }

    response = await client.get('https://www.strava.com/athletes/email_unique', headers=headers, params=params)

    if response.text == "false":
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": False,
                    "exists": True,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    elif response.text == "true":
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
