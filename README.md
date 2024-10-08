
# Okapi_AI by Atou and Jeremy 💬

Welcome to **Okapi_AI**, an interactive Streamlit app that integrates the power of large language models (LLMs) for a fun and insightful experience! This app allows users to chat with various AI models, customizing their interaction by selecting different models and token limits.

## Features

- **Model Selection**: Choose between different LLMs such as Gemma, LLaMA, and Mixtral.
- **Token Limit Customization**: Adjust the number of tokens (words) for model responses using a dynamic slider.
- **Interactive Chat**: Engage in a live chat interface where messages are streamed in real-time.
- **Groq API Integration**: The app leverages the Groq API for processing chat completions.

## Installation

To run this app locally, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-repository/okapi_ai.git
   cd okapi_ai
   ```

2. **Install dependencies:**

   Make sure you have Python installed (preferably version 3.8+). Then, install the required packages with pip:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**

   Create a `.env` file in the root directory of your project and set your `GROQ_API_KEY`:

   ```env
   GROQ_API_KEY=your_api_key_here
   ```

4. **Run the app:**

   To start the Streamlit app, run:

   ```bash
   streamlit run app.py
   ```

## Usage

1. **Select a Model**: Choose from the dropdown menu to select an AI model for your conversation.
2. **Adjust Max Tokens**: Use the slider to define the maximum number of tokens the model can use in its response.
3. **Start Chatting**: Enter your prompt in the chat input, and receive real-time responses from the selected model.

## Models Available

- **Gemma-7b-it** (Google)
- **LLaMA2-70b-chat** (Meta)
- **LLaMA3-70b-8192** (Meta)
- **LLaMA3-8b-8192** (Meta)
- **Mixtral-8x7b-Instruct-v0.1** (Mistral)

## Developer Notes

- **API Key**: The app uses the Groq API to generate chat completions. Ensure you have a valid API key set in your `.env` file.
- **Streaming Responses**: The app streams responses from the Groq API, making the chat interaction more dynamic and real-time.

## Contributors

- **Atou** 
- **Jeremy** 

## License
