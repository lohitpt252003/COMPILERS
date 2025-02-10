**GitHub Repository**: [https://github.com/lohitpt252003/COMPILERS.git](https://github.com/lohitpt252003/COMPILERS.git)  
**Team Members**:  
- LOHIT P TALAVAR (210564)  
- KARTAVYA (180343)  
- P LOKESH NAYAK (210710)  

---

## **Milestone 1**

---

### **1. `token.py`**

The `token.py` module implements the **tokenizer** for CHIRONLANG. It converts a CHIRONLANG source string into a list of tokens. Each token contains the following information:

- **Type**: The category of the token (e.g., `NUMBER`, `IDENTIFIER`, `KEYWORD`, `OPERATOR`, etc.).
- **Value**: The string representation of the token.
- **Line and Column**: The starting position of the token in the source code for debugging and error reporting.

#### **Supported Keywords**
The following keywords are recognized by the tokenizer:
```
if, else, repeat, penup, pendown, forward, backward,
left, right, go, true, false, input
```

#### **Additional Features**
- Variables in CHIRONLANG start with a colon (`:`).
- Supported operators include:
  - Comparison: `==`, `!=`, `<=`, `>=`, `<`, `>`
  - Logical: `&&`, `||` (or `∥`)
  - Arithmetic: `+`, `-`, `*`, `/`

---

### **2. `ast.py`**

The `ast.py` module defines the **Abstract Syntax Tree (AST)** node classes for CHIRONLANG. Each AST node stores its location (line and column) to support debugging and error reporting.

#### **AST Constructs**
The AST supports the following constructs:
- **Program**: A sequence of statements.
- **Assignment**: Variable assignment (`variable = expression`).
- **IfStatement**: Conditional statement with an optional `else` clause.
- **RepeatStatement**: Loop structure (`repeat <expression> [ <statements> ]`).
- **PenStatement**: Pen control (`penup` or `pendown`).
- **MoveStatement**: Movement commands (`forward`, `backward`, `left`, `right`, `go`).
- **BinaryOp and UnaryOp**: Binary and unary operations.
- **Number**: Numeric literals.
- **Var**: Variables (identifiers starting with a colon `:`).

---

### **3. `test.py`**

The `test.py` script serves as a **test harness** for the CHIRONLANG compiler. It performs the following tasks:
1. Scans the current directory for all `.t1` test files.
2. Tokenizes and parses each CHIRONLANG source file using the tokenizer from `token.py` and the AST generator from `ast.py`.
3. Prints the tokens and AST for each test file, along with the test file name.
4. Continues processing even if an individual test fails, providing a summary at the end.

#### **Supported Keywords**
The parser supports the following keywords:
```
if, else, repeat, penup, pendown, forward, backward,
left, right, go, true, false, input
```

#### **Error Handling**
- If a test file fails during tokenization or parsing, the error is reported, and the harness continues processing the remaining files.
- A summary of all tests (passed/failed) is printed at the end.

---

### **How to Use**

1. Clone the repository:
   ```bash
   git clone https://github.com/lohitpt252003/COMPILERS.git
   cd COMPILERS
   ```

2. Place your `.t1` test files in the same directory as the scripts.

3. Run the test harness:
   ```bash
   python test.py
   ```

4. Review the output:
   - Tokens and AST for each test file will be printed.
   - A summary of passed and failed tests will be displayed.

---