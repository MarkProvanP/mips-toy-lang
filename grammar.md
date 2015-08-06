The Noggin programming language
=====

### Comments

`# Anything after a '#' on a line is a comment and is not parsed`

### Grammar in Backus-Naur Form
-----

program ::=
	{ functiondeclare | declare } { functiondefine };

function-declare :: =
	"DECLARE" "FUNCTION" type name '(' function-signature-arguments ')' ';'

function-define ::=
	"FUNCTION" type name '(' function-signature-arguments ')' '{' statements '}' ;

function-signature-arguments ::=
	ε
	function-signature-declare { ',' function-signature-declare } ;

function-signature-declare ::=
	type name

type ::=
	ident
	ident { "[" "]" }

name ::=
	ident

statements ::=
	{ statement } ;

statement ::=
	asm-statement
	expression-statement
	ifelse
	while
	dowhile
	for-loop
	return
	declare
	switch
	break
	fallthrough ;

asm-statement ::=
	"ASM" '{' { string } '}' ;

expression-statement ::=
	expression ';' ;

callarguments ::=
	ε
	expression { ',' expression } ;

ifelse ::=
	"IF" '(' expression ')' '{' statements '}' { elif }
	"IF" '(' expression ')' '{' statements '}' "ELSE" '{' statements '}' ;

elif ::=
	"ELIF" '(' expression ')' '{' statements '}'

while ::=
	"WHILE" '(' expression ')' '{' statements '}' ;

dowhile ::=
	"DO" '{' statements '}' "WHILE" '(' expression ')' ';' ;

(*

forloop ::=
	"FOR" '(' forloop-initialisation ';' expression ';' forloop-afterthought ')' '{' statements '}'

forloop-initialisation ::=
	ε
	type name '=' expression
	type name '=' expression { ',' name '=' expression }
*)

return ::=
	"RETURN" expression ';' ;

declare ::=
	"DECLARE" type-and-name ';'
	"DECLARE" type-and-name "=" literal-expression ;

switch ::=
	"SWITCH" '(' expression ')' '{' { case-statement } '}'
	"SWITCH" '(' expression ')' '{' { case-statement } default-statement '}'

case-statement ::=
	"CASE" primary-expression ":" statements

default-statement ::=
	"DEFAULT" ":" statements

expression ::=
	primary-expression
	binary-expression ;

primary-expression ::=
	literal-expression
	function-call-expression
	assignment-expression
	variable-access-expression ;

literal-expression ::=
	bool
	char
	string
	number ;

function-call-expression ::=
	ident '(' callarguments ')' ;

assignment-expression ::=
	ident '=' expression ;

variable-access-expression ::=
	ident
	array-access-expression

array-access-expression ::=
	ident '[' expression ']' { '[' expression ']' } ;

bool ::=
	"TRUE" | "FALSE" ;

binary-expression ::=
	expression binary-operator expression ;

binary-operator ::=
	`'+' | '-' | '*' | '/' |
	'==' | '!=' | '>' | '<' | '<=' | '>=' |
	'&' | '|' | '&&' | '||' | '>>' | '<<' ;`

ident ::=
	ident-start-char { ident-continue-char } ;

ident-start-char ::=
	"a"..."z" | "A"..."Z" | "_" ;

ident-continue-char ::=
	ident-start-char | "-" | "0..9" ;

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

string ::=
	'"' { char }'"'
