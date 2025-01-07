"""
Improved OpenAI API wrapper example
"""

import os
import json
from openai import OpenAI, OpenAIError

MODEL = "gpt-4"  # Corrected model name

client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")


def find_product(_sql_query):
    """
    Get a list of products from a SQL query
    """
    results = [
        {"name": "pen", "color": "blue", "price": 2.5},
        {"name": "pen", "color": "black", "price": 1.5},
        {"name": "pen", "color": "white", "price": 0.5},
    ]
    return results


function_find_product = {
    "name": "find_product",
    "description": "Get a list of products from a SQL query",
    "parameters": {
        "type": "object",
        "properties": {
            "sql_query": {
                "type": "string",
                "description": "A SQL query",
            },
        },
        "required": ["sql_query"],
    },
}

tools = [{"type": "function", "function": function_find_product}]

def process_product_query(user_query):
    """
    Process a user query to find products

    :param user_query: The user query
    :return: The response
    """
    try:
        # Initial message
        messages = [{"role": "user", "content": user_query}]

        # First API call
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
        )

        # Process tool calls
        response_message = response.choices[0].message
        if response_message.tool_calls:
            tool_call = response_message.tool_calls[0]
            function_args = json.loads(tool_call.function.arguments)

            # Execute function and add result to messages
            products = find_product(function_args["sql_query"])
            messages.extend(
                [
                    response_message,
                    {
                        "role": "tool",
                        "content": json.dumps(products),
                        "tool_call_id": tool_call.id,
                    },
                ]
            )

            final_response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
            )

            return final_response.choices[0].message.content

    except (OpenAIError, json.JSONDecodeError) as e:
        return f"Error processing query: {str(e)}"


result = process_product_query(
    "I need the top 2 products where the price is less than 1"
)
print(result)
