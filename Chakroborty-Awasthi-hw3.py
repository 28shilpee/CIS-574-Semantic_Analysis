# -------------------------------------------------------------------------
# hw3-starter.py: Starter code for DLang Semantic Analyzer
# Run with source file 
# -------------------------------------------------------------------------
import sys
from sly import Lexer, Parser
import traceback

class SymbolTable:
    
    def __init__(self):
        self.table = []
        self.current_function = None  # Track the current function for return type checking
    
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
        
    def set_current_function(self, name):
        '''Set the current function being processed for return type checking'''
        self.current_function = name
        
    def get_current_function_type(self):
        '''Get the return type of the current function'''
        if self.current_function:
            return self.get_type(self.current_function)
        return None

# global object that instantiates symbol table: use this to insert, get, loookup ...
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

    # Set operator preceedence
    precedence = (
        ('nonassoc', EQ, NE, LE, GE, AND, OR, '<', '>'),
        ('left', '+', '-'),
        ('left', '*', '/', '%'),
        ('nonassoc', '=')
        )   

    def __init__(self):
        self.IDENTIFIERs = { }
        self.semantic_errors = 0
    
    def semantic_error(self,msg):
        print('\n Semantic Error:', msg)
        self.semantic_errors += 1
    
        
    # Program ->Decl+
    @_('Decl DeclRest', 'Epsilon')
    def Program(self, p):
        if self.semantic_errors == 0:
            print('\n No Semantic Error!')
        else:
            print(f'\n {self.semantic_errors} semantic errors found!')
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
        # Add the type of each identifier to the symbol table
        tab.add_type(p.IDENTIFIER, p[0])
        return {'name': p.IDENTIFIER, 'type': p[0]}

    @_('INTK', 'DOUBLEK', 'BOOLK','STRINGK')
    def Type(self, p):
        return p[0]

    # FunctionDecl -> Type ident ( Formals ) StmtBlock 
    @_('Variable "(" Formals ")" StmtBlock') 
    def FunctionDecl(self, p):
        # Set the current function for return type checking
        tab.set_current_function(p.Variable['name'])
        
        # Store function parameters
        if isinstance(p.Formals, list):
            for formal in p.Formals:
                if formal:
                    tab.add_formals(p.Variable['name'], formal)
        elif p.Formals:
            tab.add_formals(p.Variable['name'], p.Formals)
            
        # Reset current function after processing the function block
        tab.set_current_function(None)
        return p

    # FunctionDecl -> nothing ident ( Formals ) StmtBlock
    @_('NOTHING IDENTIFIER "(" Formals ")" StmtBlock')
    def FunctionDecl(self, p):
        # Add the function to symbol table with "nothing" type
        tab.add_type(p.IDENTIFIER, 'nothing')
        tab.set_current_function(p.IDENTIFIER)
        
        # Store function parameters
        if isinstance(p.Formals, list):
            for formal in p.Formals:
                if formal:
                    tab.add_formals(p.IDENTIFIER, formal)
        elif p.Formals:
            tab.add_formals(p.IDENTIFIER, p.Formals)
            
        # Reset current function after processing the function block
        tab.set_current_function(None)
        return p

    # Formals -> Variable+,|ε
    @_('Variable VariableRest')
    def Formals(self, p):
        if p.VariableRest:
            if isinstance(p.VariableRest, list):
                return [p.Variable] + p.VariableRest
            else:
                return [p.Variable, p.VariableRest]
        return p.Variable

    @_('Epsilon')
    def Formals(self, p):
        return []

    @_('"," Variable VariableRest')
    def VariableRest(self, p):
        if p.VariableRest:
            if isinstance(p.VariableRest, list):
                return [p.Variable] + p.VariableRest
            else:
                return [p.Variable, p.VariableRest]
        return p.Variable

    @_('Epsilon')
    def VariableRest(self, p):
        return None
   

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
    @_('RETURN Expr ";" ')
    def ReturnStmt(self, p):
        # Check if return type matches function return type
        function_type = tab.get_current_function_type()
        if function_type and hasattr(p.Expr, 'type'):
            if not self.type_compatible(function_type, p.Expr.type):
                self.semantic_error(f"mismatch between return type ({function_type}) and return value of function ({p.Expr.type})")
        return p

    @_('RETURN ";"')
    def ReturnStmt(self, p):
        # Check if void function is trying to return a value
        function_type = tab.get_current_function_type()
        if function_type != 'nothing':
            self.semantic_error(f"function with return type {function_type} must return a value")
        return p

    # break ;
    @_('BREAK ";" ')
    def BreakStmt(self, p):
        return p

   # Output ( Expr+, ) ;     
    @_('OUTPUT "(" Expr ExprRest ")" ";" ')
    def OutputStmt(self, p):
        return p

    @_(' "," Expr ExprRest', 'Epsilon')
    def ExprRest(self, p):
        return p

    @_('"!" Expr')
    def Expr(self, p):
        if hasattr(p.Expr, 'type'):
            # Logical not should be applied to boolean expressions
            if p.Expr.type != 'bool':
                self.semantic_error(f"operand to '!' must be boolean, found {p.Expr.type}")
            result = SimpleObject()
            result.type = 'bool'
            return result
        return p.Expr

    @_('IDENTIFIER')
    def Expr(self, p):
        # Check if identifier is declared
        if tab.lookup_name(p.IDENTIFIER) == 0:
            self.semantic_error(f"identifier '{p.IDENTIFIER}' is used before it is declared")
            result = SimpleObject()
            result.type = 'unknown'
            return result
        
        # Get the type of the identifier
        id_type = tab.get_type(p.IDENTIFIER)
        if id_type == 0:
            self.semantic_error(f"identifier '{p.IDENTIFIER}' has no type")
            result = SimpleObject()
            result.type = 'unknown'
            return result
        
        result = SimpleObject()
        result.type = id_type
        result.name = p.IDENTIFIER
        return result

    @_('Constant')
    def Expr(self, p):
        return p.Constant

    @_('Call')
    def Expr(self, p):
        return p.Call

    @_('"(" Expr ")"')
    def Expr(self, p):
        return p.Expr

    @_('"-" Expr')
    def Expr(self, p):
        if hasattr(p.Expr, 'type'):
            # Negation should be applied to numeric expressions
            if p.Expr.type not in ['int', 'double']:
                self.semantic_error(f"operand to '-' must be numeric, found {p.Expr.type}")
            
            result = SimpleObject()
            result.type = p.Expr.type
            return result
        return p.Expr

    @_('INPUTINT "(" ")"')
    def Expr(self, p):
        result = SimpleObject()
        result.type = 'int'
        return result

    @_('INPUTLINE "(" ")"')
    def Expr(self, p):
        result = SimpleObject()
        result.type = 'string'
        return result

    @_('Expr "+" Expr', 'Expr "-" Expr', 'Expr "*" Expr', 'Expr "/" Expr', 'Expr "%" Expr')
    def Expr(self, p):
        # Check if types of operands are compatible
        if hasattr(p[0], 'type') and hasattr(p[2], 'type'):
            left_type = p[0].type
            right_type = p[2].type
            
            # Special case for string concatenation with + operator
            if p[1] == '+' and (left_type == 'string' or right_type == 'string'):
                if left_type != right_type:
                    self.semantic_error(f"cannot concatenate '{left_type}' and '{right_type}'")
                result = SimpleObject()
                result.type = 'string'
                return result
            
            # Arithmetic operations should be performed on numeric types
            if left_type not in ['int', 'double'] or right_type not in ['int', 'double']:
                self.semantic_error(f"operand type mismatch: '{left_type}' {p[1]} '{right_type}'")
                result = SimpleObject()
                result.type = 'int'  # Default to int for error recovery
                return result
            
            # Result type is the "wider" of the two types
            result = SimpleObject()
            if left_type == 'double' or right_type == 'double':
                result.type = 'double'
            else:
                result.type = 'int'
            return result
        
        result = SimpleObject()
        result.type = 'unknown'
        return result

    @_('Expr "<" Expr', 'Expr LE Expr', 'Expr ">" Expr', 'Expr GE Expr', 'Expr EQ Expr', 'Expr NE Expr')
    def Expr(self, p):
        # Check if types of operands are compatible for comparison
        if hasattr(p[0], 'type') and hasattr(p[2], 'type'):
            left_type = p[0].type
            right_type = p[2].type
            
            # Comparison operators can be applied to numeric types
            if left_type not in ['int', 'double'] or right_type not in ['int', 'double']:
                self.semantic_error(f"operand type mismatch for comparison: '{left_type}' {p[1]} '{right_type}'")
        
        result = SimpleObject()
        result.type = 'bool'
        return result

    @_('Expr AND Expr', 'Expr OR Expr')
    def Expr(self, p):
        # Check if types of operands are compatible for logical operations
        if hasattr(p[0], 'type') and hasattr(p[2], 'type'):
            left_type = p[0].type
            right_type = p[2].type
            
            # Logical operators should be applied to boolean expressions
            if left_type != 'bool' or right_type != 'bool':
                self.semantic_error(f"operand type mismatch for logical operation: '{left_type}' {p[1]} '{right_type}'")
        
        result = SimpleObject()
        result.type = 'bool'
        return result

    @_('IDENTIFIER "=" Expr')
    def Expr(self, p):
        # Check if the identifier has been declared before
        if tab.lookup_name(p.IDENTIFIER) == 0:
            self.semantic_error(f"identifier '{p.IDENTIFIER}' is used before it is declared")
            result = SimpleObject()
            result.type = 'unknown'
            return result
        
        id_type = tab.get_type(p.IDENTIFIER)
        
        # Check type compatibility for assignment
        if hasattr(p.Expr, 'type'):
            expr_type = p.Expr.type
            
            if not self.type_compatible(id_type, expr_type):
                self.semantic_error(f"operand type mismatch and unsafe type casting: cannot assign '{expr_type}' to '{id_type}'")
        
        result = SimpleObject()
        result.type = id_type
        return result
            

    @_('IDENTIFIER "(" Actuals ")" ')
    def Call(self, p):
        # Check if function exists
        if tab.lookup_name(p.IDENTIFIER) == 0:
            self.semantic_error(f"call to undeclared function '{p.IDENTIFIER}'")
            result = SimpleObject()
            result.type = 'unknown'
            return result
        
        # Get function type and formals
        func_type = tab.get_type(p.IDENTIFIER)
        formals = tab.get_formals(p.IDENTIFIER)
        
        # Check number of parameters
        actuals = p.Actuals if p.Actuals else []
        if not isinstance(actuals, list):
            actuals = [actuals]
        
        # Filter out None values from actuals
        actuals = [a for a in actuals if a is not None]
        
        if len(formals) != len(actuals):
            if len(formals) > len(actuals):
                self.semantic_error(f"too few parameters to function '{p.IDENTIFIER}'")
            else:
                self.semantic_error(f"too many parameters to function '{p.IDENTIFIER}'")
        
        # Check parameter types
        for i in range(min(len(formals), len(actuals))):
            if hasattr(actuals[i], 'type') and isinstance(formals[i], dict) and 'type' in formals[i]:
                formal_type = formals[i]['type']
                actual_type = actuals[i].type
                
                if not self.type_compatible(formal_type, actual_type):
                    self.semantic_error(f"type mismatch between actual and formal parameters: expected '{formal_type}', got '{actual_type}'")
        
        # Return function type
        result = SimpleObject()
        result.type = func_type
        return result

    # Expr+, |ε
    @_('Expr ExprRest1')
    def Actuals(self, p):
        if p.ExprRest1:
            if isinstance(p.ExprRest1, list):
                return [p.Expr] + p.ExprRest1
            else:
                return [p.Expr, p.ExprRest1]
        return [p.Expr]

    @_('Epsilon')
    def Actuals(self, p):
        return []

    @_('"," Expr ExprRest1')
    def ExprRest1(self, p):
        if p.ExprRest1:
            if isinstance(p.ExprRest1, list):
                return [p.Expr] + p.ExprRest1
            else:
                return [p.Expr, p.ExprRest1]
        return p.Expr

    @_('Epsilon')
    def ExprRest1(self, p):
        return None

    @_('INT')
    def Constant(self, p):
        result = SimpleObject()
        result.type = 'int'
        result.value = int(p.INT)
        return result

    @_('DOUBLE')
    def Constant(self, p):
        result = SimpleObject()
        result.type = 'double'
        result.value = float(p.DOUBLE)
        return result

    @_('BOOL')
    def Constant(self, p):
        result = SimpleObject()
        result.type = 'bool'
        result.value = p.BOOL == 'True'
        return result

    @_('STRING')
    def Constant(self, p):
        result = SimpleObject()
        result.type = 'string'
        result.value = p.STRING
        return result

    @_('NULL')
    def Constant(self, p):
        result = SimpleObject()
        result.type = 'null'
        return result

    # Helper method to check type compatibility
    def type_compatible(self, target_type, source_type):
        # Same types are always compatible
        if target_type == source_type:
            return True
        
        # int can be assigned to double (safe conversion)
        if target_type == 'double' and source_type == 'int':
            return True
        
        # double to int is unsafe and not allowed
        if target_type == 'int' and source_type == 'double':
            return False
        
        # All other type conversions are not allowed
        return False

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

# Simple class to attach attributes (type, name, value) to objects
class SimpleObject:
    pass

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