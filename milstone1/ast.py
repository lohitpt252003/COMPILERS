
class ASTNode:
    def __init__(self, line=None, column=None):
        self.line = line        # Source line number
        self.column = column    # Source column number

    def __repr__(self):
        return f"{self.__class__.__name__}(line={self.line}, col={self.column})"

class Program(ASTNode):
    def __init__(self, statements, line=None, column=None):
        super().__init__(line, column)
        self.statements = statements

    def __repr__(self):
        return f"Program(statements={self.statements}, line={self.line}, col={self.column})"

class Assignment(ASTNode):
    def __init__(self, var, expr, line=None, column=None):
        super().__init__(line, column)
        self.var = var    # e.g., ":x"
        self.expr = expr

    def __repr__(self):
        return f"Assignment({self.var} = {self.expr}, line={self.line}, col={self.column})"

class IfStatement(ASTNode):
    def __init__(self, condition, then_statements, else_statements=None, line=None, column=None):
        super().__init__(line, column)
        self.condition = condition
        self.then_statements = then_statements  # List of statements in the then-block.
        self.else_statements = else_statements  # Optional list for the else-block.

    def __repr__(self):
        return (f"IfStatement(cond={self.condition}, then={self.then_statements}, "
                f"else={self.else_statements}, line={self.line}, col={self.column})")

class RepeatStatement(ASTNode):
    def __init__(self, expr, statements, line=None, column=None):
        super().__init__(line, column)
        self.expr = expr              # Expression for the number of iterations.
        self.statements = statements  # List of statements inside the loop.

    def __repr__(self):
        return f"RepeatStatement({self.expr}, {self.statements}, line={self.line}, col={self.column})"

class PenStatement(ASTNode):
    def __init__(self, pen_type, line=None, column=None):
        super().__init__(line, column)
        self.pen_type = pen_type  # "penup" or "pendown"

    def __repr__(self):
        return f"PenStatement({self.pen_type}, line={self.line}, col={self.column})"

class MoveStatement(ASTNode):
    def __init__(self, move_type, exprs, line=None, column=None):
        super().__init__(line, column)
        self.move_type = move_type  # "forward", "backward", "left", "right", or "go"
        self.exprs = exprs          # List of one expression (or two for "go")

    def __repr__(self):
        return f"MoveStatement({self.move_type}, {self.exprs}, line={self.line}, col={self.column})"

class BinaryOp(ASTNode):
    def __init__(self, left, op, right, line=None, column=None):
        super().__init__(line, column)
        self.left = left
        self.op = op      # e.g., "+", "-", "==", etc.
        self.right = right

    def __repr__(self):
        return f"BinaryOp({self.left} {self.op} {self.right}, line={self.line}, col={self.column})"

class UnaryOp(ASTNode):
    def __init__(self, op, operand, line=None, column=None):
        super().__init__(line, column)
        self.op = op      # e.g., "-", "!".
        self.operand = operand

    def __repr__(self):
        return f"UnaryOp({self.op}{self.operand}, line={self.line}, col={self.column})"

class Number(ASTNode):
    def __init__(self, value, line=None, column=None):
        super().__init__(line, column)
        self.value = value  # Numeric value

    def __repr__(self):
        return f"Number({self.value}, line={self.line}, col={self.column})"

class Var(ASTNode):
    def __init__(self, name, line=None, column=None):
        super().__init__(line, column)
        self.name = name  # Variable name (including the colon, e.g. ":x")

    def __repr__(self):
        return f"Var({self.name}, line={self.line}, col={self.column})"

# For simple testing of the AST classes.
if __name__ == "__main__":
    
    prog = Program([
        Assignment(":x", Number(10, line=2, column=5), line=2, column=1),
        MoveStatement("forward", [Var(":x", line=3, column=9)], line=3, column=1)
    ], line=2, column=1)
    print(prog)
