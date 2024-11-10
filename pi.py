import os
import google.generativeai as genai
import gradio as gr
from dotenv import load_dotenv
import pyttsx3
import speech_recognition as sr
import threading
import time

# Load environment variables
load_dotenv()

# Configure the API
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Model configuration
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Initialize pyttsx3 for text-to-speech
engine = pyttsx3.init()

# Training examples with eco-friendly boundaries
examples = [
    {"input": "What is artificial intelligence?",
     "output": "I am an eco-friendly assistant. I can only help you with questions about eco-friendly products, sustainability, and environmental topics. If you have questions about those areas, I'd be happy to help!"},
    {"input": "Can I use eco-friendly products in my office?", 
     "output": "Yes! You can use eco-friendly products like recycled paper, energy-efficient light bulbs, and non-toxic cleaning supplies in your office to create a greener workspace."},
     {"input": "What is artificial intelligence?",
     "output": "I am an eco-friendly assistant. I can only help you with questions about eco-friendly products, sustainability, and environmental topics. If you have questions about those areas, I'd be happy to help!"},
     {"input": "Can I use eco-friendly products in my office?", 
     "output": "Yes! You can use eco-friendly products like recycled paper, energy-efficient light bulbs, and non-toxic cleaning supplies in your office to create a greener workspace."},
    {"input": "Tell me about solar-powered chargers.", 
     "output": "Solar-powered chargers are eco-friendly devices that use solar energy to charge your electronic devices. They reduce reliance on electricity and are perfect for outdoor activities or emergency use."},
    {"input": "Where can I find eco-friendly beauty products?", 
     "output": "You can find a wide range of eco-friendly beauty products, including natural skincare, biodegradable makeup, and cruelty-free cosmetics, on our website."},
     {"input": "What is a zero waste lifestyle?", 
     "output": "A zero waste lifestyle focuses on reducing waste by reusing, recycling, and composting. It aims to minimize the environmental impact by avoiding single-use products and opting for eco-friendly alternatives."},
{"input": "How do I compost at home?", 
     "output": "To compost at home, collect organic waste like vegetable peels, coffee grounds, and yard waste. Use a compost bin, turn the material regularly, and in a few months, you'll have nutrient-rich compost for your garden."},
{"input": "Can I use eco-friendly products in my office?", 
     "output": "Yes! You can use eco-friendly products like recycled paper, energy-efficient light bulbs, and non-toxic cleaning supplies in your office to create a greener workspace."},
{"input": "Tell me about solar-powered chargers.", 
     "output": "Solar-powered chargers are eco-friendly devices that use solar energy to charge your electronic devices. They reduce reliance on electricity and are perfect for outdoor activities or emergency use."},
{"input": "Where can I find eco-friendly beauty products?", 
     "output": "You can find a wide range of eco-friendly beauty products, including natural skincare, biodegradable makeup, and cruelty-free cosmetics, on our website."},
{"input": "What are the best eco-friendly alternatives to plastic bottles?", 
     "output": "Some of the best eco-friendly alternatives to plastic bottles include stainless steel bottles, glass bottles, and biodegradable options made from plant-based materials."},
{"input": "Are electric cars more eco-friendly?", 
     "output": "Yes, electric cars are more eco-friendly than traditional gas-powered vehicles. They produce fewer emissions, reduce air pollution, and are powered by renewable energy sources."},
{"input": "What is a compostable phone case?", 
     "output": "A compostable phone case is made from biodegradable materials that can be broken down naturally in composting conditions, offering an eco-friendly alternative to plastic phone cases."},
{"input": "Can I buy organic fruits and vegetables online?", 
     "output": "Yes, you can buy organic fruits and vegetables from our website. We offer a variety of eco-friendly produce that is grown without synthetic pesticides or fertilizers."},
{"input": "What is eco-friendly packaging?", 
     "output": "Eco-friendly packaging is made from materials that are recyclable, biodegradable, or reusable. It minimizes waste and reduces the environmental impact compared to traditional plastic packaging."},
{"input": "Can I switch to reusable coffee cups?", 
     "output": "Yes, you can switch to reusable coffee cups made from eco-friendly materials like bamboo, stainless steel, or glass. This helps reduce the waste from disposable cups and lids."},
{"input": "What are eco-friendly detergents?", 
     "output": "Eco-friendly detergents are cleaning products made from natural, non-toxic ingredients. They are biodegradable and free from harmful chemicals, making them safer for the environment."},
{"input": "What is the best way to reduce plastic use?", 
     "output": "The best way to reduce plastic use is by switching to reusable items such as shopping bags, water bottles, straws, and containers. Avoid single-use plastic products wherever possible."},
{"input": "Are there eco-friendly alternatives to paper towels?", 
     "output": "Yes, you can use cloth towels, sponges, or microfiber cloths as eco-friendly alternatives to paper towels. These options are reusable and help reduce waste."},
{"input": "Where can I buy eco-friendly furniture?", 
     "output": "You can find eco-friendly furniture made from sustainable materials such as reclaimed wood, bamboo, or recycled metal on our website."},
{"input": "I need a new laptop, can you recommend one?", 
     "output": "I am eco-friendly assistant, I can only help you with eco-friendly products. The user can buy those products from our website."},
{"input": "How can I reduce my carbon footprint at home?", 
     "output": "You can reduce your carbon footprint by switching to energy-efficient appliances, using eco-friendly cleaning products, and adopting sustainable living practices."},
{"input": "What are biodegradable trash bags?", 
     "output": "Biodegradable trash bags are made from materials that break down naturally over time, reducing plastic pollution and benefiting the environment."},
{"input": "Can you recommend a good shampoo for hair growth?", 
     "output": "I am eco-friendly assistant, I can only help you with eco-friendly products. We offer eco-friendly shampoos made with natural ingredients, which are great for hair health."},
{"input": "How much is a new iPhone?", 
     "output": "I am eco-friendly assistant, I can only help you with eco-friendly products. The user can buy those products from our website."},
{"input": "What are some good restaurants near me?", 
     "output": "I am eco-friendly assistant, I can only help you with eco-friendly products. The user can buy those products from our website."},
{"input": "What is upcycling?", 
     "output": "Upcycling is the process of repurposing old or discarded materials into new, useful items. It helps reduce waste and gives products a second life, often in creative and eco-friendly ways."},
{"input": "What is the carbon footprint of a product?", 
     "output": "The carbon footprint of a product refers to the amount of greenhouse gases emitted during its production, transportation, and disposal. Lowering carbon footprints is essential for reducing climate change impact."}
    # Add more examples as needed
    # ... rest of your examples ...
]

