%{
#include <stdio.h>
int yylex(void);
int yyerror(const char *s);
extern FILE *yyin;

int enabled = 1;
int total = 0;
int totalDo = 0;
int totalDont = 0;
int totalMul = 0;

struct {
    int num1;
    int num2;
} current_mul;

%}

%union {
    int num1;
    int num2;
}

%token <num1> NUMBER
%token <num1> MUL
%token DO
%token DONT

%%

input:  /* empty input */
    | input line
    ;

line:   multiplication
    | toggle
    | error {yyerrok;}
    ;

multiplication:  MUL
        {if (enabled) {
            totalMul++;
            total += (current_mul.num1 * current_mul.num2);
         }
        }
    ;

toggle: DO {enabled = 1; totalDo++;}
    | DONT {enabled = 0; totalDont++;}
    ;

%%

int yyerror(const char *s) {
    return 0;
}

int main(int argc, char **argv) {
    if (argc > 1) {
        yyin = fopen(argv[1], "r");
    }
    yyparse();
    printf("Total: %d\n", total);
    return 0;
}
