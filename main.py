from lexer import SimpleLexer
from parser import SimpleParser
from util import build_tree

# if __name__ == '__main__':
#     data = open("sample.txt", "r").read()
#     lexer = SimpleLexer()
#     for tok in lexer.tokenize(data):
#         print('type=%r, value=%r' % (tok.type, tok.value))

if __name__ == '__main__':
    lexer = SimpleLexer()
    parser = SimpleParser()

    data = open("sample.txt", "r").read()
    result = parser.parse(lexer.tokenize(data))
    # print(result)
    print(build_tree(result))


