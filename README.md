# Lisp-Interpreter
A simple LISP interpreter using Python. It can interpret the following commands:

- If
- Define
- Begin
- Quote
- Lambda
- Arithmetic operations (eg: +, -, etc.)

## How to use

Clone the repository and run the file using the command:

```
python3 LispInterpreter.py
```
Input the LISP commands that need to be interpreted, and the corresponding output will be displayed. A read-eval-print loop has been implemented, so the program will accept inputs continuously until a blank line is entered.

##### Sample output

```
>>(define circle-area (lambda (r) (* pi (* r r))))
>>(circle-area 3)
28.274333882308138
>>
---Program Terminated---
```
