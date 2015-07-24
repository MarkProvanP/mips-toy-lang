The Noggin programming language
=====

### Comments

`# Anything after a '#' on a line is a comment and is not parsed`

Grammar in Backus-Naur Form
-----

program ::=
	{ function } ;

function ::=
	"FUNCTION" typeandname '(' functiondeclarearguments ')' '{' statements '}' ;

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
	declare
	switch
	break
	fallthrough ;

functioncall ::=
	ident '(' callarguments ')' ';' ;

callarguments ::=
	ε
	expression { ',' expression } ;

assignment ::=
	ident '=' expression ';' ;

ifelse ::=
	"IF" '(' expression ')' '{' statements '}' { elif }
	"IF" '(' expression ')' '{' statements '}' "ELSE" '{' statements '}' ;

elif ::=
	"ELIF" '(' expression ')' '{' statements '}'

while ::=
	"WHILE" '(' expression ')' '{' statements '}' ;

dowhile ::=
	"DO" '{' statements '}' "WHILE" '(' expression ')' ';' ;

return ::=
	"RETURN" expression ';' ;

declare ::=
	"DECLARE" typeandname ';'
	"DECLARE" typeandname "=" primary-expression ;

switch ::=
	"SWITCH" '(' expression ')' '{' { casestatement } '}'
	"SWITCH" '(' expression ')' '{' { casestatement } defaultstatement '}'

casestatement ::=
	"CASE" primary-expression ":" statements

defaultstatement ::=
	"DEFAULT" ":" statements

expression ::=
	primary-expression
	binary-expression ;

primary-expression ::=
	bool
	char
	number
	ident ;

bool ::=
	"TRUE" | "FALSE" ;

binary-expression ::=
	expression operator expression ;

operator ::=
	`'+' | '-' | '*' | '/' |
	'==' | '!=' | '>' | '<' | '<=' | '>=' ;`

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

char ::=
	"'" [any ASCII character, or the escaped ones] "'"

escapedchar ::=
	`"\0" | "\\" | "\'" | "\"" | "\t" | "\n"`
