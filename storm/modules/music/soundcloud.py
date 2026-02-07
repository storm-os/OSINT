from storm.core import *
from storm.localuseragent import *

async def soundcloud(email, client, out):
    name = "soundcloud"
    domain = "soundcloud.com"
    method= "register"
    frequent_rate_limit=False


    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': random.choice(ua["browsers"]["iOS"])
        }

    getAuth = await client.get('https://soundcloud.com/octobersveryown', headers=headers)
    soup = BeautifulSoup(getAuth.text, 'html.parser')

    clientId = None
    for script in soup.find_all('script'):
        if script.contents and "runtimeConfig" in script.contents[0]:
            try:
                data = json.loads(script.contents[0])
                clientId = data["runtimeConfig"]["clientId"]
                break
            except:
                continue

    if not clientId:
        print("[!] Failed to get SoundCloud Client ID.")

    linkMail = email.replace('@','%40')
    API = await client.get(f'https://api-auth.soundcloud.com/web-auth/identifier?q={linkMail}&client_id={clientId}', headers=headers)
    Json = json.loads(API.text)
    if Json['status'] == 'available' or 'in_use':
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": False,
                        "exists": True if Json['status'] == 'in_use' else False,
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
