## Venkataraman 18 5001 192

import time
from copy import deepcopy 

class SATProblem:
    
    def __init__(self, formula):
        '''
        Initialize the class with neccessary literals and 
        Clausal form of the string formula.
        '''
        
        self.formula = formula
        while(len(formula) and self.formula[0] == ' '):
            self.formula = self.formula[1:]
        self.clauses = [[literal for literal in clause.split()] for clause in self.formula.split(", ")]
        self.literals = self.getLiterals()
        self.true_literals = set()
        self.false_literals = set()
        
        self.no_of_branches = 0
        self.unit_depth = 0
        self.pure_literal_depth = 0
        self.result = None
        
    def __str__(self):
        '''
        To convert the object into human readable form 
        using pretty printer.
        '''
        
        string = self.prettyPrint(self.clauses); 
        return string
    
    def prettyPrint(self,clauses):
        '''
        To convert the 2D- list into human readable form using 
        brackets union and intersection unicode symbols
        '''
        
        string = ""
        
        if clauses == []:
            string = '(True)'
        
        for i,clause in enumerate(clauses):
            string += '('
            
            if clause == []:
                string += 'False'
            
            for j,literal in enumerate(clause):
                string += literal
                string += ' '
                if j != len(clause)-1:
                    string += '∨ '
            if '∨' in string:
                string += '\b'
            string += ')'
            
            if i != len(clauses)-1:
                string += ' ∧ '    
        
        return string
    
    def getLiterals(self):
        '''
        Returns the set of literals involved in the CNF form
        of the formula
        '''
        
        literals = set()
        
        for clause in self.clauses:
            for literal in clause:
                if '¬' in literal:
                    literals.add(literal[1:])
                else:
                    literals.add(literal)
        
        return sorted(literals)

    def printSolution(self):
        '''
        Printing the solution in proper format
        '''
        
        print('The formula is ', self)
        print('The given formula is ', self.result, '\n')
        
        if self.result == 'SATISFIABLE':
            for literal in self.literals:
                if literal in self.false_literals:
                    print('\t',literal,' : False')
                elif literal in self.true_literals:
                    print('\t',literal,' : True')
                else:
                    print('\t',literal,' : Don\'t Care')
            print()
        
        print('No. of Pure literal(s) elimination tried : ',self.pure_literal_depth, '\n')
        print('No. of Unit propogations                 : ',self.unit_depth, '\n')
        print('No. of Branching by Substituition        : ',self.no_of_branches, '\n')
    
    def allTrue(self, clauses, model):
        '''
        Checks for every clause being true
        with respect to the current model
        '''
        
        if len(clauses) == 0 or clauses == []:
            return True
        for clause in clauses:
            someTrue = False
            for literal in clause:
                if '¬' in literal and literal[1:] in model and model[literal[1:]] == False:
                    someTrue = True
                    break
                elif '¬' not in literal and literal in model and model[literal] == True:
                    someTrue = True
                    break
            if not someTrue:
                 return False
        return True
    
    def someFalse(self, clauses, model):
        '''
        Checks for some clause being false
        with respect to the current model
        '''
        
        if [] in clauses:
            return True
        for clause in clauses:
            clauseFalse = True
            for literal in clause:
                if '¬' in literal and literal[1:] in model and model[literal[1:]] == False:
                    clauseFalse = False
                    break
                elif '¬' not in literal and literal in model and model[literal] == True:
                    clauseFalse = False
                    break
                elif '¬' in literal and literal[1:] not in model:
                    clauseFalse = False
                    break
                elif '¬' not in literal and literal not in model:
                    clauseFalse = False
                    break
            if clauseFalse:
                 return True
        return False
    
    def compliment(self, Clauses):
        '''
        Finds the compliment of literals on the given CNF
        '''
        
        clauses = deepcopy(Clauses)
        for i,clause in enumerate(clauses):
            for j,literal in enumerate(clause):
                if '¬' not in literal:
                    clauses[i][j] = '¬' + literal
                else:
                    clauses[i][j] = literal[1:]
        return clauses
    
    def findPure(self, clauses, neg=False):
        '''
        the function traverses and finds a pure literal if any present
        else returns 'None' saying no pure literal is been found
        '''
        
        pure_symbols = set()
        for clause in clauses:
            for literal in clause:
                if '¬' not in literal:
                    pure_symbols.add(literal)

        for clause in clauses:
            for literal in clause:
                if '¬' in literal and literal[1:] in pure_symbols:
                    pure_symbols.remove(literal[1:])
        
        pure_symbols = sorted(pure_symbols)
        
        if neg:
            for i,lit in enumerate(pure_symbols):
                pure_symbols[i] = '¬' + pure_symbols[i]
        
        if len(pure_symbols) == 0:
            return None
        
        return pure_symbols[0]
        
    
    def findPureSymbol(self, clauses):
        '''
        the function finds all positive pure literals first , if no postive literals 
        are present , it tries to find a negetive literal and return them.
        if 'None' present it returns 'None'
        '''
        
        positive_pure_symbol = self.findPure(clauses)
        
        if positive_pure_symbol:
            return positive_pure_symbol
        
        clauses = self.compliment(clauses)
        
        negetive_pure_symbol = self.findPure(clauses,True)
        
        if negetive_pure_symbol:
            return negetive_pure_symbol
        
        return None
        
    def findUnitClause(self, clauses, model):
        '''
        The function finds a unit clause from the set of clauses present
        '''
        
        for indx,clause in enumerate(clauses):
            isUnit = True
            undefined = None
            
            if len(clause) == 1:
                return indx, clause[0]
            
            
        for indx,clause in enumerate(clauses):
            isUnit = True
            undefined = []
            
            for literal in clause:
                if '¬' in literal and literal[1:] in model and model[literal[1:]] == False:
                    isUnit = False
                elif '¬' not in literal and literal in model and model[literal] == True:
                    isUnit = False
                elif '¬' in literal and literal[1:] not in model:
                    undefined.append(literal)
                elif '¬' not in literal and literal not in model:
                    undefined.append(literal)
            
            if isUnit and len(undefined)==1:
                return indx, undefined[0]
                
        return None, None
    
    def applyValue(self,clauses, symbol):
        '''
        Reduces the clausal form by substituting the symbol with 
        corressponding value
        '''
        
        remove_clause = set()
        
        for i,clause in enumerate(clauses):
            remove_literal = set()
                
            for j,literal in enumerate(clause):
                if literal == symbol:
                    remove_clause.add(i)
                    break
                
                elif '¬' + literal == symbol or '¬' + symbol == literal:
                    remove_literal.add(j)
            
            if i not in remove_clause:
                remove_literal = sorted(remove_literal)
                
                for indx in remove_literal[::-1]:
                    clauses[i].pop(indx)

        remove_clause = sorted(remove_clause)
        
        for indx in remove_clause[::-1]:
            clauses.pop(indx)
        
        return clauses
        
    def DPLLSatisfiable(self):
        '''
        Runs DPLL function and finds satisfiability of the Algorithm
        '''
        
        print('Query:-\n\tTo find satisfiability for : ',self, '\n');
        ret =  self.DPLL(deepcopy(self.clauses),model=dict())

        if ret:
            self.result = 'SATISFIABLE'
        else:
            self.result = 'UNSATISFIABLE'
            
        self.printSolution()
        
    def DPLL(self, clauses, model):
        '''
        DPLL Algo.
        
        # Find whether all the clauses are true - allTrue()
        # Find whether some clause is false - someFalse()
        # Do unit propogation.
        # Find pure symbol(s) and eliminate them
        # Find the firstLiteral in the clause and replace it with 
          True and check for satisfiability, if Unsatisfied check 
          for substitution for False, and return Satisfiabiltity
        
        '''
        print('Clauses : ', self.prettyPrint(clauses))
        
        if self.allTrue(clauses, model):
            for lit, value in model.items():
                if value == True:
                    self.true_literals.add(lit)
                else:
                    self.false_literals.add(lit)
            
            print('Resultant Clause   : 🟩')
            print('Model obtained ...\n')
            return True

        if self.someFalse(clauses, model):
            print('Resultant Clause(s)  : (🟥) ')
            print("Unsatisfiable Clause Obtained .... \nBacktracking to immediate Higher Layer....\n")

            return False
        
        unit_clause_indx, unit_symbol = self.findUnitClause(clauses, model)
        
        if unit_clause_indx != None:
            
            self.unit_depth += 1
            
            clauses.pop(unit_clause_indx)
            
            if '¬' in unit_symbol:
                model[unit_symbol[1:]] = False
            else:
                model[unit_symbol] = True
            
            clauses = self.applyValue(clauses, unit_symbol)

            print('Unit Symbol Found : ', unit_symbol)
            print('Reduced Clasue(s)   : ',self.prettyPrint(clauses))
            print()
            return self.DPLL(deepcopy(clauses), deepcopy(model))
        
        pure_symbol = self.findPureSymbol(clauses)
        
        if pure_symbol:
            
            self.pure_literal_depth += 1
            
            remove_clause = set()
            
            for i,clause in enumerate(clauses):
                for literal in clause:
                    if literal == pure_symbol:
                        remove_clause.add(i)
                        break
            
            remove_clause = sorted(remove_clause)
            
            for indx in remove_clause[::-1]:
                clauses.pop(indx)
        
            if '¬' in pure_symbol:
                model[pure_symbol[1:]] = False
            else:
                model[pure_symbol] = True
            
            print('Pure Symbol Found : ',pure_symbol)
            print('Reduced Clause(s)   : ',self.prettyPrint(clauses))
            print()
            return self.DPLL(deepcopy(clauses), deepcopy(model))
        
        

        #naive checker 
        
        firstLiteral = None
        
        for clause in clauses:
            for literal in clause:
                firstLiteral = literal
                if '¬' in firstLiteral:
                    firstLiteral = firstLiteral[1:]
                break
            break
        
        newClauses = deepcopy(clauses)
        newClauses = self.applyValue(newClauses, firstLiteral)
        newModel = deepcopy(model)
        newModel[firstLiteral] = True
        
        print('Substituting ', firstLiteral, ' : True')
        print('Reduced Clause(s) : ', self.prettyPrint(newClauses))
        print()
        
        retVal = self.DPLL(newClauses, newModel)
        
        self.no_of_branches += 1
        
        if retVal == True:
            return True
        
        newClauses = deepcopy(clauses)
        newClauses = self.applyValue(newClauses, '¬'+firstLiteral)
        newModel = deepcopy(model)
        newModel[firstLiteral] = False
        
        print('BackTracked to Current level ....\n')
        print('Clauses : ', self.prettyPrint(clauses))
        print('Substituting ', firstLiteral, ' : False')
        print('Reduced Clause(s) : ', self.prettyPrint(newClauses))
        print()
        
        retVal = self.DPLL(newClauses, newModel)
        
        self.no_of_branches += 1
        
        if retVal == True:
            return True
        
        return False
    
