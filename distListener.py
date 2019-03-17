# Generated from dist.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .distParser import distParser
else:
    from distParser import distParser

	


# This class defines a complete listener for a parse tree produced by distParser.
class distListener(ParseTreeListener):

    # Enter a parse tree produced by distParser#dist.
    def enterDist(self, ctx:distParser.DistContext):
        pass

    # Exit a parse tree produced by distParser#dist.
    def exitDist(self, ctx:distParser.DistContext):
        pass


    # Enter a parse tree produced by distParser#programa.
    def enterPrograma(self, ctx:distParser.ProgramaContext):
        pass

    # Exit a parse tree produced by distParser#programa.
    def exitPrograma(self, ctx:distParser.ProgramaContext):
        pass


    # Enter a parse tree produced by distParser#expresion.
    def enterExpresion(self, ctx:distParser.ExpresionContext):
        pass

    # Exit a parse tree produced by distParser#expresion.
    def exitExpresion(self, ctx:distParser.ExpresionContext):
        pass


    # Enter a parse tree produced by distParser#exp_and.
    def enterExp_and(self, ctx:distParser.Exp_andContext):
        pass

    # Exit a parse tree produced by distParser#exp_and.
    def exitExp_and(self, ctx:distParser.Exp_andContext):
        pass


    # Enter a parse tree produced by distParser#exp_comp.
    def enterExp_comp(self, ctx:distParser.Exp_compContext):
        pass

    # Exit a parse tree produced by distParser#exp_comp.
    def exitExp_comp(self, ctx:distParser.Exp_compContext):
        pass


    # Enter a parse tree produced by distParser#exp.
    def enterExp(self, ctx:distParser.ExpContext):
        pass

    # Exit a parse tree produced by distParser#exp.
    def exitExp(self, ctx:distParser.ExpContext):
        pass


    # Enter a parse tree produced by distParser#termino.
    def enterTermino(self, ctx:distParser.TerminoContext):
        pass

    # Exit a parse tree produced by distParser#termino.
    def exitTermino(self, ctx:distParser.TerminoContext):
        pass


    # Enter a parse tree produced by distParser#factor.
    def enterFactor(self, ctx:distParser.FactorContext):
        pass

    # Exit a parse tree produced by distParser#factor.
    def exitFactor(self, ctx:distParser.FactorContext):
        pass


    # Enter a parse tree produced by distParser#var_cte.
    def enterVar_cte(self, ctx:distParser.Var_cteContext):
        pass

    # Exit a parse tree produced by distParser#var_cte.
    def exitVar_cte(self, ctx:distParser.Var_cteContext):
        pass


    # Enter a parse tree produced by distParser#cte.
    def enterCte(self, ctx:distParser.CteContext):
        pass

    # Exit a parse tree produced by distParser#cte.
    def exitCte(self, ctx:distParser.CteContext):
        pass


    # Enter a parse tree produced by distParser#lectura.
    def enterLectura(self, ctx:distParser.LecturaContext):
        pass

    # Exit a parse tree produced by distParser#lectura.
    def exitLectura(self, ctx:distParser.LecturaContext):
        pass


    # Enter a parse tree produced by distParser#escritura.
    def enterEscritura(self, ctx:distParser.EscrituraContext):
        pass

    # Exit a parse tree produced by distParser#escritura.
    def exitEscritura(self, ctx:distParser.EscrituraContext):
        pass


    # Enter a parse tree produced by distParser#tipo.
    def enterTipo(self, ctx:distParser.TipoContext):
        pass

    # Exit a parse tree produced by distParser#tipo.
    def exitTipo(self, ctx:distParser.TipoContext):
        pass


    # Enter a parse tree produced by distParser#tipo_funcion.
    def enterTipo_funcion(self, ctx:distParser.Tipo_funcionContext):
        pass

    # Exit a parse tree produced by distParser#tipo_funcion.
    def exitTipo_funcion(self, ctx:distParser.Tipo_funcionContext):
        pass


    # Enter a parse tree produced by distParser#varss.
    def enterVarss(self, ctx:distParser.VarssContext):
        pass

    # Exit a parse tree produced by distParser#varss.
    def exitVarss(self, ctx:distParser.VarssContext):
        pass


    # Enter a parse tree produced by distParser#returnn.
    def enterReturnn(self, ctx:distParser.ReturnnContext):
        pass

    # Exit a parse tree produced by distParser#returnn.
    def exitReturnn(self, ctx:distParser.ReturnnContext):
        pass


    # Enter a parse tree produced by distParser#un_parametro.
    def enterUn_parametro(self, ctx:distParser.Un_parametroContext):
        pass

    # Exit a parse tree produced by distParser#un_parametro.
    def exitUn_parametro(self, ctx:distParser.Un_parametroContext):
        pass


    # Enter a parse tree produced by distParser#dos_parametros.
    def enterDos_parametros(self, ctx:distParser.Dos_parametrosContext):
        pass

    # Exit a parse tree produced by distParser#dos_parametros.
    def exitDos_parametros(self, ctx:distParser.Dos_parametrosContext):
        pass


    # Enter a parse tree produced by distParser#tres_parametros.
    def enterTres_parametros(self, ctx:distParser.Tres_parametrosContext):
        pass

    # Exit a parse tree produced by distParser#tres_parametros.
    def exitTres_parametros(self, ctx:distParser.Tres_parametrosContext):
        pass


    # Enter a parse tree produced by distParser#llamada_funcion_especial.
    def enterLlamada_funcion_especial(self, ctx:distParser.Llamada_funcion_especialContext):
        pass

    # Exit a parse tree produced by distParser#llamada_funcion_especial.
    def exitLlamada_funcion_especial(self, ctx:distParser.Llamada_funcion_especialContext):
        pass


    # Enter a parse tree produced by distParser#llamada_funcion.
    def enterLlamada_funcion(self, ctx:distParser.Llamada_funcionContext):
        pass

    # Exit a parse tree produced by distParser#llamada_funcion.
    def exitLlamada_funcion(self, ctx:distParser.Llamada_funcionContext):
        pass


    # Enter a parse tree produced by distParser#funcion.
    def enterFuncion(self, ctx:distParser.FuncionContext):
        pass

    # Exit a parse tree produced by distParser#funcion.
    def exitFuncion(self, ctx:distParser.FuncionContext):
        pass


    # Enter a parse tree produced by distParser#vars_arreglo.
    def enterVars_arreglo(self, ctx:distParser.Vars_arregloContext):
        pass

    # Exit a parse tree produced by distParser#vars_arreglo.
    def exitVars_arreglo(self, ctx:distParser.Vars_arregloContext):
        pass


    # Enter a parse tree produced by distParser#mult_cte.
    def enterMult_cte(self, ctx:distParser.Mult_cteContext):
        pass

    # Exit a parse tree produced by distParser#mult_cte.
    def exitMult_cte(self, ctx:distParser.Mult_cteContext):
        pass


    # Enter a parse tree produced by distParser#dimension_uno.
    def enterDimension_uno(self, ctx:distParser.Dimension_unoContext):
        pass

    # Exit a parse tree produced by distParser#dimension_uno.
    def exitDimension_uno(self, ctx:distParser.Dimension_unoContext):
        pass


    # Enter a parse tree produced by distParser#dimension_dos.
    def enterDimension_dos(self, ctx:distParser.Dimension_dosContext):
        pass

    # Exit a parse tree produced by distParser#dimension_dos.
    def exitDimension_dos(self, ctx:distParser.Dimension_dosContext):
        pass


    # Enter a parse tree produced by distParser#posicion_arreglo.
    def enterPosicion_arreglo(self, ctx:distParser.Posicion_arregloContext):
        pass

    # Exit a parse tree produced by distParser#posicion_arreglo.
    def exitPosicion_arreglo(self, ctx:distParser.Posicion_arregloContext):
        pass


    # Enter a parse tree produced by distParser#estatuto.
    def enterEstatuto(self, ctx:distParser.EstatutoContext):
        pass

    # Exit a parse tree produced by distParser#estatuto.
    def exitEstatuto(self, ctx:distParser.EstatutoContext):
        pass


    # Enter a parse tree produced by distParser#bloque_condicional.
    def enterBloque_condicional(self, ctx:distParser.Bloque_condicionalContext):
        pass

    # Exit a parse tree produced by distParser#bloque_condicional.
    def exitBloque_condicional(self, ctx:distParser.Bloque_condicionalContext):
        pass


    # Enter a parse tree produced by distParser#bloque_local.
    def enterBloque_local(self, ctx:distParser.Bloque_localContext):
        pass

    # Exit a parse tree produced by distParser#bloque_local.
    def exitBloque_local(self, ctx:distParser.Bloque_localContext):
        pass


    # Enter a parse tree produced by distParser#asignacion.
    def enterAsignacion(self, ctx:distParser.AsignacionContext):
        pass

    # Exit a parse tree produced by distParser#asignacion.
    def exitAsignacion(self, ctx:distParser.AsignacionContext):
        pass


    # Enter a parse tree produced by distParser#condicion.
    def enterCondicion(self, ctx:distParser.CondicionContext):
        pass

    # Exit a parse tree produced by distParser#condicion.
    def exitCondicion(self, ctx:distParser.CondicionContext):
        pass


    # Enter a parse tree produced by distParser#while_cycle.
    def enterWhile_cycle(self, ctx:distParser.While_cycleContext):
        pass

    # Exit a parse tree produced by distParser#while_cycle.
    def exitWhile_cycle(self, ctx:distParser.While_cycleContext):
        pass


