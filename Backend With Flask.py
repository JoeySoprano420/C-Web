from flask import Flask, request, jsonify
from flask_cors import CORS
from antlr4 import InputStream, CommonTokenStream
from Generated.CWebLexer import CWebLexer
from Generated.CWebParser import CWebParser

app = Flask(__name__)
CORS(app)

@app.route("/parse", methods=["POST"])
def parse_code():
    code = request.json["code"]
    lexer = CWebLexer(InputStream(code))
    tokens = CommonTokenStream(lexer)
    parser = CWebParser(tokens)

    tree = parser.program()
    visitor = CWebVisitor()
    visitor.visit(tree)

    return jsonify({"llvm_ir": str(visitor.module)})

if __name__ == "__main__":
    app.run(port=5000)
