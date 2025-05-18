# AI Research Assistant
AI-powered research assistant that helps Academic Professionals and Startup Founders gather deep, contextual information about specific individuals for grant preparation, collaboration planning, and funding opportunities.

## Project Description
The AI Research Assistant is a Flask-based REST API that leverages OpenAI's GPT models to provide comprehensive research on academic professionals and startup founders. The system works in two main stages:

1. **Verification:** First, the system verifies the identity of the person based on their name and affiliation, retrieving their current position, a brief description, and generating a confidence score.
2. **Research:** Once verification is complete, the system generates in-depth research about the individual, including:
    - Research focus areas or business domains
    - Notable publications, projects, or products
    - Institutional or industry connections
    - Funding history
    - Public mentions and recognition
    - Strategic insights for grants or investment opportunities

## Key Features
- Entity verification with confidence scoring
- Comprehensive research generation
- Support for both academic professionals and startup founders
- Rate limiting to prevent abuse
- Structured JSON responses
- Comprehensive error handling and logging

## Technology Stack
- Backend: Python, Flask
- AI: OpenAI GPT models with web search capability
- Utilities: Flask-Limiter, dotenv

## Installation and Setup
### Prerequisites
- Python 3.8 or higher
- OpenAI API key

### Installation Steps
1. Clone the repository
```
git clone https://github.com/venkapk/ai-research-assistant.git
cd ai-research-assistant/backend
```
2. Create and activate a virtual environment
```
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```
3. Install dependencies
```
pip install -r requirements.txt
```
4. Create a .env file in the backend directory with the following variables:
```
OPENAI_API_KEY=your_openai_api_key_here
FLASK_ENV=development
APP_NAME=AI-Research-Tool
LOG_LEVEL=INFO
```
5. Run the application
```
python app.py
```
The API will be available at http://localhost:5000

### Troubleshooting
- If facing issues with the Python interpreter, provide the absolute path to the virtual environment's Python executable:
```
# On Windows
C:\full\path\to\venv\Scripts\python.exe app.py

# On macOS/Linux
/full/path/to/venv/bin/python app.py
```
- If you encounter permission issues on Linux/macOS when activating the virtual environment, you may need to add execute permissions:
```
chmod +x venv/bin/activate
```
