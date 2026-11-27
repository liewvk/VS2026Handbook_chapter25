
import ast
import json
import operator
import os

from datetime import date
from urllib.request import Request, urlopen

# Supported mathematical operators
OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv
}


def safe_math(expression):
    def eval_node(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in OPS:
            return OPS[type(node.op)](
                eval_node(node.left),
                eval_node(node.right)
            )

        raise ValueError("Unsupported expression")

    if len(expression) > 80:
        raise ValueError("Expression too long")

    return eval_node(ast.parse(expression, mode="eval").body)


def tool_call(name, argument):
    if name == "date":
        return str(date.today())

    if name == "calculator":
        return str(safe_math(argument))

    return "Tool rejected"


# Get user's question
question = input("Ask the agent: ")

model = os.getenv("OLLAMA_MODEL", "qwen3.5:4b")

# Instructions for the AI model
instruction = (
    "Return ONLY a JSON object with keys tool and argument. "
    "tool must be date or calculator; for date argument is empty. "
    "For calculator use arithmetic with + - * / only. "
    "If neither applies, return tool=none. "
    "Question: " + question
)

# Prepare the Ollama request
body = json.dumps({
    "model": model,
    "stream": False,
    "messages": [
        {
            "role": "user",
            "content": instruction
        }
    ]
})

request = Request(
    "http://localhost:11434/api/chat",
    data=body.encode(),
    headers={"Content-Type": "application/json"}
)

try:
    # Send request to Ollama
    with urlopen(request, timeout=120) as r:
        response = json.load(r)

    # Parse the model's JSON response
    choice = json.loads(response["message"]["content"])

    name = choice.get("tool", "none")
    argument = choice.get("argument", "")

    if not isinstance(argument, str):
        raise ValueError("Invalid argument")

    # Execute the selected tool
    print(
        "Tool:", name,
        "Result:", tool_call(name, argument)
    )

except (
    ValueError,
    KeyError,
    TypeError,
    OSError,
    ZeroDivisionError,
    OverflowError,
    RecursionError
) as error:
    print("The request could not be completed:", error)
