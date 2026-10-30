import os
from types import SimpleNamespace
from openai import OpenAI
from dotenv import load_dotenv
from Utilities.utilities import log
from tools import TOOLS, run_tool

MAX_STEPS=10
load_dotenv() #by deafult looks for all .env file in the current directory 
clint= OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)
messages=[]
messages.append(
    {
        "role": "system",
        "content":(
        "You are a helpful humble agent. "
        "Answer general questions like programming, science, advice ect from you knowledge as a senior."
        "Use the tool when we ask particular questions like time, weather, location etc. "
        )
    }
)

def stream_chat(history):
    """
    Stream the chat response from the model.
    Returns the full response and a list of tool calls.
    """
    stream=clint.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=history,
        tools=TOOLS,
        stream=True
    )

    full_response=""
    calls={}
    label_printed=False
    try:
        for chunk in stream:
            if not chunk.choices:
                continue

            delta= chunk.choices[0].delta

            #1 Content Streaming : Do we have message content from LLM?
            if delta.content:
                if not label_printed:
                    print("Assistant: ", end="", flush=True)
                    label_printed=True
                print(delta.content, end="", flush=True)
                full_response+= delta.content

            #2 Tool Calls : Do we have tool calls from LLM?
            for tc in (delta.tool_calls or []):
                obj = calls.setdefault(
                    tc.index,
                    SimpleNamespace(id=None, function=SimpleNamespace(name="", arguments="")),
                )
                if tc.id:
                    obj.id = tc.id
                if tc.function and tc.function.name:
                    obj.function.name += tc.function.name
                if tc.function and tc.function.arguments:
                    obj.function.arguments += tc.function.arguments
    except KeyboardInterrupt:
        print("\nResponse stopped by user.")
        calls={}
    

    if label_printed:
        print() #print a new line after the assistant's response

    #Cinverting Dictionary into list
    calls_list = []
    for key in sorted(calls):
        calls_list.append(calls[key])

    return full_response, calls_list


def build_tool_calls_payload(tool_call):
    """
    Convert a tool call object to a dictionary representation.
    That API expects inside a sssitant message.
    """
    payload=[]
    for tool_call in tool_calls:
        tool_call_dict=({
            "id": tool_call.id,
            "type":"function",
            "function":{
                "name": tool_call.function.name,
                "arguments": tool_call.function.arguments
            }
        })
        payload.append(tool_call_dict)
    return payload

while True:
    input_text=input("\nUser: ")
    if input_text.lower() in ["exit", "quit", "bye", "end"]:
        break

    messages.append({"role": "user", "content": input_text})

    for step in range(MAX_STEPS):
        full_response, tool_calls= stream_chat(messages)
        
         # print(response.choices[0].message)
        # msg= response.choices[0].message

        if not tool_calls:
            break

        log(f"Step {step+1}: model requested {len(tool_calls)} tool call(s)")

        messages.append({
            "role":"assistant",
            "content": full_response,
            "tool_calls":build_tool_calls_payload(tool_calls)
        })

        for tool_call in tool_calls:
            result= run_tool(tool_call)
            messages.append({
                "role":"tool",
                "tool_call_id":tool_call.id,
                "content":str(result)
            })
    else:
        fallback="Max steps reached. Stopping. Model didn't able to give final answer. You can try again with a different prompt."
        messages.append({
            "role":"assistant",
            "content":fallback
        })
        print("Assistant:" +fallback)
        continue