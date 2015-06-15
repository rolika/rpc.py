### Reverse Polish Calculator

import math

### CLASSES ###

class Stack:
    """ Object to realize&handle stack
        Access to stack only through its methods """

    def __init__(self):
        """ Init stack as list """
        self.clear_stack()

    def clear_stack(self):
        """ Clears stack """
        self.stack = []
        print("\nStack cleared")

    def push_to(self, item):
        """ Function tu push an item to stack
            returns True if item is not a valid number """
        try:
            num = float(item) #only numbers are allowed
        except:
            return True
        self.stack.append(item) #stores numbers as strings (because of eval)
        return False

    def pop_from(self):
        """ Removes&returns last item in stack
            returns None if stack is empty"""
        try:
            return self.stack.pop()
        except:
            print("Error: empty stack")
            return None

class Variable:
    """ Defines storage place & handling methods for variables
        Access to variable only through its methods """

    def __init__(self):
        """ Init storage as dictionary """
        self.clear_variables()

    def clear_variables(self):
        """ Destroy all variables """
        self.variable = {}
        print("\nVariables cleared")

    def check_variable(self, name):
        """ Checks if variable name already exists"""
        if self.variable.get(name, None) is None:
            return False # existing
        return True #not existing

    def add_variable(self, name, value):
        """ Creates new variable equaling value """
        self.variable[name] = value
        print(value, "popped from stack into", name)

    def get_variable(self, name):
        """ Returns variable """
        print(self.variable[name], "from", name, "pushed to stack")
        return self.variable[name]
        
class RPC:
    """Application for performing calculations expressed in postfix notation, aka
    
REVERSED POLISH CALCULATION

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

(c) 2015 Weisz Roland <weisz.roland@wevik.hu> license: ISC"""
    
    def __init__(self):
        """ Init operators, functions & stack """
        self.operators = { "*": "*", "x": "*", "X": "*", "×": "*", ".": "*",
              "/": "/", "÷": "/", ":": "/", "%": "%",
              "+": "+", "-": "-", "^": "**", "**": "**" }
        self.functions = dir(math)[5:] #without language-spec functions
        self.trigonometric = ('acos', 'asin', 'atan', 'cos', 'sin', 'tan') #handling radians
        print(self.__doc__) #display usage
        self.stack, self.var = Stack(), Variable()       
    
    def evaluate(self, expression):
        """ Evaluates expression in postfix notation """
        for op in expression.split(): #split expression at spaces into list
            if self.stack.push_to(op): #number pushed, otherwise proceed
                if op in self.operators.keys(): #handling common operators
                    if self.performCalculation(self.operators[op]):
                        break
                elif op.lower() in self.functions: #handling functions
                    if self.performCalculation(op):
                        break
                elif op == "=" or op == "==": #handling displaying
                    self.displayStackTop(op)
                elif op.lower() == "c": #clear stack
                    self.stack.clear_stack()
                elif op.lower() == "d": #destroy variables
                    self.var.clear_variables()
                elif op[0].lower() == "v": #handling variables
                    var = op[1:]
                    if var:
                        if self.var.check_variable(var): #variable name exists
                            self.stack.push_to(self.var.get_variable(var))
                        else: #encountered new variable name
                            value = self.stack.pop_from()
                            if value is not None:
                                self.var.add_variable(var, value)
                            else:
                                break
                    else:
                        print("Error: variable name must follow v immediately")
                        break
                else:
                    print(op, "ignored")
                    
    def displayStackTop(self, how):
        """ Displays stack's top item, where
            how can be = or == (latter removes item from stack too) """
        top_item = self.stack.pop_from()
        if top_item is not None:
            print(top_item)
            if how == "=": #only read
                self.stack.push_to(top_item) #push back item

    def performCalculation(self, operator):
        """ Performs calculation based on operators type """
        if operator in self.functions: #function with one operand
            operand = self.stack.pop_from()
            if operand is not None:
                formula = "math." + operator + "(" + operand + ")" #like: math.sqrt(2)
                if operator in self.trigonometric:
                    formula = "math." + operator + "(math.radians(" + operand + "))" #like: math.sin(math.radians(60))
            else:
                return True #error already displayed
        else: #otherwise operator with two operands
            operand1, operand2 = self.stack.pop_from(), self.stack.pop_from()
            if (operand1 is not None) and (operand2 is not None):
                formula = operand2 + operator + operand1
            else:
                return True #error already displayed
        try:
            self.stack.push_to(str(eval(formula))) #validated (no injections)
            return False
        except ZeroDivisionError:
            print("Error: divide by zero")
            return True
        except:
            print("Error: calculation impossible")
            return True
        return False
        
def main():
    """ Main programm """
    app = RPC() #instantiate calculator
    while True:
        expression = input("\nPlease enter a postfix-notated expression: ")
        if expression.lower() == "done":
            break
        app.evaluate(expression)

if __name__ == "__main__":
    main()
