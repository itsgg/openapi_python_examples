"""
OpenAI Function Calling Implementation

This script demonstrates how to implement OpenAI's function calling feature,
allowing AI models to invoke predefined functions and tools. It provides a
structured way to handle tool calls in conversational AI applications.

Dependencies:
    - openai: The official OpenAI Python client library
    - Environment variable OPENAI_API_KEY must be set
    - json: For parsing function parameters

Features:
    - Define and register custom functions for AI to call
    - Handle structured function calls from AI responses
    - Support for multiple function definitions
    - Error handling and validation of function calls
    - Automatic parameter parsing and type checking

Example:
    $ export OPENAI_API_KEY='your-api-key'
    $ python tool_call.py
"""

import os
import json
from typing import List, Dict, Any, Optional
from openai import OpenAI, OpenAIError

# Configuration
MODEL = "gpt-4"
client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")


def find_product(sql_query: str) -> List[Dict[str, Any]]:
    """
    Get a list of products matching the SQL query criteria.

    Args:
        sql_query (str): SQL query to filter products

    Returns:
        List[Dict[str, Any]]: List of product dictionaries with name, color, and price
    """
    # Mock database results
    results = [
        {"name": "pen", "color": "blue", "price": 2.5},
        {"name": "pen", "color": "black", "price": 1.5},
        {"name": "pen", "color": "white", "price": 0.5},
    ]
    return results


# Function definition for OpenAI
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


def process_product_query(user_query: str, model: str = MODEL) -> str:
    """
    Process a user query to find and describe products.

    Args:
        user_query (str): Natural language query about products
        model (str): OpenAI model to use

    Returns:
        str: Generated response about the requested products

    Raises:
        ValueError: If API key is not set or query is empty
        OpenAIError: If API call fails
        json.JSONDecodeError: If function arguments are invalid
    """
    if not client.api_key:
        raise ValueError("OpenAI API key not found in environment variables")
    if not user_query.strip():
        raise ValueError("Query cannot be empty")

    try:
        # Initial message
        messages = [{"role": "user", "content": user_query}]

        # First API call to get function call
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
        )

        # Process tool calls
        response_message = response.choices[0].message
        if not response_message.tool_calls:
            return "No product query could be processed from your request."

        tool_call = response_message.tool_calls[0]
        function_args = json.loads(tool_call.function.arguments)

        # Execute function and add result to messages
        products = find_product(function_args["sql_query"])
        if not products:
            return "No products found matching your criteria."

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

        # Final API call to generate response
        final_response = client.chat.completions.create(
            model=model,
            messages=messages,
        )

        return final_response.choices[0].message.content

    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid function arguments: {str(e)}", e.doc, e.pos)
    except OpenAIError as e:
        raise OpenAIError(f"OpenAI API error: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}")


def main():
    """Main function to demonstrate product query processing."""
    try:
        query = "I need the top 2 products where the price is less than 1"
        result = process_product_query(query)
        print(f"\nQuery: {query}")
        print(f"Result: {result}")

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
