from lexer import SimpleLexer
from parser import SimpleParser
from util import build_tree

if __name__ == '__main__':
    lexer = SimpleLexer()
    parser = SimpleParser()

    data = open("sample.txt", "r").read()
    result = parser.parse(lexer.tokenize(data))
    # print(result)
    print(build_tree(result))

    # for i in lexer.tokenize(data):
    #     print(i)
