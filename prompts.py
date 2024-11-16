PROMPTS=dict()
PROMPTS["HumanEval"]=\
'''
This task will evaluate your ability to appreciate the control flow of code with a given input.
In the following, I will give you the source code of a program written in Python. The program may feature different functions, which may call each other.
To make the task more accessible to you, I have annotated the lines with their index as comments (those begin with a #).
The following is very important! *Please note that the function signatures are generally not called,
instead you should start with the first line of the function. This does not apply to the function call, of course.*
In addition to the function, I will give you an initial input and the called function.
It is your task to return the called lines, in order, as a list. I will give you an example:
Source Code : """def simple_loop(x): #1
                     for i in range(3): #2
                         print(i+x) #3
                     return i #4
              """
Input: (5)
Correct solution: [2,3,2,3,2,3,2,4]
Now I will give you your task.
Here is the source code: {0}
Here is the called function: {1}
Here is the input to the function {2}
Please produce the python list containing the executed line numbers in order now. Remember not to include the function signature lines. Think about the solution step-by-step,
going through execution steps one at a time. Finally, print the solution as a list of executed steps.
'''

PROMPTS['Recursion']=\
'''This task will evaluate your ability to appreciate the control flow of code with a given input.
In the following, I will give you the source code of a program written in Python. The program may feature different functions, which may call each other.
To make the task more accessible to you, I have annotated the lines with their index as comments (those begin with a #).
The following is very important! *Please note that the function signatures are generally not called,
instead you should start with the first line of the function. This does not apply to the function call of course.*
In addition to the function, the code will feature a 'main' code block, which you should execute. It is possible that functions are defined in the 
main method, which means the signature will be read once, but not the body.
It is your task to return the called lines while executing the main, in order, as a list. I will give you an example:
Source Code : """def simple_loop(x): #1
                     for i in range(3): #2
                         print(i+x) #3
                     return i #4
                  #5
                  if __name__ == "__main__":#6
                      simple_loop(5)#7
                  """
Correct solution: [7,2,3,2,3,2,3,2,4]
Now I will give you the code for your task.
Here is the source code: {0}
Please produce the python list containing the executed line numbers in order now. Remember not to include the function signature line during a call. Print the solution as a list of executed steps.
Do not produce any other output.
'''

PROMPTS["OOP"]=PROMPTS["Recursion"]

PROMPTS["Concurrency"]=\
'''This task will evaluate your ability to appreciate the control flow of code with a given input.
In the following, I will give you the source code of a program written in Python. The program may feature different functions, which may call each other.
To make the task more accessible to you, I have annotated the lines with their index as comments (those begin with a #).
The following is very important! *Please note that the function signatures are generally not called,
instead you should start with the first line of the function. This does not apply to the function call of course.*
In addition to the function, the code will feature a 'main' code block, which you should execute. It is possible that functions are defined in the 
main method, which means the signature will be read once, but not the body.
It is your task to return the called lines while executing the main, in order, as a list. The contained code may contain concurrency. For this purpose, you are supposed to mark the corresponding lines
using parantheses. In particular, an opening paranthesis should be placed once concurrency starts and a closing one should be placed once it ends (if it concurrency never ends explicitly, place it at the very end).
I will give you an example:
Source Code : 
"""def task(name):#1
       print("Task starting")#2
       time.sleep(2)#3
       print("Task completed")#4
   #5
   if __name__ == "__main__":#6
       thread1 = threading.Thread(target=task, args=('A',))#7
       thread2 = threading.Thread(target=task, args=('B',))#8
       #9
       thread1.start()#10
       thread2.start()#11
       #12
       thread1.join()#13
       thread2.join()#14
       #15
       print("All tasks completed")#16
"""
Correct solution: [7,8,(,10,2,3,4,11,2,3,4,13,14,),16]
Due to the concurrency, execution order may vary. You can pick any valid combination here as long as it is marked correctly with the parentheses.
Now I will give you the code for your task.
Here is the source code: {0}
Please produce the python list containing the executed line numbers in order now. Remember not to include the function signature line during a call. Print the solution as a list of executed steps.
Do not produce any other output.
'''
