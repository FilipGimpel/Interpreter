from lexer import SimpleLexer
from parser import SimpleParser
from util import build_tree

# You can clone this repository from https://github.com/FilipGimpel/Interpreter
# SLY library and python is all that is required to run this project:
# pip install sly

if __name__ == '__main__':
    lexer = SimpleLexer()
    parser = SimpleParser()

    data = open("sample.txt", "r").read()
    result = parser.parse(lexer.tokenize(data))
    print(build_tree(result))

    # for i in lexer.tokenize(data):
    #     print(i)
