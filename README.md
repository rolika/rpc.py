# rpc.py
Realisation of postfix notated calculation in Python3

Application for performing calculations expressed in postfix notation, aka
reversed polish calculation.
Usage:
    self.evaluate(expression),
    where expression is a string containing postfix notated formula,
    for example: 2 3 4 5 + - * = -12
    
Known operators: * / + - ** %
Known functions: all of Python's math module are available for use
                 trigonometrics: please specify degrees, not radians
Known commands:
    =:  display last item in stack (without it, calculation is just performed)
    ==: remove&display last item in stack (pop from stack)
    c:  clear stack (stack isn't cleared after errors by itself)
    v:  declaring a variable
        - not existing: vANY pops stack, and stores value in ANY
        - existing: vANY pushes its value to stack (leaving value in ANY)
        Variable name must follow v immediately!
    d:  destroys all variables
    
Typing errors handled gracefully, ignoring everything that's not a number,
operator, function or command.
Commands are not, but variable names are case sensitive.
