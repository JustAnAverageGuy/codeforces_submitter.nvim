#!/usr/bin/python3
import requests
import sys

from credentials import HANDLE

print(f"__Fetching Status__", flush=True)
req = requests.get(f"http://codeforces.com/api/user.status?handle={HANDLE}&from=1&count=1").json()

status = req['status']
if status != "OK": print(f"[!] Request Failed: status = {repr(status)}", file=sys.stderr, flush=True); exit(1)
res = req['result'][0]

verdict = res["verdict"]

contest_id, problem_index = res["problem"]["contestId"],res["problem"]["index"]
problem_name = res["problem"]["name"] 

username = res["author"]["members"][0]["handle"]
language = res["programmingLanguage"]

s = \
f"""{contest_id}{problem_index} `{problem_name}`
{language} 
{username}
---------------
_{verdict}_
"""

print(s,flush=True,file=sys.stdout if verdict == "OK" else sys.stderr)

