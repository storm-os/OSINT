import httpx
import trio
import importlib
import pkgutil
import re
import time
from termcolor import colored
from storm.instruments import TrioProgress

EMAIL_FORMAT = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


class StormArgs:
    def __init__(self):
        self.onlyused = False
        self.nocolor = False
        self.noclear = True
        self.nopasswordrecovery = False
        self.timeout = 10

def import_submodules(package, recursive=True):
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + '.' + name
        results[full_name] = importlib.import_module(full_name)
        if recursive and is_pkg:
            results.update(import_submodules(full_name))
    return results

def get_functions(modules, args):
    websites = []
    for module in modules:
        if len(module.split(".")) > 3:
            modu = modules[module]
            site = module.split(".")[-1]
            websites.append(modu.__dict__[site])
    return websites

def print_result(data, args, email, start_time, websites):
    def print_color(text, color, args):
        return colored(text, color) if not args.nocolor else text

    description = f"{print_color('[+] Email used', 'green', args)}, {print_color(' [-] Email not used', 'magenta', args)}, {print_color(' [x] Rate limit', 'yellow', args)}, {print_color(' [!] Error', 'red', args)}"

    print("\n" + "*" * (len(email) + 6))
    print(f"   {email}")
    print("*" * (len(email) + 6))

    for results in data:
        if results["rateLimit"] and not args.onlyused:
            print(print_color(f"[x] {results['domain']}", "yellow", args))
        elif "error" in results.keys() and results["error"] and not args.onlyused:
            toprint = f" Error message: {results['others']['errorMessage']}" if results["others"] and "Message" in str(results["others"].keys()) else ""
            print(print_color(f"[!] {results['domain']}{toprint}", "red", args))
        elif results["exists"] == False and not args.onlyused:
            print(print_color(f"[-] {results['domain']}", "magenta", args))
        elif results["exists"] == True:
            toprint = "".join([f" {results[k]}" for k in ["emailrecovery", "phoneNumber"] if results[k]])
            print(print_color(f"[+] {results['domain']}{toprint}", "green", args))

    print(f"\n{description}")
    print(f"{len(websites)} websites checked in {round(time.time() - start_time, 2)} seconds")

async def launch_module(module, email, client, out):
    # Dictionary mapping domain
    try:
        await module(email, client, out)
    except Exception:
        name = str(module).split('<function ')[1].split(' ')[0]
        out.append({"name": name, "domain": name, "rateLimit": False, "error": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

async def storm_entry(email):
    """
    MAIN LOGIC FOR Storm Framework
    This logic is connected to storm.py in the root folder.
    """
    if not bool(re.fullmatch(EMAIL_FORMAT, email)):
        print("[-] Incorrect Email Format!")
        return

    args = StormArgs()
    modules = import_submodules("storm.modules")
    websites = get_functions(modules, args)

    start_time = time.time()
    client = httpx.AsyncClient(timeout=args.timeout)
    out = []

    # Trio Progress & Execution
    instrument = TrioProgress(len(websites))
    trio.lowlevel.add_instrument(instrument)

    async with trio.open_nursery() as nursery:
        for website in websites:
            nursery.start_soon(launch_module, website, email, client, out)

    trio.lowlevel.remove_instrument(instrument)
    out = sorted(out, key=lambda i: i['name'])
    await client.aclose()

    print_result(out, args, email, start_time, websites)
    return out
