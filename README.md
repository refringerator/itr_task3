# Rock-Paper-Scissors game

Command line Rock-Paper-Scissors game with moves on your choice!

### Tech stack

1. Python 3.10
2. [PyTest](https://pypi.org/project/pytest/)
3. [PrettyTable](https://pypi.org/project/prettytable/)
4. [Python StateMachine](https://pypi.org/project/python-statemachine/)
5. [rich](https://pypi.org/project/rich/)
6. Bootstrap and Crypto-js on web page

### How to run

1. Create the virtual environment `python3 -m venv myenv`
2. Activate the virtual environment `source myenv/bin/activate`
3. Install requirements `pip install -r requirements.txt`
4. Run game with 3 or 7 params with `make game3` or `make game7`
5. Check results on [Awesome HMAC generator](https://refringerator.github.io/itr_task3/)

### Known issues

1. Using commas in move names causes web pages to incorrectly parse messages

### State machine diagram

![Diagram](/media/sm.svg)

### Demo

![Demo](/media/demo.gif)
