grammar dist;
 
@header{
from Compiler import Compiler
c = Compiler()
VARS = "vars"
}
 
dist                            : programa {print(c.functions)} EOF;
programa                        : PROGRAM ID ';' ((varss| vars_arreglo) ';')* funcion* MAIN bloque_local;
expresion                       : exp_and ('||' exp_and)*;
exp_and                         : exp_comp ('&&' exp_comp)*;
exp_comp                        : exp (('<' | '>' | '!=' | '<=' | '>=' | '==') exp)?;
exp                             : termino (('+' | '-') termino)*;
termino                         : factor (('*' | '/') factor)*;
factor                          : ('(' expresion ')') |                                                                                                   
                                  (('+' | '-')? var_cte);
var_cte                         : cte | ID | llamada_funcion | posicion_arreglo | llamada_funcion_especial;
cte                             : CTE_I | CTE_F | CTE_C | CTE_B | NULL;
lectura                         : READ '(' (ID | posicion_arreglo) ')';
escritura                       : PRINT '(' (expresion | CTE_STRING) (',' (expresion | CTE_STRING))* ')';
tipo                            : INT | FLOAT | CHAR | BOOL;
tipo_funcion                    : tipo | VOID;
varss                           : VAR ID {c.push_id($ID.text)} (',' ID {c.push_id($ID.text)})* ':' tipo {c.add_variables($tipo.text)};
returnn							            : RETURN expresion;

un_parametro                   : '(' expresion ')';
dos_parametros                  : '(' expresion ',' expresion ')';
tres_parametros                 : '(' expresion ',' expresion ',' expresion ')';

llamada_funcion_especial        : (SIZE | VARIANCE | MODE | MEDIAN |
                                    EXP_GEOMETRIC | VAR_GEOMETRIC |
                                    PLOT_HISTOGRAM | EXP_BERNOULLI | VAR_BERNOULLI) un_parametro
                                    | (POW | SQRT | PROB | MOMENT | EXP_BINOMIAL |
                                    VAR_BINOMIAL | PROB_GEOMETRIC) dos_parametros |
                                    PROB_BINOMIAL tres_parametros;

llamada_funcion					        : ID '(' expresion? (',' expresion)* ')';


funcion                         : FUN ID {c.switch_context($ID.text)} '(' ((ID ':' tipo) (',' ID ':' tipo)*)? ')' ':' tipo_funcion bloque_local;

vars_arreglo                    : VAR ID (('[' CTE_I ']' dimension_uno) | ('[' CTE_I ']' '[' CTE_I ']' dimension_dos ));
mult_cte                        : '{' cte (',' cte)* '}';
dimension_uno                   : ':' tipo '=' mult_cte;
dimension_dos                   : ':' tipo '=' '{' mult_cte (',' mult_cte)*  '}' ;
posicion_arreglo                : ID '[' exp ']' ('[' exp ']')?;

estatuto                        : (asignacion | condicion | while_cycle | escritura | lectura | llamada_funcion | llamada_funcion_especial | returnn) ';';

bloque_condicional              : '{' estatuto* '}';
bloque_local                    : '{' ((varss| vars_arreglo) ';')* estatuto* '}';
asignacion                      : (ID | posicion_arreglo) '=' expresion;

condicion                       : IF '(' expresion ')' bloque_condicional (ELSE bloque_condicional)?;
while_cycle                     : WHILE '(' expresion ')' bloque_condicional;


vars_arreglo                    : VAR ID '[' CET_I ']' (dimension_uno) | ('[' CET_I ']' dimension_dos) ';';
mult_cte                        : '{' cte (',' cte)* '}';
dimension_uno                   : ':' tipo '=' mult_cte;
dimension_dos                   : ':' tipo '=' '{' mult_cte (',' mult_cte)*  '}' ;
posicion_arreglo                : ID '[' exp ']' ('[' exp ']')?;

