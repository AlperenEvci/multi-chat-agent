# AI Assistant 🤖

A modern, intelligent AI assistant with chat and image generation capabilities, built with Streamlit and powered by advanced language models.

## 🌐 Live Demo

Try it out: [Multi-Chat Agent Demo](https://multi-chat-agent.streamlit.app/)

![AI Assistant Interface](docs/images/app_screenshot.png)

## ✨ Features

- **Modern, Sleek Interface**: Clean and intuitive design with a dark theme and smooth animations
- **Multi-Model Support**:
  - Gemini Pro (1.5 & 2.5)
  - DeepSeek (Chat & Coder)
  - Gemma
  - Access via OpenRouter (DeepSeek, Gemma)
- **Real-time Chat**: Interactive conversations with AI models
- **Image Generation**: Create AI-powered images using Google's Imagen
- **Conversation Management**: Save and manage multiple chat sessions
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Database Integration**: MongoDB Atlas for secure and scalable data storage
- **Cloud Deployment**: Hosted on Streamlit Cloud for easy access

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- MongoDB Atlas account (for database)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/AlperenEvci/multi-chat-agent.git
cd multi-chat-agent
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up your environment variables in `.streamlit/secrets.toml`:

```toml
[api_keys]
GOOGLE_API_KEY = "your_google_api_key"
GROQ_API_KEY = "your_groq_api_key"
DEEPSEEK_API_KEY = "your_deepseek_api_key"
OPENROUTER_API_KEY = "your_openrouter_api_key"

[google_cloud]
GOOGLE_CLOUD_PROJECT = "your_project_id"
GOOGLE_CLOUD_LOCATION = "your_location"

[database]
MONGO_URI = "your_mongodb_connection_string"
DB_NAME = "chat_agent"
```

4. Run the application:

```bash
streamlit run app.py
```

## 🎯 Usage

1. **Select AI Model**: Choose from various available models in the sidebar
2. **Start a Conversation**: Click "New Conversation" to begin chatting
3. **Chat Interface**: Type your messages in the input field at the bottom
4. **Image Generation**: Switch to the Image Generation tab to create AI-powered images
5. **Conversation Management**: Your conversations are automatically saved and can be accessed from the sidebar

## 🛠️ Technical Features

- **Streamlit**: Modern web framework for Python applications
- **LangChain**: Framework for developing applications powered by language models
- **Google AI Platform**: Integration for Imagen image generation
- **MongoDB Atlas**: Cloud database for conversation storage
- **Custom CSS**: Enhanced visual styling and animations
- **Multiple AI Models**: Support for various language models
- **Cloud Deployment**: Streamlit Cloud hosting

## 🎨 UI/UX Features

- Customized dark theme
- Smooth animations and transitions
- Intuitive navigation
- Clear visual hierarchy
- Responsive message bubbles
- Modern button and input styling
- Loading animations and feedback
- Emoji integration for better visual cues

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

If you have any questions or run into issues, please open an issue in the GitHub repository.

## 🙏 Acknowledgments

- Thanks to the Streamlit team for their amazing framework
- Thanks to Google, DeepSeek, and other AI providers for their powerful models
- Thanks to the open-source community for their valuable contributions