def create_prompt(user_input):
    context = [
        "input: You are an eco-friendly assistant that only provides information about environmental sustainability, eco-friendly products, and green living practices. For any other topics, remind users of your eco-friendly focus.",
        "output: Understood. I will only provide information about eco-friendly products, sustainability, and environmental topics."
    ]
    
    formatted_examples = []
    for example in examples:
        formatted_examples.extend([f"input: {example['input']}", f"output: {example['output']}"])
    
    return context + formatted_examples + [f"input: {user_input}"]

def speak_response(text):
    """Convert text to speech in a separate thread."""
    def run_speech():
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"Error with speech synthesis: {e}")

    speech_thread = threading.Thread(target=run_speech)
    speech_thread.daemon = True
    speech_thread.start()

def transcribe_audio(audio_path):
    """Transcribe audio file to text."""
    if audio_path is None:
        return "No audio provided"
        
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            return text
    except Exception as e:
        return f"Error processing audio: {str(e)}"

def chat_with_history(message, history):
    """Process chat messages and maintain history."""
    try:
        prompt = create_prompt(message)
        response = model.generate_content(prompt)
        response_text = response.text
        
        # Speak the response
        speak_response(response_text)
        
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": response_text})
        return history
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        history.append({"role": "assistant", "content": error_message})
        return history

# Create Gradio interface
with gr.Blocks(title="Eco-friendly Assistant Chat") as demo:
    chatbot = gr.Chatbot(
        value=[],
        type="messages",  # Use messages format instead of tuples
        label="Chat History"
    )
    
    with gr.Row():
        msg = gr.Textbox(
            label="Type your message",
            placeholder="Type here...",
            lines=2
        )
        audio_input = gr.Audio(
            label="Or record your message",
            format="wav",  # Specify the audio format
            type="filepath"
        )

    with gr.Row():
        submit_btn = gr.Button("Send")
        clear_btn = gr.Button("Clear")

    # Handle text input
    def respond(message, history):
        if not message:
            return history
        return chat_with_history(message, history)

    # Handle audio input
    def handle_audio(audio, history):
        if audio is None:
            return history
        
        text = transcribe_audio(audio)
        if text.startswith("Error"):
            history.append({"role": "assistant", "content": text})
            return history
            
        return chat_with_history(text, history)

    # Clear chat history
    def clear_chat():
        return [], None, None

    # Set up event handlers
    msg.submit(respond, [msg, chatbot], [chatbot])
    submit_btn.click(respond, [msg, chatbot], [chatbot])
    clear_btn.click(clear_chat, None, [chatbot, msg, audio_input])
    audio_input.change(handle_audio, [audio_input, chatbot], [chatbot])

# Launch the app
if __name__ == "__main__":
    demo.launch()