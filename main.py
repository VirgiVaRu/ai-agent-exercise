import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from call_function import *

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("couldn't find an API key")
    
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages =[types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    client = genai.Client(api_key=api_key)

    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=messages, 
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0,
                tools=[available_functions]
            )
        )

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if args.verbose:
            if response.usage_metadata == None:
                raise RuntimeError("could not find usage metadata. potential failed API request")
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        
        function_results = []
        if response.function_calls != None:
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, args.verbose)
                if not function_call_result.parts:
                    raise Exception
                if function_call_result.parts[0].function_response == None:
                    raise Exception
                if function_call_result.parts[0].function_response.response == None:
                    raise Exception
                
                function_results.append(function_call_result.parts[0])

                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                
        else:
            print(response.text)
            return

        messages.append(types.Content(role="user", parts=function_results))
    
    sys.exit(1)

if __name__ == "__main__":
    main()
