

# Set of all keywords as per the documentation.
KEYWORDS = {
    "if", "else", "repeat", "penup", "pendown",
    "forward", "backward", "left", "right", "go",
    "true", "false", "input"
}

class Token:
    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line      # 1-indexed line number
        self.column = column  # 1-indexed column number

    def __repr__(self):
        return f"Token({self.type}, {self.value}, line={self.line}, col={self.column})"

def tokenize(text):
    tokens = []
    i = 0
    line = 1
    column = 1
    length = len(text)
    
    while i < length:
        ch = text[i]
        
        # Update for newlines.
        if ch == '\n':
            i += 1
            line += 1
            column = 1
            continue

        # Skip other whitespace (spaces, tabs)
        if ch.isspace():
            i += 1
            column += 1
            continue

        # Record the starting position for the token.
        start_line = line
        start_column = column

        # --- Numeric literals ---
        if ch.isdigit():
            num_str = ch
            i += 1
            column += 1
            while i < length and text[i].isdigit():
                num_str += text[i]
                i += 1
                column += 1
            tokens.append(Token("NUMBER", num_str, start_line, start_column))
            continue

        # --- Variables (identifiers starting with a colon) ---
        
        if ch == ':':
            ident_str = ch
            i += 1
            column += 1
            while i < length and (text[i].isalnum() or text[i] == '_'):
                ident_str += text[i]
                i += 1
                column += 1
            tokens.append(Token("IDENT", ident_str, start_line, start_column))
            continue

        # --- Identifiers and Keywords ---
        if ch.isalpha():
            ident_str = ch
            i += 1
            column += 1
            while i < length and (text[i].isalnum() or text[i] == '_'):
                ident_str += text[i]
                i += 1
                column += 1
            if ident_str in KEYWORDS:
                tokens.append(Token("KEYWORD", ident_str, start_line, start_column))
            else:
                tokens.append(Token("IDENT", ident_str, start_line, start_column))
            continue

        # --- Operators and Symbols ---
        # multi-character operators for =, !, <, >.
        if ch in "=!<>":
            op = ch
            if i + 1 < length and text[i+1] == '=':
                op += '='
                i += 2
                column += 2
            else:
                i += 1
                column += 1
            tokens.append(Token("SYMBOL", op, start_line, start_column))
            continue

        # Logical AND: &&
        if ch == '&':
            if i + 1 < length and text[i+1] == '&':
                tokens.append(Token("SYMBOL", "&&", start_line, start_column))
                i += 2
                column += 2
                continue
            # Single '&' not defined in CHIRONLANG.
            tokens.append(Token("UNKNOWN", ch, start_line, start_column))
            i += 1
            column += 1
            continue

        # Logical OR: either ∥ or ||
        if ch == '∥':
            tokens.append(Token("SYMBOL", "∥", start_line, start_column))
            i += 1
            column += 1
            continue
        if ch == '|':
            if i + 1 < length and text[i+1] == '|':
                tokens.append(Token("SYMBOL", "||", start_line, start_column))
                i += 2
                column += 2
                continue
            else:
                tokens.append(Token("SYMBOL", ch, start_line, start_column))
                i += 1
                column += 1
                continue

        # Single-character symbols: punctuation, arithmetic operators, parentheses, etc.
        if ch in "+-*/(),;[]{}":
            tokens.append(Token("SYMBOL", ch, start_line, start_column))
            i += 1
            column += 1
            continue

        # Fallback: If character is unrecognized, record as UNKNOWN.
        tokens.append(Token("UNKNOWN", ch, start_line, start_column))
        i += 1
        column += 1

    return tokens

# For simple testing of the tokenizer.
if __name__ == "__main__":
    sample_code = """
    input (:sX, :sY)
    :x = 20; :y = 100; :z = 60
    repeat 6 [
      if (:x != :y) [
        if (:x > :y) [ right :x ]
        else [ left :y ]
      ] else [
        if((:x <= :z) ∥ (:y <= :z))[
          :x = :z / :x
          :z = :y / :z
        ]
      ]
      forward :x; right :y
      forward :z; left :z
    ]
    """
    token_list = tokenize(sample_code)
    for token in token_list:
        print(token)
