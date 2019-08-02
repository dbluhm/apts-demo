Aries Protocol Test Suite Demo Agent
====================================

This is a static agent that passes the Aries Protocol Test Suite. It does this
by cutting corners and is therefore not useful as a general purpose agent or
static agent. However, it can be very useful as a demonstration of expected
behavior even if that behavior is hard coded here.

Using this agent, one can see what the complete flow of messages between the
protocol test suite and the agent under test should look like.

Requirements
------------

- Python 3.6 or higher
- `libsodium` version 1.0.15 or higher

> The most recent version of `libsodium` available in package repositories for
> some operating systems may not meet this requirement (notably, Ubuntu 16.04).
> Additionally, pre-built binaries may be altogether unavailable for your
> operating system. If possible, follow the standard installation method for
> your OS; otherwise, follow the instructions listed [here][2].

Quickstart
----------

Create and activate a python virtual environment:
```sh
$ python3 -m venv env
$ source env/bin/activate
```

Install requirements into the virtual environment:
```sh
$ pip install -r requirements.txt
```

Run the agent:
```sh
$ python main.py --endpoint "<endpoint of test suite>" --port 3001
```
