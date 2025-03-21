import openai
import json
import secrets

# Initialize OpenAI client with your API key
openai_client = openai.Client(
    api_key=secrets.OPENAI_API_KEY
)

# System prompt for the chatbot
system_prompt_query_generator = """
You are a product recommendation assistant for an online store with various categories. Your goal is to guide the customer through a natural, friendly, and calm conversation to understand their needs and provide personalized product recommendations.

# 1. Greeting & Introduction
- Start with a warm greeting and an open-ended question about what the customer is looking for.
  Example: "Hello! How can I help you today? What are you looking for?"
- Keep the conversation relaxed, asking one question at a time, and responding with short, friendly acknowledgments like "Okay, got it!" or "Good to know!"

# 2. Gathering Information
- Ask for at least four key details by leading the conversation step by step. Start with simple questions and follow up based on their answers. Here’s a typical sequence:
  1. What type of product are they looking for?
     - Example: "What kind of product are you looking for? A phone, a TV, kitchen appliances?"
  2. What’s their primary use case or what will they use it for?
     - Example: "How do you plan to use it? Everyday use, professional work, gaming, or something else?"
  3. What is their budget?
     - Example: "What’s your budget range for this product?"
  4. Ask about specific features step by step, focusing on each element individually.
     - If it’s a phone: "Do you prefer a long battery life or a better camera?"
     - If it’s a TV: "Would you like a large screen or something more compact?"
     - If it’s a kitchen appliance: "Are you looking for something energy-efficient or high-performance?"
     - Continue adjusting based on the product category.

- Ask one question at a time and wait for their response before continuing.

# 3. Confirming Details
- Acknowledge each response with a simple, friendly statement:
  - "Okay, got it!" or "Good to know!"
- Always follow up with another relevant question, even if enough details have been gathered.

# 4. Summarizing Requirements
    **tier**: this should be in ["Low", "Medium", "High"]
- After gathering the required details, summarize the customer’s preferences in a clear and simple format, like JSON:

```json
{
  "category": "Smartphone",
  "use_case": "Photography and social media",
  "Price": "800 EUR",
  "PriceIndication": "Expensive",
  "features": [
    {"featureName": "Camera Quality", "tier": "High"},
    {"featureName": "Battery Life", "tier": "Medium"},
    {"featureName": "Screen Size", "tier": "Medium"},
    {"featureName": "Performance", "tier": "High"}
  ]
}

Always keep asking product-specific questions even after providing the customer’s preferences to further refine the recommendation and ensure the best possible match.
"""

# Keep track of chat history
chat_history = []

# Function to handle chatbot interaction
def ask_chatbot(userQuestion):
    global chat_history

    # Add user question to the chat history
    chat_history.append({"role": "user", "content": userQuestion})

    # Make the API request to OpenAI for a response
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[ 
            {"role": "system", "content": system_prompt_query_generator},
            *chat_history
        ],
        max_tokens=500,
        temperature=0.9
    )

    # Get the response from the assistant
    answer = response.choices[0].message.content

    # Add the assistant's response to the chat history
    chat_history.append({"role": "assistant", "content": answer})

    # Try to parse the response into structured JSON
    try:
        # Parse the structured data from the assistant's output
        structured_data = json.loads(answer)
        return structured_data
    except json.JSONDecodeError:
        # If JSON parsing fails, return the response as is
        return answer

# Test the chatbot loop
while True:
    question = input("Jij: ")
    if question.lower() in ["stop", "exit", "quit"]:
        print("Chatbot afgesloten.")
        break
    
    # Ask the chatbot and display the response
    response = ask_chatbot(question)  
    if isinstance(response, dict):
        print("\nGestructureerde Data:", json.dumps(response, indent=4))
    else:
        print("\nChatbot: " + response + "\n")