/*
 * Lexer Rules
 */

 fragment LOWERCASE             : [a-z];
 fragment UPPERCASE             : [A-Z];
 fragment DIGIT                 : [0-9];

 CTE_F                          : (DIGIT)+ '.' (DIGIT)+;
 CTE_I                          : (DIGIT)+;
 CTE_C                          : ('\'' LOWERCASE '\'') | ('\'' UPPERCASE '\'') | ('\'' DIGIT '\'');
 CTE_B                       	  : ('t' 'r' 'u' 'e') | ('f' 'a' 'l' 's' 'e');
 CTE_STRING                     : '"' .*? '"';
 NULL                           : 'n' 'u' 'l' 'l';

 INT                            : 'i' 'n' 't';
 FLOAT                          : 'f' 'l' 'o' 'a' 't';
 CHAR                           : 'c' 'h' 'a' 'r';
 BOOL                           : 'b' 'o' 'o' 'l';
 VOID                           : 'v' 'o' 'i' 'd';
 PRINT                          : 'p' 'r' 'i' 'n' 't';
 IF                             : 'i' 'f';
 ELSE                           : 'e' 'l' 's' 'e';
 WHILE                          : 'w' 'h' 'i' 'l' 'e';
 PROGRAM                        : 'p' 'r' 'o' 'g' 'r' 'a' 'm';
 VAR                            : 'v' 'a' 'r';
 MAIN                           : 'm' 'a' 'i' 'n';
 RETURN                         : 'r' 'e' 't' 'u' 'r' 'n';
 READ                           : 'r' 'e' 'a' 'd';
 FUN                            : 'f' 'u' 'n';

 SIZE                           : 's' 'i' 'z' 'e';
 POW                            : 'p' 'o' 'w';
 SQRT                           : 's' 'q' 'r' 't';
 MOMENT                         : 'm' 'o' 'm' 'e' 'n' 't';
 PROB                           : 'p' 'r' 'o' 'b';
 VARIANCE                       : 'v' 'a' 'r' 'i' 'a' 'n' 'c' 'e';
 MODE                           : 'm' 'o' 'd' 'e';
 MEDIAN                         : 'm' 'e' 'd' 'i' 'a' 'n';
 PLOT_HISTOGRAM                 : 'p' 'l' 'o' 't' '_' 'h' 'i' 's' 't' 'o' 'g' 'r' 'a' 'm';
 EXP_BERNOULLI                  : 'e' 'x' 'p' '_' 'b' 'e' 'r' 'n' 'o' 'u' 'l' 'l' 'i';
 VAR_BERNOULLI                  : 'v' 'a' 'r' '_' 'b' 'e' 'r' 'n' 'o' 'u' 'l' 'l' 'i';
 PROB_BINOMIAL                  : 'p' 'r' 'o' 'b' '_' 'b' 'i' 'n' 'o' 'm' 'i' 'a' 'l';
 EXP_BINOMIAL                   : 'e' 'x' 'p' '_' 'b' 'i' 'n' 'o' 'm' 'i' 'a' 'l';
 VAR_BINOMIAL                   : 'v' 'a' 'r' '_' 'b' 'i' 'n' 'o' 'm' 'i' 'a' 'l';
 PROB_GEOMETRIC                 : 'p' 'r' 'o' 'b' '_' 'g' 'e' 'o' 'm' 'e' 't' 'r' 'i' 'c';
 EXP_GEOMETRIC                  : 'e' 'x' 'p' '_' 'g' 'e' 'o' 'm' 'e' 't' 'r' 'i' 'c';
 VAR_GEOMETRIC                  : 'v' 'a' 'r' '_' 'g' 'e' 'o' 'm' 'e' 't' 'r' 'i' 'c';
 ID                             : (LOWERCASE)(UPPERCASE | LOWERCASE | DIGIT)*;

 NEWLINE                        : ('\r'? '\n' | '\r')+ -> skip;
 WHITESPACE                     : (' ' | '\t') -> skip;
