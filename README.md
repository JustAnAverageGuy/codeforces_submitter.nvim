# Codeforces Submitter Plugin Vim

This plugin helps you in submitting your solutions to codeforces while practicing.

#Installation

To install this plugin just run the following commands on your terminal:

`cd ~/.vim/bundle`

`git clone https://github.com/iamayushanand/CodeForce.vim.git`

## Configuration

You need to configure CF.vim present in the plugin/ dir based on your codeforces account settings etc.

on line 30 replace "yourhandle" with Your Handle and on line 31 replace "YourPassword" with your codeforces password.On line 37 replace your User agent with the default.

on line 46 replace 'depends on language' with your language code given in this README.
Replace the location given in line 59 with your preferred one(That snippet is for debugging purposes).Replace the location given in line 71 with the location in which the file checker.py is present.

Replace "YourHandle" in checker.py with your cf handle.

## Language Codes

|Language          |Language code|
|------------------|-------------|
|GNU GCC 5.1.0     |           10|
|GNU GCC C11 5.1.0 |           43|
|GNU G++ 5.1.0     |            1|
|GNU G++11 5.1.0   |           42|
|GNU G++14 6.2.0   |           50|
|Microsoft visu C++|            2|
|Haskell GHC 7.8   |           12|
|Java 1.8.0        |           46|
|Perl 5.20.1       |           13|
|python 2.7.12     |            7|
|python 3.5.2      |           31|

## Dependencies

You need to have python with beautiful soup and requests library installed.

## Usage 

To submit a code for a specific cf problem use 

`:CodeForceSubmit XXXA`

where XXXA is problem code.

To see your last verdict use

`:LastVerdict`

## Issues 

If you find any problems or bug with my plugin please email me at iamayushanand@gmail.com 
or open an issue on github page.

## Self Promition

If you like this plugin then follow me on github ;).


