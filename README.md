# LyzrBoost Agent Demo Application

## Overview
LyzrBoost Agent Demo is a powerful demonstration of building agentic applications using the LyzrBoost framework integrated with Google's Gemini API. This application showcases both interactive chat capabilities and structured content generation workflows, making it an ideal starting point for developers looking to build AI-powered applications.

![Image](https://github.com/user-attachments/assets/50eebe05-bd5f-4214-9f19-e48114d0b6cc)

## 🌟 Features

### 1. Dual Mode Operation
- **Interactive Mode**: Real-time chat interface for direct Q&A
- **Workflow Mode**: Structured content generation pipeline

### 2. Content Generation Pipeline
- Research phase
- Content writing
- Professional editing
- Formatted output generation

### 3. Integration Features
- Google Gemini API integration
- LyzrBoost workflow orchestration
- Session management
- Error handling

## 🚀 Getting Started

### Prerequisites
```bash
- Python 3.7 or higher
- pip (Python package manager)
```

### Installation

1. Clone the repository
```bash
git clone [repository-url]
cd lyzrboost-agent-demo
```

2. Install dependencies
```bash
python setup_demo.py
```

3. Set up environment variables
```bash
# Add your Gemini API key
export GEMINI_API_KEY="your-api-key"
```

## 💻 Usage

### Interactive Mode
Start a conversational session with the agent:
```bash
python mock_agent_demo.py -i
```

Example interaction:




### Workflow Mode
Generate comprehensive content on a specific topic:
```bash
python mock_agent_demo.py "Your Topic"
```

With verbose output:
```bash
python mock_agent_demo.py "Your Topic" --verbose
```

## 🛠️ Command Options

| Option | Description |
|--------|-------------|
| `-i, --interactive` | Enable interactive chat mode |
| `-v, --verbose` | Show detailed output |
| `--help` | Display help message |

## 📋 Workflow Architecture

The application follows a structured workflow:

1. **Initialization**
   - Session creation
   - API configuration
   - Resource preparation

2. **Processing**
   - Research phase
   - Content generation
   - Editing and refinement
   - Output formatting

3. **Output Handling**
   - Result presentation
   - Session management
   - Error handling

## 🔧 Configuration

### Environment Variables
```bash
GEMINI_API_KEY=your-api-key
```

### API Configuration
- Model: gemini-2.0-flash
- Default timeout: 30 seconds
- Max retries: 3

## 📚 Use Cases

1. **Content Creation**
   - Blog post generation
   - Technical documentation
   - Research summaries

2. **Interactive Assistant**
   - Q&A sessions
   - Technical support
   - Educational tutoring

3. **Research Tool**
   - Topic exploration
   - Data analysis
   - Information gathering

## ⚡ Benefits of Using LyzrBoost

1. **Developer Productivity**
   - Simplified workflow management
   - Reduced boilerplate code
   - Automated session handling

2. **Flexibility**
   - Easy mode switching
   - Customizable workflows
   - Extensible architecture

3. **Reliability**
   - Built-in error handling
   - Session persistence
   - Robust API integration

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔍 Troubleshooting

Common issues and solutions:

1. **API Key Issues**
   ```bash
   # Check if API key is set
   echo $GEMINI_API_KEY
   ```

2. **Dependencies**
   ```bash
   # Reinstall dependencies
   python setup_demo.py
   ```

3. **Version Conflicts**
   ```bash
   # Check Python version
   python --version
   ```

## 📮 Support

For support, please:
1. Check the documentation
2. Search existing issues
3. Create a new issue if needed

## 🔄 Updates

Stay updated with the latest features and improvements:
```bash
git pull origin main
python setup_demo.py
```

---

Built with ❤️ using LyzrBoost and Google Gemini API
