# codeforces_submitter.nvim

Useful for submitting solutions to codeforces.

## Installation

 TODO

## Configuration

Add the file `plugin/credentials.py` containing the following
MAKE SURE TO INSERT YOUR HANDLE AND PASSWORD

```py

#!/usr/bin/python3
CODEFORCES_DOMAIN = "https://codeforces.com"
HANDLE="your_handle_here"
PASSWORD="your_password_here"
LANGUAGE_CODE = "language_id_here"
```
## Usage

Have the problem url in the file you want to submit (Maybe have it in your template by using [xeluxee/competitest.nvim](https://github.com/xeluxee/competitest.nvim))

Then 
- `:CodeForceSubmit` submits the current file
- `:LastVerdict` tells you the status of your last submission

## language_code_table
 TODO

## Gotchas
- `:CodeForceSubmit` will report "Submitted !" even if it fails due to captcha verification situaion
