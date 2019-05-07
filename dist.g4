grammar dist;

@header{
from Compiler import Compiler
import tokens
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
rel_op                          : ('<' | '>' | '!=' | '<=' | '>=' | '==');
exp_comp                        : exp ( rel_op {c.push_operator($rel_op.text)} exp {c.generate_operation_quadruple('>')})? {c.generate_operation_quadruple('&&')};
exp                             : termino (('+' {c.push_operator('+')} | '-'{c.push_operator('-')}) termino)*;
termino                         : factor (('*' {c.push_operator('*')} | '/' {c.push_operator('/')}) factor)* {c.generate_operation_quadruple('+')};
sign                            : ('+' | '-');
factor                          : ((sign? '(' {c.push_operator('(')} expresion ')'{c.change_sign($sign.text)}{c.pop_operator()}) | (sign? var_cte {c.change_sign($sign.text)})) {c.generate_operation_quadruple('*')};
var_cte                         : cte {c.push_constant_data($cte.text)} | ID {c.push_variable_data($ID.text)} | llamada_funcion | posicion_arreglo | llamada_funcion_especial;
cte                             : (CTE_I {c.current_cte_type = 'int'} | CTE_F {c.current_cte_type = 'float'} | CTE_C {c.current_cte_type = 'char'} | CTE_B {c.current_cte_type = 'bool'} | NULL {c.current_cte_type = 'null'});
lectura                         : READ '(' ((ID {c.generate_read_quadruple($ID.text)}) | (posicion_arreglo {c.generate_read_array_quadruple()})) ')';
escritura                       : PRINT '(' (expresion | CTE_STRING {c.current_cte_type = 'str'}{c.push_constant_data($CTE_STRING.text)}) {c.generate_print_quadruple()} (',' (expresion | CTE_STRING{c.current_cte_type = 'str'}{c.push_constant_data($CTE_STRING.text)}){c.generate_print_quadruple()})* ')';
escritura_nueva_linea           : PRINT_NEW_LINE '('( (expresion | CTE_STRING {c.current_cte_type = 'str'}{c.push_constant_data($CTE_STRING.text)}) {c.generate_print_quadruple()} (',' (expresion | CTE_STRING{c.current_cte_type = 'str'}{c.push_constant_data($CTE_STRING.text)}){c.generate_print_quadruple()})* )? ')'{c.add_new_line()};
tipo                            : INT | FLOAT | CHAR | BOOL;
tipo_funcion                    : tipo | VOID;
varss                           : VAR ID {c.push_id($ID.text)}(',' ID {c.push_id($ID.text)})* ':' tipo {c.add_variables($tipo.text)};
returnn							            : RETURN expresion {c.generate_return_quadruple()};

llamada_pow                     : POW '(' expresion {c.verify_float()}',' expresion {c.verify_float()}')' {c.generate_quadruple_special_func(tokens.POW)};
llamada_sqrt                    : SQRT '(' expresion {c.verify_float()}',' expresion {c.verify_float()}')' {c.generate_quadruple_special_func(tokens.SQRT)};
llamada_mode                    : MODE '(' expresion {c.verify_array()} {c.verify_int()}')' {c.generate_quadruple_special_func(tokens.MODE)};
llabada_prob                    : PROB '(' expresion {c.verify_array()} {c.verify_int()} ',' expresion {c.verify_int()} ')' {c.generate_quadruple_special_func(tokens.PROB)};
llamada_moment                  : MOMENT '(' expresion {c.verify_array()} {c.verify_int()} ',' expresion {c.verify_int()} ')' {c.generate_quadruple_special_func(tokens.MOMENT)};
llamada_median                  : MEDIAN '(' expresion {c.verify_array()} {c.verify_int()}')' {c.generate_quadruple_special_func(tokens.MEDIAN)};
llamada_var                     : VAR '(' expresion {c.verify_array()} {c.verify_int()}')' {c.generate_quadruple_special_func(tokens.VAR)};
llamada_exp_bernoulli           : EXP_BERNOULLI '(' expresion {c.verify_float()}')' {c.generate_quadruple_special_func(tokens.EXP_BERNOULLI)};
llamada_var_bernoulli           : VAR_BERNOULLI '(' expresion {c.verify_float()}')' {c.generate_quadruple_special_func(tokens.VAR_BERNOULLI)};
llamada_prob_binomial           : PROB_BINOMIAL'(' expresion {c.verify_float()}',' expresion {c.verify_int()}',' expresion {c.verify_int()}')' {c.generate_quadruple_special_func(tokens.PROB_BINOMIAL)};
llamada_exp_binomial            : EXP_BINOMIAL '(' expresion {c.verify_float()}',' expresion {c.verify_int()}')' {c.generate_quadruple_special_func(tokens.EXP_BINOMIAL)} ;
llamada_var_binomial            : VAR_BINOMIAL '(' expresion {c.verify_float()}',' expresion {c.verify_int()}')' {c.generate_quadruple_special_func(tokens.VAR_BINOMIAL)} ;
llamada_prob_geometric          : PROB_GEOMETRIC '(' expresion {c.verify_float()}',' expresion {c.verify_int()}')' {c.generate_quadruple_special_func(tokens.PROB_GEOMETRIC)} ;
llamada_exp_geometric           : EXP_GEOMETRIC '(' expresion {c.verify_float()}')' {c.generate_quadruple_special_func(tokens.EXP_GEOMETRIC)};
llamada_var_geometric           : VAR_GEOMETRIC '(' expresion {c.verify_float()}')' {c.generate_quadruple_special_func(tokens.VAR_GEOMETRIC)};
llamada_plot_histogram          : PLOT_HISTOGRAM '(' expresion {c.verify_array()} {c.verify_int()}')' {c.generate_quadruple_special_func(tokens.PLOT_HISTOGRAM)};

llamada_funcion_especial        : {c.add_fake_bottom()} (llamada_pow | llamada_mode | llamada_sqrt | llabada_prob | llamada_moment | llamada_median | llamada_var | llamada_exp_bernoulli | llamada_var_bernoulli | llamada_prob_binomial | llamada_exp_binomial | llamada_var_binomial | llamada_prob_geometric | llamada_exp_geometric | llamada_var_geometric | llamada_plot_histogram) {c.remove_fake_bottom()};

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

posicion_arreglo                : ID {c.id_assign = $ID.text} (('[' {c.add_fake_bottom()} exp {c.verify_pos_type()} ']' {c.access_array_dim_one($ID.text)}) | ('[' {c.add_fake_bottom()} exp {c.verify_pos_type()}{c.p_operators.pop()}']' '[' {c.add_fake_bottom()} exp {c.verify_pos_type()}']'{c.access_array_dim_two($ID.text)}));

estatuto                        : (asignacion | condicion | while_cycle | escritura | escritura_nueva_linea | lectura | llamada_funcion | llamada_funcion_especial | returnn) ';';

bloque_condicional              : '{' estatuto* '}';
bloque_local                    : '{' (((varss| vars_arreglo) ';') | estatuto)* '}';
asignacion                      : (ID {quad_assign = c.get_variable($ID.text)} | posicion_arreglo {quad_assign = c.p_values.pop()} ) '=' expresion {c.generate_assign_quadruple(quad_assign)};

condicion                       : IF '(' expresion ')' {c.generate_go_to_f()} bloque_condicional (ELSE {c.generate_else_go_to()} bloque_condicional)? {c.complete_go_to_f()};
while_cycle                     : WHILE {c.add_breadcrumb()}'(' expresion ')' {c.generate_go_to_f()} bloque_condicional {c.end_of_while()};

/*
 * Lexer Rules
 */

 fragment LOWERCASE             : [a-z];
 fragment UPPERCASE             : [A-Z] ;
 fragment DIGIT                 : [0-9];

 CTE_F                          : (DIGIT)+ '.' (DIGIT)+;
 CTE_I                          : (DIGIT)+;
 CTE_C                          : '\'' .? '\'';
 CTE_B                       	  : ('true') | ('false');
 CTE_STRING                     : '"' .*? '"';
 NULL                           : 'null';

 INT                            : 'int';
 FLOAT                          : 'float';
 CHAR                           : 'char';
 BOOL                           : 'bool';
 VOID                           : 'void';
 PRINT                          : 'print';
 PRINT_NEW_LINE                 : 'println';
 IF                             : 'if';
 ELSE                           : 'else';
 WHILE                          : 'while';
 PROGRAM                        : 'program';
 VAR                            : 'var';
 MAIN                           : 'main';
 RETURN                         : 'return';
 READ                           : 'read';
 FUN                            : 'fun';

 SIZE                           : 'size';
 POW                            : 'pow';
 SQRT                           : 'sqrt';
 MOMENT                         : 'moment';
 PROB                           : 'prob';
 VARIANCE                       : 'variance';
 MODE                           : 'mode';
 MEDIAN                         : 'median';
 PLOT_HISTOGRAM                 : 'plot_histogram';
 EXP_BERNOULLI                  : 'exp_bernoulli';
 VAR_BERNOULLI                  : 'var_bernoulli';
 PROB_BINOMIAL                  : 'prob_binomial';
 EXP_BINOMIAL                   : 'exp_binomial';
 VAR_BINOMIAL                   : 'var_binomial';
 PROB_GEOMETRIC                 : 'prob_geometric';
 EXP_GEOMETRIC                  : 'exp_geometric';
 VAR_GEOMETRIC                  : 'var_geometric';

 ID                             : (LOWERCASE | UPPERCASE)(UPPERCASE | LOWERCASE | DIGIT | '_' )*;

 NEWLINE                        : ('\r'? '\n' | '\r')+ -> skip;
 WHITESPACE                     : (' ' | '\t') -> skip;

 COMMENT: '/*' .*? '*/' -> skip;
 LINE_COMMENT: '//' ~[\r\n]* -> skip;
