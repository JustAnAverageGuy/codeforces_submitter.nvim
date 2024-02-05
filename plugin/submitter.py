#!/usr/bin/python3
import sys
import re
import requests

from requests.cookies import RequestsCookieJar 
from Crypto.Cipher import AES
from bs4 import BeautifulSoup


from credentials import CODEFORCES_DOMAIN, HANDLE, PASSWORD, LANGUAGE_CODE
source_file_path = sys.argv[1]

me = requests.Session()
csrf = ""
cookie_jar = RequestsCookieJar()
is_logged_in = False

me.cookies = cookie_jar
me.headers = {
    "user-agent":
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}


def get_parameter(inp):
    key, iv, cipher = [None] * 3

    mat = re.match(r'(?<=a=toNUmbers\(")\w+(?="\))', inp)
    if mat is not None: key = mat.group()

    mat = re.match(r'(?<=b=toNUmbers\(")\w+(?="\))', inp)
    if mat is not None: iv = mat.group()

    mat = re.match(r'(?<=c=toNUmbers\(")\w+(?="\))', inp)
    if mat is not None: cipher = mat.group()

    if not all([key, iv, cipher]):
        raise ValueError(
            f"Regex didn't match in `get_parameter` for input={repr(inp)}"
        )
    return cipher, key, iv


def decrypter_RCPC(ocipher, okey, oiv):
    key = bytes.fromhex(okey)
    iv = bytes.fromhex(oiv)
    cipher = bytes.fromhex(ocipher)

    return AES.new(key, AES.MODE_CBC, iv).decrypt(cipher).hex()


def get_csrf(path):
    res = me.get(path)
    c__srf = BeautifulSoup(res.text, 'html.parser').select_one(".csrf-token")
    if c__srf:
        global csrf
        csrf = c__srf["data-csrf"]
        me.cookies.set('csrf', csrf)

def get_rcpc():
    res = me.get(CODEFORCES_DOMAIN + "/enter")
    if len(res.text) > 800: return "", False
    return decrypter_RCPC(*get_parameter(res.text)), True


def re_login():
    global csrf
    handle = HANDLE
    password = PASSWORD
    rcpc, does_rcpc_exist = get_rcpc()
    if does_rcpc_exist:
        me.cookies.set("RCPC", rcpc)
    get_csrf(CODEFORCES_DOMAIN + "/enter")
    me.post(CODEFORCES_DOMAIN + '/enter?back',
            data={
                "action": "enter",
                "handleOrEmail": handle,
                "password": password,
                "remember": "on",
                "csrf_token": csrf,
            })
    for ke, val in cookie_jar.items():
        me.cookies.set(ke, val)
    get_csrf(CODEFORCES_DOMAIN)


def login():
    print(f'- Logging in as `{HANDLE}`', flush=True)
    re_login()
    global is_logged_in
    is_logged_in = True


def manually_login():
    re_login()


def is_gym(contest_id):
    return len(contest_id) >= 6


def submit_code(contest, index, code, programTypeID):
    login()
    path = f'{CODEFORCES_DOMAIN}/gym/{contest}/submit?csrf_token={csrf}' if is_gym(
        contest
    ) else f'{CODEFORCES_DOMAIN}/contest/{contest}/submit?csrf_token={csrf}'

    print(f'- Submitting problem: `{contest}{index}` for user: `{HANDLE}`', flush=True)

    me.post(path,
            data={
                "csrf_token": csrf,
                "action": "submitSolutionFormSubmitted",
                "contestId": contest,
                "submittedProblemIndex": index,
                "programTypeId": programTypeID,
                "source": code,
                "tabSize": "4",
            })
    print(f'- Submitted !', flush=True)


def main():

    with open(source_file_path) as f: cod = f.read()
    # extract problem index from source code
    matches = re.search(r'https?://codeforces.com/(?:problemset/problem/(?P<contest_id>\d+)/(?P<problem_index>\w+)|(?:contest|gym)/(?P<contest_id_2>\d+)/problem/(?P<problem_index_2>\w+))', cod).groupdict()
    
    contest_id = matches["contest_id"] or matches["contest_id_2"]
    problem_index = matches["problem_index"] or matches["problem_index_2"]

    submit_code(contest_id, problem_index, cod, str(LANGUAGE_CODE))


main()
exit(0)
