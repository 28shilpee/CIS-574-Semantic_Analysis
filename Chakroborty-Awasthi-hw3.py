# -------------------------------------------------------------------------
# chakroborty_awasthi.py: Starter code for DLang Semantic Analyzer
# Run with source file 
# -------------------------------------------------------------------------
import sys
from sly import Lexer, Parser
import traceback

class SymbolTable:
    
    def __init__(self):
        self.table = []
    
    def add_name(self,name):
        '''Insert a new identified to the symbol table'''
        new_entry = {}
        new_entry['name'] = name 
        self.table.append(new_entry)
        
    def add_type(self,name,typee):
        '''Insert type of an identifier to the symbol table'''
        for i in range(len(self.table)):
            if self.table[i]['name'] == name:
                self.table[i]['type'] = typee 
    
    def add_formals(self,name,formalVar):
        '''Insert formals (parameters) of a function to the symbol table'''
        for i in range(len(self.table)):
            if self.table[i]['name'] == name:
                if 'formals' in self.table[i].keys():
                    self.table[i]['formals'].append(formalVar)
                else:
                    self.table[i]['formals'] = []
                    self.table[i]['formals'].append(formalVar)
    
    def get_formals(self,symbol):
        '''Get formals of a function symbol'''
        for elt in self.table:
            if elt['name'] == symbol:
                if 'formals' in elt.keys():
                    return elt['formals']
        return [] # symbol not found or formals not found
    
    def insert_value(self,name,value):
        '''Insert a value of symbol to the symbol table'''
        for i in range(len(self.table)):
            if self.table[i]['name'] == name:
                self.table[i]['value'] = value 
    
    def lookup_name(self,name):
        '''Check whether an idenfifier name exists in symbol table'''
        for elt in self.table:
            if elt['name'] == name:
                return 1
        return 0
    
    def get_type(self,symbol):
        '''Get the type of a symbol'''
        for elt in self.table:
            if elt['name'] == symbol:
                if 'type' in elt.keys():
                    return elt['type']
        return 0 # symbol not found
    
    def get_value(self,symbol,typee):
        '''Get the type of a symbol'''
        for elt in self.table:
            if elt['name'] == symbol and elt['type'] == typee:
                return elt['value']
        return 0 # symbol is not found

# global object that instantiates symbol table: use this to insert, get, loookup, ...
tab = SymbolTable()

class DLangLexer(Lexer):

    
    # Define names of tokens
    tokens ={LE, GE, EQ, NE, AND, OR, INT, DOUBLE, STRING, IDENTIFIER, NOTHING, INTK, DOUBLEK, BOOL, BOOLK, STRINGK, NULL, FOR, WHILE, IF, ELSE, RETURN, BREAK, OUTPUT, INPUTINT, INPUTLINE}
    
    # Single-character literals can be recognized without token names
    # If you use separate tokens for each literal, that is fine too
    literals = {'+', '-', '*', '/', '%', '<', '>', '=','!', ';', ',', '.', '[', ']','(',')','{','}'}
    
    # Specify things to ignore
    ignore = ' \t\r' # space, tab, and carriage return
    ignore_comment1= r'\/\*[^"]*\*\/' # c-style multi-line comment (note: test with input from file)
    ignore_comment = r'\/\/.*' # single line comment
    ignore_newline=r'\n+' # end of line


    # Specify REs for each token
    STRING = r'\"(.)*\"'
    DOUBLE = r'[0-9]+\.[0-9]*([E][+-]?\d+)?'
    INT = r'[0-9]+'
    EQ = r'=='
    NE = r'!='
    LE = r'<='
    GE = r'>='
    AND = r'&&' 
    OR =  r'\|\|'
    IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]{0,39}'
    # IDENTIFIER lexemes overlap with keywords.
    # To avoid confusion, we do token remaping.
    # Alternatively, you can specify each keyword before IDENTIFIER
    IDENTIFIER['nothing'] = NOTHING
    IDENTIFIER['int'] = INTK
    IDENTIFIER['double'] = DOUBLEK
    IDENTIFIER['string'] = STRINGK
    IDENTIFIER['bool'] = BOOLK
    IDENTIFIER['True'] = BOOL
    IDENTIFIER['False'] = BOOL
    IDENTIFIER['null'] = NULL
    IDENTIFIER['for'] = FOR
    IDENTIFIER['while'] = WHILE
    IDENTIFIER['if'] = IF
    IDENTIFIER['else'] = ELSE
    IDENTIFIER['return'] = RETURN
    IDENTIFIER['break'] = BREAK
    IDENTIFIER['Output'] = OUTPUT
    IDENTIFIER['InputInt'] = INPUTINT
    IDENTIFIER['InputLine'] = INPUTLINE
    

    def error(self,t):
        print ("Invalid character '%s'" % t.value[0])
        self.index+=1


