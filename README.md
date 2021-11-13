**Expript is currently under development. Not all of the things in this README are possible yet.**
**Check the TODO section to see what has been implemented.** 

# Expript3 - about
Expript3 is a language engine that allows people to create their own expression based programming languages, in addition to other types of languages. I call languages made with Expript3 "Expript Languages". There have been previous versions of Expript, but they have not been fully implemented. They can still be accessed on GitHub if you want to see how bad they are.

# How does Expript3 work?
Expript3 will have things called "Models". These will indicate how a program is taken from its source code, either to be interpreted, or to be compiled. Each model will allow you to finetune and define things that the model uses to take the source code to the final output. For example, it can allow to set the syntax for a language. One of the main models will be the "Expression Model". It say will flow of different components such as the lexer, parser, and interpreter and/or computer. The expression model will allow you to define your own operators which can be used in expressions. Other models may be developed as well, for example the Postfix model. It will allow you to define what each word in the source code will do to the stack. Each instance of a model, where you have defined everything and done everything a model needs you to do, is an expript language. Through clever implenentations of things that a model needs, more complex things can be done, such as statements in an expression based language.

# TODO
This is the big list of things that I want to do. Check here to see if something in the README has been implemented. Anything with a *(maybe?)* next to it is being considered. It may or may not be implemented. 

- [x] Add Standard Expript Language (*STEL*)
    - [x] Add [standard lexer](std.lxr.py)
    - [x] Add [standard parser](std.psr.py)
    - [x] Add [standard interpreter](std.int.py)
    - [ ] Add [standard operaters](std.ops.py) 
        - *some operators have not been fully implemented, but it's enough for now.*
    - [x] Add [standard library](std.lib.py)
    - [x] Add [standard literals](std.lit.py)
    - [x] Add [standard representer](std.rpr.py)
- [ ] Add Extended Expript Language (*EXEL*)
    - [x] Add [extended libary](ext.lib.py).
    - [x] Add [extended operators](ext.ops.py).
- [ ] Refactoring
	- [ ] Add Models
		- [ ] Add Expression model
			- [ ] Reimplement the standard expript language using the expression model
			- [ ] Reimplement the extended expript language using the expression model
			- [ ] Reimplement the lambda calculus expript language using the expression model
		- [ ] Add Postfix model
		- [ ] Add Prefix model *(maybe?)*
	- [ ] Add Shell factory
- [ ] Make Haskellesque expript language using the Expression Model (*HSEL*)
	- ...
	- ...
- [ ] Implement in other languages
	- [ ] Haskell (*Hexpript*)
	- [ ] C (*Cexpript*)
		- [ ] C++ (*CPexpript) *(maybe?)*
	- [ ] Lisp (*Lexpript*)
	- [ ] Java (*Jexpript*)
	- [ ] JavaScript (*JSexpript*)
	- [ ] Expript *(maybe?)*
	- [ ] Porth *(maybe?)*