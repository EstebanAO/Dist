grammar dist;

@header{
from Compiler import Compiler
c = Compiler()
id_arr = ''
quad_assign = ''
function_call = ''
dim_one = ''
dim_two = ''

}

dist                            : programa EOF {c.print_quad()} {c.write_quadruples()};
programa                        : PROGRAM ID {c.save_program_name($ID.text)} ';' ((varss| vars_arreglo) ';')* {c.generate_go_to_main()} funcion* MAIN {c.complete_go_to_main()} {c.switch_context('main')} {c.add_function_type('void')}bloque_local;
expresion                       : exp_and ('||'{c.push_operator('||')} exp_and)*;
exp_and                         : exp_comp ('&&' {c.push_operator('&&')} exp_comp)*{c.generate_operation_quadruple('||')};
rel_op                          :('<' | '>' | '!=' | '<=' | '>=' | '==');
exp_comp                        : exp ( rel_op {c.push_operator($rel_op.text)} exp {c.generate_operation_quadruple('>')})? {c.generate_operation_quadruple('&&')};
exp                             : termino (('+' {c.push_operator('+')} | '-'{c.push_operator('-')}) termino)*;
termino                         : factor (('*' {c.push_operator('*')} | '/' {c.push_operator('/')}) factor)* {c.generate_operation_quadruple('+')};
sign                            : ('+' | '-');
factor                          : ((sign? '(' {c.push_operator('(')} expresion ')'{c.change_sign($sign.text)}{c.pop_operator()}) | (sign? var_cte {c.change_sign($sign.text)})) {c.generate_operation_quadruple('*')};
var_cte                         : cte {c.push_constant_data($cte.text)} | ID {c.push_variable_data($ID.text)} | llamada_funcion | posicion_arreglo | llamada_funcion_especial;
cte                             : (CTE_I {c.current_cte_type = 'int'} | CTE_F {c.current_cte_type = 'float'} | CTE_C {c.current_cte_type = 'char'} | CTE_B {c.current_cte_type = 'bool'} | NULL {c.current_cte_type = 'null'});
lectura                         : READ '(' (posicion_arreglo {c.generate_read_array_quadruple()}) ')';
escritura                       : PRINT '(' (expresion | CTE_STRING {c.current_cte_type = 'str'}{c.push_constant_data($CTE_STRING.text)}) {c.generate_print_quadruple()} (',' (expresion | CTE_STRING{c.current_cte_type = 'str'}{c.push_constant_data($CTE_STRING.text)}){c.generate_print_quadruple()})* ')' {c.add_new_line()};
tipo                            : INT | FLOAT | CHAR | BOOL;
tipo_funcion                    : tipo | VOID;
varss                           : VAR ID {c.push_id($ID.text)}(',' ID {c.push_id($ID.text)})* ':' tipo {c.add_variables($tipo.text)};
returnn							            : RETURN expresion {c.generate_return_quadruple()};

un_parametro                    : '(' expresion ')';
dos_parametros                  : '(' expresion ',' expresion ')';
tres_parametros                 : '(' expresion ',' expresion ',' expresion ')';

llamada_funcion_especial        : (SIZE | VARIANCE | MODE | MEDIAN |
                                    EXP_GEOMETRIC | VAR_GEOMETRIC |
                                    PLOT_HISTOGRAM | EXP_BERNOULLI | VAR_BERNOULLI) un_parametro
                                    | (POW | SQRT | PROB | MOMENT | EXP_BINOMIAL |
                                    VAR_BINOMIAL | PROB_GEOMETRIC) dos_parametros |
                                    PROB_BINOMIAL tres_parametros;

llamada_funcion				    : ID {function_call = $ID.text} {c.generate_era_quadruple()} {c.add_fake_bottom()} '(' (expresion {c.assign_param_direction(function_call)} (',' expresion {c.assign_param_direction(function_call)})*)? ')'{c.generate_go_sub_quadruple(function_call)};

funcion                         :  FUN ID {c.switch_context($ID.text)} '(' 
                                    (ID {c.add_param($ID.text)}
                                        (('[' CTE_I {dim_one = $CTE_I.text } ']' '[' CTE_I {dim_two = $CTE_I.text }']' ':' tipo {c.add_array_two_dim(int(dim_one), int(dim_two), $tipo.text)} dimension_dos ) | ('[' CTE_I ']' ':' tipo {c.add_array_one_dim(int($CTE_I.text), $tipo.text)} dimension_uno ) | (':' tipo {c.add_type($tipo.text) })) 
                                        (',' ID {c.add_param($ID.text)} (('[' CTE_I {dim_one = $CTE_I.text } ']' '[' CTE_I {dim_two = $CTE_I.text }']' ':' tipo {c.add_array_two_dim(int(dim_one), int(dim_two), $tipo.text)} dimension_dos ) | ('[' CTE_I ']' ':' tipo {c.add_array_one_dim(int($CTE_I.text), $tipo.text)} dimension_uno ) | (':' tipo {c.add_type($tipo.text) })))* )? 
                                        ')' ':' tipo_funcion {c.add_function_type($tipo_funcion.text)} bloque_local {c.generate_end_proc()};

vars_arreglo                    : VAR ID {c.current_variable = $ID.text} (('[' CTE_I ']' ':' tipo {c.add_array_one_dim(int($CTE_I.text), $tipo.text)} dimension_uno ) | ('[' CTE_I {dim_one = $CTE_I.text } ']' '[' CTE_I {dim_two = $CTE_I.text } ']' ':' tipo {c.add_array_two_dim(int(dim_one), int(dim_two), $tipo.text)} dimension_dos ));
mult_cte                        : '{' cte {c.push_constant_data($cte.text)} (',' cte{c.push_constant_data($cte.text)} )* '}';
dimension_uno                   : ('=' mult_cte)?;
dimension_dos                   : ('=' '{' mult_cte (',' mult_cte )* '}' )?;

posicion_arreglo                : ID {c.id_assign = $ID.text} (('[' {c.add_fake_bottom()} exp ']' {c.access_array_dim_one($ID.text)}) | ('[' {c.add_fake_bottom()} exp {c.p_operators.pop()}']' '[' {c.add_fake_bottom()} exp ']'{c.access_array_dim_two($ID.text)}));

estatuto                        : (asignacion | condicion | while_cycle | escritura | lectura | llamada_funcion | llamada_funcion_especial | returnn) ';';

bloque_condicional              : '{' estatuto* '}';
bloque_local                    : '{' ((varss| vars_arreglo) ';')* estatuto* '}';
asignacion                      : (ID {quad_assign = c.get_variable($ID.text)} | posicion_arreglo {quad_assign = c.p_values.pop()} ) '=' expresion {c.generate_assign_quadruple(quad_assign)};

condicion                       : IF '(' expresion ')' {c.generate_go_to_f()} bloque_condicional (ELSE {c.generate_else_go_to()} bloque_condicional)? {c.complete_go_to_f()};
while_cycle                     : WHILE {c.add_breadcrumb()}'(' expresion ')' {c.generate_go_to_f()} bloque_condicional {c.end_of_while()};

/*
 * Lexer Rules
 */

 fragment LOWERCASE             : [a-z];
 fragment UPPERCASE             : [A-Z];
 fragment DIGIT                 : [0-9];

 CTE_F                          : (DIGIT)+ '.' (DIGIT)+;
 CTE_I                          : (DIGIT)+;
 CTE_C                          : '\'' .? '\'';
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

 COMMENT: '/*' .*? '*/' -> skip;
 LINE_COMMENT: '//' ~[\r\n]* -> skip;