class DLangParser(Parser):
    
    # Parser log file
    debugfile ='dlang-parser.log'

    # Fetch tokens from the lexer
    tokens = DLangLexer.tokens
    
    def Eval_const(self, param):
        # find the type of a constant value
        try:
            int(param)
            return 'int'
        except:
            try:
                float(param)
                return 'double'
            except:
                try:
                    bool(param)
                    return 'bool'
                except:
                    if param != '':
                        return 'string'
                    else:
                        return "Null"

    precedence = (
        ('nonassoc', EQ, NE, LE, GE, AND, OR, '<', '>'),
        ('left', '+', '-'),
        ('left', '*', '/', '%'),
        ('nonassoc', '=')
        )   

    def __init__(self):
        self.IDENTIFIERs = { }
        
    
    def semantic_error(self,msg):
        print ('\n Semantic Error:',msg)
    
        
    # Program ->Decl+
    @_('Decl DeclRest', 'Epsilon')
    def Program(self, p):
        print ('\n Parsing completed Successfully!\n')
        return p

    @_('Decl DeclRest', 'Epsilon')
    def DeclRest(self, p):
        return p

    # Decl ->VariableDecl
    @_('VariableDecl')
    def Decl(self, p):
        return p

    # Decl ->Stmt
    @_('Stmt')
    def Decl(self, p):
        return p


    # Decl -> FunctionDecl
    @_('FunctionDecl')
    def Decl(self, p):
        return p


    @_(' Variable ";" ')
    def VariableDecl(self, p):
        return p

    @_('Type IDENTIFIER')
    def Variable(self, p):
        # ToDo: here add the type of each identifier to the symbol table
        if tab.lookup_name(p.IDENTIFIER) == 1:
            tab.add_type(p.IDENTIFIER, p.Type)
        else:
            tab.add_name(p.IDENTIFIER)
            tab.add_type(p.IDENTIFIER, p.Type)
        return p

    @_('INTK', 'DOUBLEK', 'BOOLK','STRINGK')
    def Type(self, p):
        return p

    def Eval_ReturnStmt(self, return_stmt):
        # evaluating the types of the return statements
        for t in return_stmt:
            if 'Expr' in t:
                type = self.eval_Expr_TypeOnly(t)
                if isinstance(type, tuple):
                    return type[1]
                else:
                    return type
        return

    # FunctionDecl -> Type ident ( Formals ) StmtBlock 
    @_('Variable "(" Formals ")" StmtBlock')
    def FunctionDecl(self, p):
        # ToDo: here check if returned value matches the return type
        function_type = (p.Variable[1])[1]
        function_name = p.Variable[2]

        # store formals in symbol table
        def store_formals(formals):
            for item in formals:
                if isinstance(item, tuple):
                    store_formals(item)
                else:
                    if item == 'Variable':
                        tab.add_formals(p.Variable[2], formals[1][1])

        store_formals(p.Formals)

        # find return statements in function declaration
        return_statements = []

        def find_return_statements(item, return_statements):
            for element in item:
                if isinstance(element, tuple):
                    find_return_statements(element, return_statements)
                else:
                    if element == 'ReturnStmt':
                        return_statements.append(item)

        find_return_statements(p.StmtBlock, return_statements)

        # test type match to return statements
        for return_stmt in return_statements:
            value_type = self.Eval_ReturnStmt(return_stmt)
            if not (function_type == value_type or (function_type == 'double' and value_type == 'int')):
                self.semantic_error("Function " + str(function_name) + " return type " + str(function_type) +
                                    " does not match returned variable/value type " + str(value_type))
        return p

    # FunctionDecl -> nothing ident ( Formals ) StmtBlock
    @_('NOTHING IDENTIFIER "(" Formals ")" StmtBlock')
    def FunctionDecl(self, p):
        return p

    # Formals -> Variable+,|ε
    @_('Variable VariableRest', 'Epsilon')
    def Formals(self, p):
        return p

    @_(' "," Variable VariableRest', 'Epsilon')
    def VariableRest(self, p):
        return p
   

    @_('"{" "}"', ' "{" VariableDecl "}" ', ' "{" VariableDecl VariableDeclRest "}" ', ' "{" Stmt "}" ', ' "{" Stmt StmtRest "}" ', ' "{" VariableDecl VariableDeclRest Stmt StmtRest  "}" ' )
    def StmtBlock(self, p):
        return p

    @_('VariableDecl VariableDeclRest', 'Epsilon')
    def VariableDeclRest(self, p):
        return p 

    @_('Stmt StmtRest', 'Epsilon')
    def StmtRest(self, p):
        return p 

    # Stmt can be many things    
    @_('Expr ";" ',' ";" ','IfStmt','WhileStmt', 'ForStmt', 'BreakStmt','ReturnStmt','OutputStmt','StmtBlock')
    def Stmt(self, p):
        return p

    # if ( Expr ) Stmt <else Stmt>
    @_('IF "(" Expr ")" Stmt IfRest' )
    def IfStmt(self, p):
        return p 

    @_('ELSE Stmt','Epsilon' )
    def IfRest(self, p):
        return p

    # while ( Expr ) Stmt
    @_('WHILE "(" Expr ")" Stmt' )
    def WhileStmt(self, p):
        return p

    # for ( <Expr> ; Expr ; <Expr> ) Stmt
    @_('FOR "(" Expr ";" Expr ";" Expr ")" Stmt')
    def ForStmt(self, p):
        return p 

    # return <Expr> ;
    @_('RETURN Expr ";" ', 'RETURN ";"')
    def ReturnStmt(self, p):
        return p

    # break ;
    @_('BREAK ";" ')
    def BreakStmt(self, p):
        print ('BreakStmt')
        return p

   # Output ( Expr+, ) ;     
    @_('OUTPUT "(" Expr ExprRest ")" ";" ')
    def OutputStmt(self, p):
        return p

    @_(' "," Expr ExprRest', 'Epsilon')
    def ExprRest(self, p):
        return p

    @_('"!" Expr','IDENTIFIER','Constant','Call' ,' "("  Expr ")" ', '"-" Expr','INPUTINT "(" ")"', 'INPUTLINE "(" ")"')
    def Expr(self, p):
        return p

    def eval_Expr_TypeOnly(self, Expr):
        # Evaluating the types only of the expression, useful for formal variables and when values unassigned
        if(len(Expr) <= 2):
            if(Expr[0] == 'Constant'):
                typec = self.Eval_const(Expr)
                if typec == 'int':
                    return typec
                elif typec == 'double':
                    return typec
                if typec == 'bool':
                    return typec, bool(Expr[1])
                if typec == 'string':
                    return typec
                if typec == 'NULL':
                    return typec
                else:
                    return tab.get_type(Expr[1])
            try:
                x1 = Expr[1][1]
                type_x1 = tab.get_type(x1)[1]
                x2 = Expr[3][1]
                type_x2 = tab.get_type(x2)[1]
                if((type_x1 == 'double' and type_x2 == 'int') or (type_x1 == 'int' and type_x2 == 'double')):
                    # if int and double then result is double
                    return 'double'
                if(type_x1 != type_x2):
                    self.semantic_error("Type mismatch: " + str(type_x1) + " and " + str(type_x2))
                else:
                    return type_x1
            except Exception as e:
                return 'Null', 0

    def eval_Expr(self, Expr):
        # evaluate an expression and return type and value, useful when variables instaniated and function calls
        if(len(Expr) <= 2):
            if(Expr[0] == 'Constant'):
                typec = self.Eval_const(Expr)
                if typec == 'int':
                    return typec, int(Expr[1])
                elif typec == 'double':
                    return typec, float(Expr[1])
                if typec == 'bool':
                    return typec, bool(Expr[1])
                if typec == 'string':
                    return typec, str(Expr[1])
                if typec == 'NULL':
                    return typec, 0
                else:
                    return tab.get_type(Expr[1]) , tab.get_value(Expr[1],tab.get_type(Expr[1]))
            try:
                x1 = Expr[1][1]
                type_x1 = tab.get_type(x1)[1]
                val_x1 = tab.get_value(x1,tab.get_type(x1))
                x2 = Expr[3][1]
                type_x2 = tab.get_type(x2)[1]
                val_x2 = tab.get_value(x2,tab.get_type(x2))
                if(type_x1 == 'double' or type_x2 == 'double'):
                    # converting both variables to double to ensure correct type
                    tab.add_type(x1,'double')
                    type_x1='double'
                    tab.add_type(x2,'double')
                    type_x2 = 'double'
                if(type_x1 != type_x2):
                    self.semantic_error("Type mismatch: "+str(type_x1)+" and "+str(type_x2))
                if Expr[2] == "+":
                    return type_x1 , val_x1 + val_x2
                if Expr[2] == "-":
                    return type_x1 , val_x1 - val_x2
                if Expr[2] == "*":
                    return type_x1 , val_x1 * val_x2
                if Expr[2] == "/":
                    return type_x1 , val_x1 / val_x2
                if Expr[2] == "%":
                    return type_x1 , val_x1 % val_x2
                if Expr[2] == "<":
                    return 'bool' , val_x1 < val_x2
                if Expr[2] == "LE":
                    return 'bool', val_x1 <= val_x2
                if Expr[2] == ">":
                    return 'bool', val_x2 > val_x2
                if Expr[2] == "GE":
                    return 'bool', val_x1 >= val_x2
                if Expr[2] == "EQ":
                    return 'bool', val_x1 == val_x2
                if Expr[2] == "AND":
                    return 'bool', val_x1 and val_x2
                if Expr[2] == "OR":
                    return 'bool', val_x1 or val_x2
            except Exception as e:
                return self.eval_Expr_TypeOnly(Expr),"NoVAL--"

    @_('Expr "+" Expr', 'Expr "-" Expr', 'Expr "*" Expr', 'Expr "/" Expr', 'Expr "%" Expr', 'Expr "<" Expr', 'Expr LE Expr', 'Expr ">" Expr','Expr GE Expr', 'Expr EQ Expr', 'Expr  NE Expr', 'Expr AND Expr', 'Expr OR Expr')
    def Expr(self, p):
        # ToDo: here check if types of operands are compatible
        type_first_operand = self.eval_Expr_TypeOnly(p[0])
        type_second_operand = self.eval_Expr_TypeOnly(p[2])
        
        if p[1] in ["+", "-", "/", "*", "%", "<", ">", "LE", "GE", "EQ"]:
            if(type_first_operand and type_second_operand):
                if not ((type_first_operand[1] == 'double' and type_second_operand[1] == 'int') or 
                        (type_first_operand[1] == 'int' and type_second_operand[1] == 'double') or 
                        (type_first_operand[1] == type_second_operand[1])):
                    self.semantic_error("Type mismatch between " + str(type_first_operand[1]) + " and " + str(type_second_operand[1]))
        
        if p[1] in ["AND", "OR"]:
            if not (type_first_operand[1] == type_second_operand[1] == 'bool'):
                self.semantic_error("Type mismatch between " + str(type_first_operand[1]) + " and " + str(type_second_operand[1]))
        
        return p

    @_('IDENTIFIER "=" Expr')
    def Expr(self, p):
        # ToDo: here check if the identifier has been declared before
        if tab.lookup_name(p.IDENTIFIER) == 0:
            self.semantic_error('Undeclared Identifier')
        
        # add the value of a constant to the symbol table
        if isinstance(p[2], tuple):
            if p[2][1][0] == 'Constant':
                identifier_type = tab.get_type(p.IDENTIFIER)[1]
                try:
                    constant_value = self.Eval_const(p[2][1][1])
                    if identifier_type == 'int' and constant_value == 'int':
                        tab.insert_value(p.IDENTIFIER, int(p[2][1][1]))
                    elif identifier_type == 'double' and constant_value == 'double':
                        tab.insert_value(p.IDENTIFIER, float(p[2][1][1]))
                    elif identifier_type == 'string' and constant_value == 'string':
                        tab.insert_value(p.IDENTIFIER, str(p[2][1][1]))
                    elif identifier_type == 'bool' and constant_value == 'bool':
                        tab.insert_value(p.IDENTIFIER, bool(p[2][1][1]))
                    else:
                        tab.insert_value(p.IDENTIFIER, 0)  # Null type
                except:
                    self.semantic_error("Mismatch of type between identifier type and constant value assigned")
        else:
            if tab.get_type(p.IDENTIFIER) == 0:
                self.semantic_error(p.IDENTIFIER + " not defined")
            return p

        
        if tab.get_type(p.IDENTIFIER) == 'double' and tab.get_type(p[2][1]) == 'int':
            return p
        else:
            type_expr, val = self.eval_Expr(p[2])
            # Evaluating expression with no value setting, type checking only
            if tab.get_type(p.IDENTIFIER) == 'double' and type_expr == 'int' or tab.get_type(p.IDENTIFIER) == type_expr:
                if val != "NoVAL--":
                    tab.insert_value(p.IDENTIFIER, val)
            else:
                self.semantic_error("Error : Type mismatch " + str(tab.get_type(p.IDENTIFIER)) + " can not store a " +
                                    str(type_expr) + " Value")
        return p

    @_('IDENTIFIER "(" Actuals ")" ')
    def Call(self, p):
        # ToDo: here check all things related to mismatches in number and types of parameters 

        formals = tab.get_formals(p.IDENTIFIER)
        actuals_types = []

        # load actual variables types list
        def iterate_actuals(actuals, actuals_types):
            for item in actuals:
                if isinstance(item, tuple):
                    iterate_actuals(item, actuals_types)
                else:
                    if item == 'Variable':
                        actuals_types.add(actuals[1][1])
                    if item == 'Constant':
                        actuals_types.append(self.Eval_const(actuals[1]))

        iterate_actuals(p.Actuals, actuals_types)

        # Compare lists
        if len(formals) > len(actuals_types):
            self.semantic_error('Insufficient parameters for function ' + p.IDENTIFIER)
            return p

        if len(formals) < len(actuals_types):
            self.semantic_error('Too many parameters for function given ' + p.IDENTIFIER)
            return p

        for i in range(0, len(formals)):
            if formals[i] != actuals_types[i]:
                self.semantic_error('Type mismatch in parameter number ' + str(i + 1) + ' of function ' +
                                    str(p.IDENTIFIER) + ' type ' + str(formals[i]) + ' expected but ' +
                                    actuals_types[i] + ' was given')
                return p

        return p

    # Expr+, |ε
    @_('Expr ExprRest1','Epsilon')
    def Actuals(self, p):
        return p

    @_(' "," Expr ExprRest1', 'Epsilon')
    def ExprRest1(self, p):
        return p

    @_('INT','DOUBLE','BOOL','STRING','NULL')
    def Constant(self, p):
        return p

    # Empty production
    @_('')
    def Epsilon(self,p):
        pass

    # identifier
    @_('IDENTIFIER')
    def Decl(self, p):
        try:
            return self.IDENTIFIERs[p.IDENTIFIER]
        except LookupError:
            print("Undefined IDENT '%s'" % p.IDENTIFIER)
            return 0

    def error(self,p):
        print ("Syntax error near '%s'" % p.value[0],traceback.print_exc())
        

if __name__ == '__main__':

    # Read DLang source from file
    if len(sys.argv) == 2:
        lexer = DLangLexer()
        parser = DLangParser()
        with open(sys.argv[1]) as source:
            dlang_code = source.read()
            try:
                tokens = lexer.tokenize(dlang_code)
                for tok in tokens:
                    # Add identifier tokens to the symbol table
                    if tok.type == 'IDENTIFIER':
                        if tab.lookup_name(tok.value) == 0:
                            tab.add_name(tok.value)
                parser.parse(lexer.tokenize(dlang_code))
                print('Symbol Table Content')
                print(tab.table)
            except EOFError: exit(1)
    else:
        print("[DLang]: Source file missing")
