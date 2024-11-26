from poe_api_wrapper import AsyncPoeApi
import asyncio

# Replace with your actual tokens
tokens = {
    'p-b': 'Fs1mwf2Ym3oGvXooZG6Zsg%3D%3D', 
    'p-lat': 'z1CIIXXmuEyntM4RMVrNe3puY2Us433OUME1hanapg%3D%3D',
}

check_key = "0xaaaa"

async def gpt3_5(prompt, key):
    # Create an instance of the AsyncPoeApi client
    client = await AsyncPoeApi(tokens=tokens).create()
    
    if check_key != key:
        print("Wrong Key!")
        return None  # Return None or an appropriate error message

    # Send the message and collect the response
    response = []
    try:
        async for chunk in client.send_message(bot="gpt3_5", message=prompt):
            print(chunk["response"], end='', flush=True)  # Print the response in real-time
            response.append(chunk["response"])  # Collect the response chunks
    except Exception as e:
        print(f"Error during message sending: {str(e)}")
        return None  # Handle the error appropriately

    return ''.join(response)  # Return the complete response as a single string

async def capybara(prompt, key):
    # Create an instance of the AsyncPoeApi client
    client = await AsyncPoeApi(tokens=tokens).create()
    
    if check_key != key:
        print("Wrong Key!")
        return None  # Return None or an appropriate error message

    # Send the message and collect the response
    response = []
    try:
        async for chunk in client.send_message(bot="capybara", message=prompt):
            print(chunk["response"], end='', flush=True)  # Print the response in real-time
            response.append(chunk["response"])  # Collect the response chunks
    except Exception as e:
        print(f"Error during message sending: {str(e)}")
        return None  # Handle the error appropriately

    return ''.join(response)  # Return the complete response as a single string