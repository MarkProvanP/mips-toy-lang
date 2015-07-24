The Noggin programming language
=====

### Comments

`# Anything after a '#' on a line is a comment and is not parsed`

Grammar in Backus-Naur Form
-----

program ::=
	{ function } ;

function ::=
	"FUNCTION" ident '(' functiondeclarearguments ')' '{' statements '}' ;

functiondeclarearguments ::=
	ε
	typeandname { ',' typeandname } ;

typeandname ::=
	ident ident

statements ::=
	{ statement } ;

statement ::=
	functioncall
	assignment
	ifelse
	while
	dowhile
	return
	declare ;

functioncall ::=
	ident '(' callarguments ')' ';' ;

callarguments ::=
	ε
	expression { ',' expression } ;

assignment ::=
	ident '=' expression ';' ;

ifelse ::=
	"IF" '(' expression ')' '{' statements '}' "ELSE" '{' statements '}' ;

while ::=
	"WHILE" '(' expression ')' '{' statements '}' ;

dowhile ::=
	"DO" '{' statements '}' "WHILE" '(' expression ')' ';' ;

return ::=
	"RETURN" expression ';' ;

declare ::=
	"DECLARE" typeandname ';' ;

expression ::=
	primary-expression
	binary-expression ;

primary-expression ::=
	number
	ident ;

binary-expression ::=
	expression operator expression ;

operator ::=
	'+' | '-' | '*' | '/' |
	'==' | '!=' | '>' | '<' | '<=' | '>=' ;

ident ::=
	letter { letter | digit } ;

letter ::=
	"a"..."z"  "A"..."Z" ;

number ::=
	"0"
	nonzerodigit { digit } ;

digit ::=
	"0"..."9" ;

nonzerodigit ::=
	"1"..."9" ;
