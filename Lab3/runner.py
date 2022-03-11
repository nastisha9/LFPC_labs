from lexer import *

text = open(r'C:\Users\Nastea\lfpclab\lab3\dot.txt')
lexer = Lexer('<dot.txt>', text.read())
result, error = lexer.make_tokens()
if error:
    print(error)
else:
    print("\n".join(map(str, result)))
