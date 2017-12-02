# COMP 6801 Project

##  Members
 * Matthew Stewart
 * Nicholas Mendez 811002795

## Dependencies
1. Linux Distro for Q1
2. Python 2.7

## Installation

1. install nmap ``` $sudo apt-get install nmap```
2. pip dependencies ``` $ sudo pip install -r requirements.txt```

## Question 1

Run Python scripts to detect Java Deserialization vulnerability in Oracle Web Logic
detect.py - primary method
scan.py - alternative method

## Question 4
1. Generate keys using 8 character password also take note of the IV generated (IMPORTANT) 

    ```$ python main.py generate-keys {8 character password}```
2. Make sure publickey.dat is in the directory then encrypt a message (enclosed in quotes)
 
    ```$ python main.py encrypt "{enter message here}" ```
3. Make sure privatekey.dat and cipher.dat is in the directory and decrypt the message enter the previously mentioned generated IV and password when prompted.
    
    ```$ python main.py decrypt```
    

## Question 6

1. Go To [Demo Link](https://snickdx.me/xss) on chrome.
2. Open DevTools Javascript Console (F12).
3. Login With username: "bob", password "bob".
4. Create a comment "<script src="https://snickdx.me/xss/scammer.js"></script>" to perform xss.
5. Console should show message "Thanks for the data... loser" showing xss was successful.
6. Delete previous comment.
7. Click the "XSS Protection Toggle" then recreate comment.
8. The comment should be displayed and the console should indicate that it has been sanitized.
