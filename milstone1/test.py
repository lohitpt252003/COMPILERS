

import glob

# Import our local modules.
import token as chiron_token   # our token.py module
import ast as chiron_ast       # our ast.py module

# AST node for the input statement.
class InputStatement(chiron_ast.ASTNode):
    def __init__(self, variables, line=None, column=None):
        super().__init__(line, column)
        self.variables = variables

    def __repr__(self):
        return f"InputStatement(variables={self.variables}, line={self.line}, col={self.column})"

# Minimal recursive‐descent parser for CHIRONLANG.
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens  # list of chiron_token.Token objects
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def advance(self):
        self.pos += 1

    def consume(self, expected_type, expected_value=None):
        token = self.peek()
        if token is None:
            raise Exception("Unexpected end of input; expected " + expected_type)
        if token.type != expected_type:
            raise Exception(f"Expected token type {expected_type} but got {token.type} at line {token.line}, col {token.column}")
        if expected_value is not None and token.value != expected_value:
            raise Exception(f"Expected token value '{expected_value}' but got '{token.value}' at line {token.line}, col {token.column}")
        self.advance()
        return token

    # Program → StatementList
    def parse_program(self):
        statements = self.parse_statement_list()
        first_line = statements[0].line if statements else None
        first_col = statements[0].column if statements else None
        return chiron_ast.Program(statements, line=first_line, column=first_col)

    def parse_statement_list(self):
        statements = []
        while self.pos < len(self.tokens):
            token = self.peek()
            if token.type == "SYMBOL" and token.value == "]":
                break
            stmt = self.parse_statement()
            statements.append(stmt)
            token = self.peek()
            if token and token.type == "SYMBOL" and token.value == ";":
                self.consume("SYMBOL", ";")
            # Semicolons are optional.
        return statements

    def parse_statement(self):
        token = self.peek()
        if token is None:
            raise Exception("Unexpected end of input while parsing a statement")
        if token.type == "KEYWORD":
            if token.value == "if":
                return self.parse_if()
            elif token.value == "repeat":
                return self.parse_repeat()
            elif token.value in ("penup", "pendown"):
                return self.parse_pen()
            elif token.value in ("forward", "backward", "left", "right", "go"):
                return self.parse_move()
            elif token.value == "input":
                return self.parse_input()
        # Otherwise, if an IDENT followed by '=' is an assignment.
        if token.type == "IDENT":
            if (self.pos + 1 < len(self.tokens) and 
                self.tokens[self.pos + 1].type == "SYMBOL" and 
                self.tokens[self.pos + 1].value == "="):
                return self.parse_assignment()
        raise Exception("Unrecognized statement starting with token: " + repr(token))

    def parse_assignment(self):
        var_token = self.consume("IDENT")
        self.consume("SYMBOL", "=")
        expr = self.parse_expr()
        return chiron_ast.Assignment(var_token.value, expr, line=var_token.line, column=var_token.column)

    def parse_if(self):
        if_token = self.consume("KEYWORD", "if")
        condition = self.parse_expr()
        self.consume("SYMBOL", "[")
        then_statements = self.parse_statement_list()
        self.consume("SYMBOL", "]")
        else_statements = None
        token = self.peek()
        if token and token.type == "KEYWORD" and token.value == "else":
            self.consume("KEYWORD", "else")
            self.consume("SYMBOL", "[")
            else_statements = self.parse_statement_list()
            self.consume("SYMBOL", "]")
        return chiron_ast.IfStatement(condition, then_statements, else_statements, line=if_token.line, column=if_token.column)

    def parse_repeat(self):
        repeat_token = self.consume("KEYWORD", "repeat")
        expr = self.parse_expr()
        self.consume("SYMBOL", "[")
        statements = self.parse_statement_list()
        self.consume("SYMBOL", "]")
        return chiron_ast.RepeatStatement(expr, statements, line=repeat_token.line, column=repeat_token.column)

    def parse_pen(self):
        pen_token = self.consume("KEYWORD")
        if pen_token.value not in ("penup", "pendown"):
            raise Exception("Expected 'penup' or 'pendown' but got " + pen_token.value)
        return chiron_ast.PenStatement(pen_token.value, line=pen_token.line, column=pen_token.column)

    def parse_move(self):
        move_token = self.consume("KEYWORD")
        move_type = move_token.value
        if move_type in ("forward", "backward", "left", "right"):
            expr = self.parse_expr()
            return chiron_ast.MoveStatement(move_type, [expr], line=move_token.line, column=move_token.column)
        elif move_type == "go":
            self.consume("SYMBOL", "(")
            expr1 = self.parse_expr()
            self.consume("SYMBOL", ",")
            expr2 = self.parse_expr()
            self.consume("SYMBOL", ")")
            return chiron_ast.MoveStatement(move_type, [expr1, expr2], line=move_token.line, column=move_token.column)
        else:
            raise Exception("Unrecognized move command: " + move_type)

    def parse_input(self):
        input_token = self.consume("KEYWORD", "input")
        self.consume("SYMBOL", "(")
        variables = []
        while True:
            var_token = self.consume("IDENT")
            variables.append(var_token.value)
            token = self.peek()
            if token and token.type == "SYMBOL" and token.value == ",":
                self.consume("SYMBOL", ",")
            else:
                break
        self.consume("SYMBOL", ")")
        return InputStatement(variables, line=input_token.line, column=input_token.column)

    # Simple expression parser (supports numbers, identifiers, binary operations, and parentheses).
    def parse_expr(self):
        return self.parse_term()

    def parse_term(self):
        node = self.parse_factor()
        while True:
            token = self.peek()
            if token and token.type == "SYMBOL" and token.value in ("+", "-"):
                op = token.value
                self.advance()
                right = self.parse_factor()
                node = chiron_ast.BinaryOp(node, op, right, line=token.line, column=token.column)
            else:
                break
        return node

    def parse_factor(self):
        node = self.parse_primary()
        while True:
            token = self.peek()
            if token and token.type == "SYMBOL" and token.value in ("*", "/"):
                op = token.value
                self.advance()
                right = self.parse_primary()
                node = chiron_ast.BinaryOp(node, op, right, line=token.line, column=token.column)
            else:
                break
        return node

    def parse_primary(self):
        token = self.peek()
        if token is None:
            raise Exception("Unexpected end of input in expression")
        if token.type == "NUMBER":
            self.advance()
            return chiron_ast.Number(int(token.value), line=token.line, column=token.column)
        if token.type == "IDENT":
            self.advance()
            return chiron_ast.Var(token.value, line=token.line, column=token.column)
        if token.type == "SYMBOL" and token.value == "(":
            self.consume("SYMBOL", "(")
            node = self.parse_expr()
            self.consume("SYMBOL", ")")
            return node
        if token.type == "SYMBOL" and token.value in ("-", "!"):
            op = token.value
            self.advance()
            operand = self.parse_primary()
            return chiron_ast.UnaryOp(op, operand, line=token.line, column=token.column)
        raise Exception("Unexpected token in expression: " + repr(token))

