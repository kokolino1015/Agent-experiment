import anthropic
from dotenv import load_dotenv

load_dotenv()
MODEL = "claude-haiku-4-5-20251001"
MAX_TURNS = 1
MAX_TOKENS = 1000
client = anthropic.Anthropic()

def add(number1, number2):
    return number1 + number2

def multiply(number1, number2):
    return number1 * number2

TOOLS = {"add": add, "multiply": multiply}

TWO_NUMBERS = {
    "type": "object",
    "properties": {
        "number1": {"type": "number", "description": "The first number."},
        "number2": {"type": "number", "description": "The second number."},
    },
    "required": ["number1", "number2"],
}

TOOL_SCHEMAS = [
    {"name": "add", "description": "Subtract two numbers.", "input_schema": TWO_NUMBERS},
    {"name": "multiply", "description": "Multiply two numbers.", "input_schema": TWO_NUMBERS},
]


def run_tool(name, tool_input):
    func = TOOLS.get(name)
    if func is None:
        return f"Unknown tool: {name}", True
    try:
        return str(func(**tool_input)), False
    except Exception as e:
        return f"{type(e).__name__}: {e}", True


def run_agent(question):
    messages = [{"role": "user", "content": question}]

    for _ in range(MAX_TURNS):
        response = client.messages.create(
            model=MODEL, max_tokens=MAX_TOKENS, tools=TOOL_SCHEMAS, messages=messages,
        )

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            if response.stop_reason == "end_turn":
                return "".join(b.text for b in response.content if b.type == "text")

            raise RuntimeError(f"Agent did not finish within {MAX_TOKENS} tokens")

        results = []
        for block in response.content:
            if block.type == "tool_use":
                content, is_error = run_tool(block.name, block.input)
                results.append({"type": "tool_result", "tool_use_id": block.id,
                                "content": content, "is_error": is_error})
        messages.append({"role": "user", "content": results})

    raise RuntimeError(f"Agent did not finish within {MAX_TURNS} turns")


if __name__ == "__main__":
    print(run_agent("What's 100 times 400, then add 250 to that?"))