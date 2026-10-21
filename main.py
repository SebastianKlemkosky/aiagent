import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function
import json


load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

def run_agent_turn(messages, verbose, user_prompt):
    response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages, # type: ignore
            tools=available_functions,  # type: ignore
        )
        
    if response.usage is None:
            raise RuntimeError("Failed API request")
            
    message = response.choices[0].message
    messages.append(message)
    if message.tool_calls == None:
        if verbose:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
            print(f"Response:\n {response.choices[0].message.content}")
        else:
            print(f"{response.choices[0].message.content}")
        return True    
    else:   
        for tool_call in message.tool_calls:
            result = call_function(tool_call, verbose)
            if not result.get("content"):
                raise Exception(f"Empty content for function call: {tool_call.function.name}") # type: ignore
            messages.append(result)
            if verbose:
                print(f"-> {result['content']}")

def main():
    if api_key is None:
        raise RuntimeError("API key was not found")
    
    
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`  
    


    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    
    for _ in range(20):
        # call the model, handle responses, etc.
        has_final_response = run_agent_turn(messages, args.verbose, args.user_prompt)
        if has_final_response:
            break
    else:
        print("Agent reached the maximum number of iterations without producing a final response.")
        
if __name__ == "__main__":
    main()
