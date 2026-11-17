# py-scheduler-demo

Repository with some demos for schedulers/
orchestrators of triggers, using Python.

Here is the list, in order of complexity, from
the simplest to the more complex one.


 ## 1. basic_two_triggers

 **Summary**

 A scheduler, using APScheduler, has two triggers
 to orchestrate:

 1. Each 5 seconds
 2. Each 10 seconds - 10 milliseconds.

 Both triggers execute the same task, which prints a
 START message, waits 2 seconds, and prints an END
 message.

 The tasks cannot be executed at the same time. For that
 purpose, the scheduler uses a FIFO queue to enqueue the
 different tasks programmed.


**Setup**

Create a virtual environment using Python 3.12:

```bash
python3.12 -m venv .venv
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install APScheduler==3.11.3
```



**How to execute**

From the repository root, activate the virtual environment
and run the demo:

```bash
source .venv/bin/activate
python basic_two_triggers/main.py
```

Press Ctrl+C to stop the scheduler.

---