if __name__ == "__main__":
    print('\t\t DPLL Algorithm\n\n')
    
    print("---------------------------------------------------\n")  
    solver = SATProblem('A B ¬C, A ¬B D');
    solver.DPLLSatisfiable()
    
    print("---------------------------------------------------\n")
    solver = SATProblem('P, ¬P')
    solver.DPLLSatisfiable()
    
    print("---------------------------------------------------\n")
    solver = SATProblem('¬P Q, ¬Q ¬R, R ¬S, ¬S P, P Q ¬R')
    solver.DPLLSatisfiable()
    
    print("---------------------------------------------------\n")
    solver = SATProblem("X Y Z, X ¬Y Z, ¬X Y ¬Z, ¬Z")
    solver.DPLLSatisfiable()
    
    print("---------------------------------------------------\n")

'''
OUTPUT:
                DPLL Algorithm


---------------------------------------------------

Query:-
        To find satisfiability for :  (A ∨ B ∨ ¬C) ∧ (A ∨ ¬B ∨ D) 

Clauses :  (A ∨ B ∨ ¬C) ∧ (A ∨ ¬B ∨ D)
Pure Symbol Found :  A
Reduced Clause(s)   :  (True)

Clauses :  (True)
Resultant Clause   : 🟩
Model obtained ...

The formula is  (A ∨ B ∨ ¬C) ∧ (A ∨ ¬B ∨ D)
The given formula is  SATISFIABLE 

         A  : True
         B  : Don't Care
         C  : Don't Care
         D  : Don't Care

No. of Pure literal(s) elimination tried :  1 

No. of Unit propogations                 :  0 

No. of Branching by Substituition        :  0 

---------------------------------------------------

Query:-
        To find satisfiability for :  (P ) ∧ (¬P ) 

Clauses :  (P ) ∧ (¬P )
Unit Symbol Found :  P
Reduced Clasue(s)   :  (False)

Clauses :  (False)
Resultant Clause(s)  : (🟥) 
Unsatisfiable Clause Obtained .... 
Backtracking to immediate Higher Layer....

The formula is  (P ) ∧ (¬P )
The given formula is  UNSATISFIABLE 

No. of Pure literal(s) elimination tried :  0 

No. of Unit propogations                 :  1 

No. of Branching by Substituition        :  0 

---------------------------------------------------

Query:-
        To find satisfiability for :  (¬P ∨ Q) ∧ (¬Q ∨ ¬R) ∧ (R ∨ ¬S) ∧ (¬S ∨ P) ∧ (P ∨ Q ∨ ¬R) 

Clauses :  (¬P ∨ Q) ∧ (¬Q ∨ ¬R) ∧ (R ∨ ¬S) ∧ (¬S ∨ P) ∧ (P ∨ Q ∨ ¬R)
Pure Symbol Found :  ¬S
Reduced Clause(s)   :  (¬P ∨ Q) ∧ (¬Q ∨ ¬R) ∧ (P ∨ Q ∨ ¬R)

Clauses :  (¬P ∨ Q) ∧ (¬Q ∨ ¬R) ∧ (P ∨ Q ∨ ¬R)
Pure Symbol Found :  ¬R
Reduced Clause(s)   :  (¬P ∨ Q)

Clauses :  (¬P ∨ Q)
Pure Symbol Found :  Q
Reduced Clause(s)   :  (True)

Clauses :  (True)
Resultant Clause   : 🟩
Model obtained ...

The formula is  (¬P ∨ Q) ∧ (¬Q ∨ ¬R) ∧ (R ∨ ¬S) ∧ (¬S ∨ P) ∧ (P ∨ Q ∨ ¬R)
The given formula is  SATISFIABLE 

         P  : Don't Care
         Q  : True
         R  : False
         S  : False

No. of Pure literal(s) elimination tried :  3 

No. of Unit propogations                 :  0 

No. of Branching by Substituition        :  0 

---------------------------------------------------

Query:-
        To find satisfiability for :  (X ∨ Y ∨ Z) ∧ (X ∨ ¬Y ∨ Z) ∧ (¬X ∨ Y ∨ ¬Z) ∧ (¬Z) 

Clauses :  (X ∨ Y ∨ Z) ∧ (X ∨ ¬Y ∨ Z) ∧ (¬X ∨ Y ∨ ¬Z) ∧ (¬Z)
Unit Symbol Found :  ¬Z
Reduced Clasue(s)   :  (X ∨ Y) ∧ (X ∨ ¬Y)

Clauses :  (X ∨ Y) ∧ (X ∨ ¬Y)
Pure Symbol Found :  X
Reduced Clause(s)   :  (True)

Clauses :  (True)
Resultant Clause   : 🟩
Model obtained ...

The formula is  (X ∨ Y ∨ Z) ∧ (X ∨ ¬Y ∨ Z) ∧ (¬X ∨ Y ∨ ¬Z) ∧ (¬Z)
The given formula is  SATISFIABLE 

         X  : True
         Y  : Don't Care
         Z  : False

No. of Pure literal(s) elimination tried :  1 

No. of Unit propogations                 :  1 

No. of Branching by Substituition        :  0 

---------------------------------------------------
'''