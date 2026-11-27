import ast
import operator
OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul}
 
def safe_math(expression):
    def evaluate(node):
        if isinstance(node, ast.Expression): return evaluate(node.body)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float): return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in OPS:
            return OPS[type(node.op)](evaluate(node.left), evaluate(node.right))
        raise ValueError('Unsupported expression')
    return evaluate(ast.parse(expression, mode='eval'))
 
requests = ['18 + 24', '3 * 7', 'open("secret.txt")']
for request in requests:
    try: print(request, '->', safe_math(request))
    except (ValueError, SyntaxError) as error: print('Rejected:', error)

