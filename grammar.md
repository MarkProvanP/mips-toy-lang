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
	type ident

type ::=
	ident
	ident { "[" "]" }

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
	ident
	array-access-expression ;

array-access-expression ::=
	ident '[' expression ']' { '[' expression ']' } ;

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
	uint_2 | uint_8 | uint_10 | uint_16 | int_10

uint_2 ::=
	"0b" { digit_2 } ;

digit_2 ::=
	"0" | "1"

uint_8 ::=
	"0o" { digit_8 } ;

digit_8 ::=
	"0"..."7"

uint_10 ::=
	"0"
	nonzerodigit_10 { digit_10 } ;

int_10 ::=
	"-" uint_10
	uint_10

digit_10 ::=
	"0"..."9" ;

nonzerodigit_10 ::=
	"1"..."9" ;

uint_16 ::=
	"0x" { digit_16 } ;

digit_16 ::=
	"1"..."9" | "A"..."F" ;

char ::=
	"'" [any ASCII character, or the escaped ones] "'"

escapedchar ::=
	`"\0" | "\\" | "\'" | "\"" | "\t" | "\n"`
