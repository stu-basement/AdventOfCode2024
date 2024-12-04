%{
#include "day3.tab.h"
#include <stdio.h>
#include <string.h>
int yyerror(char *sp);
extern FILE *yyin;
extern YYSTYPE yylval;
extern struct {
    int num1;
    int num2;
} current_mul;
%}

NUM [0-9]{1,3}

%%

"mul("{NUM}","{NUM}")"   { /* Match complete valid mul(X,Y) */
                          char *start = yytext + 4;  // skip "mul("
                          char *comma = strchr(start, ',');
                          *comma = '\0';
                          current_mul.num1 = atoi(start);
                          current_mul.num2 = atoi(comma + 1);
                          *comma = ',';
                          return MUL; 
                        }

"do()"                  { return DO; }
"don't()"              { return DONT; }
.|\n                   {  }

%%

int yywrap(void)
{
   return 1;
}   
