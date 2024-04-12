#!/usr/bin/python3
import requests
import sys

from credentials import HANDLE

print(f"__Fetching Status__", flush=True)
req = requests.get(f"http://codeforces.com/api/user.status?handle={HANDLE}&from=1&count=1").json()

status = req['status']
if status != "OK": print(f"[!] Request Failed: status = {repr(status)}", file=sys.stderr, flush=True); exit(1)
res = req['result'][0]

verdict = res.get("verdict", "IN QUEUE ( _probably_ )")

contest_id, problem_index = res["problem"]["contestId"],res["problem"]["index"]
problem_name = res["problem"]["name"] 

username              = res["author"]["members"][0]["handle"]
language              = res["programmingLanguage"]
passed_count          = res["passedTestCount"]
time_consumed_ms      = res["timeConsumedMillis"]
memory_consumed_bytes = res["memoryConsumedBytes"]

# NOTE: On modifying `s`, appropriately match the new numbre of lines in the `CF.lua` or whatever plugin file is handling the size of the notification box
s = \
f"""{contest_id}{problem_index} `{problem_name}`
{language} 
{username}
---------------
_{verdict}_
took   : `{time_consumed_ms:4}` ms
mem    : `{round(memory_consumed_bytes/(1024*1024)):4}` MB
passed : `{passed_count:4}` tests
"""
# NOTE: On modifying `s`, appropriately match the new numbre of lines in the `CF.lua` or whatever plugin file is handling the size of the notification box

print(s,flush=True,file=sys.stdout if verdict == "OK" else sys.stderr)