# Function to run one test file.
def run_test_file(filename):
    try:
        with open(filename, 'r') as f:
            source = f.read()
    except Exception as e:
        print(f"Error reading file {filename}: {e}")
        return False

    print(f"\n=== Running test: {filename} ===")
    try:
        # Tokenize the source.
        tokens = chiron_token.tokenize(source)
        print("Tokens:")
        for t in tokens:
            print("  ", t)
        # Parse tokens into an AST.
        parser = Parser(tokens)
        ast_tree = parser.parse_program()
        print("\nAST:")
        print(ast_tree)
        print("Test PASSED.\n")
        return True
    except Exception as e:
        print(f"Test FAILED with error: {e}\n")
        return False

def main():
    test_files = glob.glob("./tests/*.t1")
    if not test_files:
        print("No .t1 test files found in the current directory.")
        return

    total_tests = len(test_files)
    passed_tests = 0

    # Process each test file in sorted order.
    for test_file in sorted(test_files):
        if run_test_file(test_file):
            passed_tests += 1

    failed_tests = total_tests - passed_tests
    print("\n=== Test Summary ===")
    print(f"Total tests: {total_tests}")
    print(f"Passed:      {passed_tests}")
    print(f"Failed:      {failed_tests}")

if __name__ == "__main__":
    main()
