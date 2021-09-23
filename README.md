# Expript3
This is my customisable programming language, Expript3. There have been two previous versions of Expript3 called Expript and Expript2, but neither of them will be made public. 

## "Programming langauge"
It is not a programming langauage in the conventional sense, but rather it is an expression evaluator. I have programmed my own operators for this language, including the => operator, which is very similar to the ```=>``` operator in JavaScript and the lambda keyword in Python. It acts in a very similar way, generating anonymous functions. Since, in conjuction with the ```<-``` operator (used for function application), this language can simulate [Lambda Calculus](https://en.wikipedia.org/wiki/Lambda_Calculus), it is therefore, [Turing-Complete](https://en.wikipedia.org/wiki/Turing_completeness). 

All the other operators are just for a nice time :)

## The language itself
This langauge is an expression langauge, so all 'code' is actually one long expression. However, I have implemented the ```;``` operator, and what this allows you to do is to string multiple expressions. The ```;``` operator can use the result of the left expression when evaluating the right. For example, the code ```a = 1; a``` will evaluate to ```1``` because the ```;``` operator in the middle uses the result of the ```a = 1``` on its left to change how it evaluates the right. In this case, the result is a binding of ```a``` to ```1```. The ```;``` operator then evaluates ```a```, which because of the binding, it knows is equal to ```1```.

## More information
More infomation can be found on the wiki for this github project. I'll be writing pages there when I can.