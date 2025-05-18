# AI Research Assistant
AI-powered research assistant that helps gather deep, contextual information about specific academic professionals or startup founders for grant preparation, collaboration planning, and funding opportunities.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.3.3-green.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-1.79.0-412991.svg)
![React](https://img.shields.io/badge/react-18.2.0-61DAFB.svg)

## Project Description
The AI Research Assistant is a full-stack application that leverages OpenAI's GPT models to provide comprehensive research on academic professionals and startup founders. The system works in two main stages:

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
- Interactive, user-friendly React frontend
- Structured JSON responses
- Comprehensive error handling and logging
- Responsive design for mobile and desktop use

## How It Works

Below are screenshots demonstrating the key features and workflow of the AI Research Assistant using a dummy person:

### Search Interface
![Search Interface](/screenshots/Landing_Page.png)
*Users can search for academic professionals or startup founders by entering their name and affiliation.*

### Verification Results
![Verification Results](/screenshots/Verified_Page.png)
*The system verifies the identity and provides a confidence score along with basic information.*

### Detailed Research View
![Research View](/screenshots/Research_Page.png)
*Comprehensive research results are presented in an organized, easy-to-navigate format.*

## Project Structure
```
ai-research-assistant/
│
├── backend/                       # Backend logic
│   ├── routes/
│   │   └── api.py
│   ├── services/
│   │   ├── research_service.py
│   │   └── verify_service.py
│   ├── utils/
│   │   └── logger.py
│   ├── app.py                     # Main app entry point
│   ├── requirements.txt           # Python dependencies
│   └── .env                       # Backend environment variables
│
├── frontend/                      # Frontend React app
│   ├── public/
│   ├── src/                       # Application source code
│   │   ├── components/
│   │   │   ├── ErrorMessage.js
│   │   │   ├── Footer.js
│   │   │   ├── Header.js
│   │   │   ├── LoadingButton.js
│   │   │   └── icons/
│   │   │       └── index.js
│   │   ├── contexts/
│   │   │   └── AppContext.js
│   │   ├── pages/
│   │   │   ├── ResearchPage.js
│   │   │   └── VerifyPage.js
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.js                 # Main app component that sets up routes and layout
│   │   ├── App.css
│   │   ├── App.test.js
│   │   ├── index.js               # React app root entry point
│   │   ├── index.css
│   │   ├── logo.svg
│   │   ├── reportWebVitals.js
│   │   └── setupTests.js
│   ├── .env                       # Frontend environment variables
│   ├── package.json               # Project metadata and dependencies
│   ├── package-lock.json
│   ├── postcss.config.js          # Tailwind/PostCSS config
│   └── tailwind.config.js         # Tailwind utility class configuration
│
├── .gitignore                     # Files and directories to ignore in Git
├── LICENSE                        # MIT License (open-source usage rights)
└── README.md                      # This file
```

## Technology Stack

### Backend
<p align="left">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Flask-2.3.3-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" />
  <img src="https://img.shields.io/badge/OpenAI-1.79.0-412991?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI" />
  <img src="https://img.shields.io/badge/Gunicorn-21.2.0-499848?style=for-the-badge&logo=gunicorn&logoColor=white" alt="Gunicorn" />
</p>

### Frontend
<p align="left">
  <img src="https://img.shields.io/badge/React-18.2.0-61DAFB?style=for-the-badge&logo=react&logoColor=black" alt="React" />
  <img src="https://img.shields.io/badge/Tailwind_CSS-3.3.5-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind CSS" />
  <img src="https://img.shields.io/badge/React--Router-6.20.0-CA4245?style=for-the-badge&logo=react-router&logoColor=white" alt="React Router" />
  <img src="https://img.shields.io/badge/Axios-1.6.2-5A29E4?style=for-the-badge&logo=axios&logoColor=white" alt="Axios" />
</p>

## Installation and Setup
### Prerequisites
- Python 3.8 or higher
- OpenAI API key

### Backend Setup
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
LOG_LEVEL=INFO
APP_NAME=AI-Research-Tool
PORT=5000
```
5. Run the application
```
python app.py

# For production
gunicorn app:app
```
The API will be available at http://localhost:5000

### Frontend Setup
1. Navigate to the frontend directory
```
cd ../frontend
```
2. Install dependencies
```
npm install
```
3. Create a .env file in the frontend directory:
```
REACT_APP_API_URL=http://localhost:5000
```
4. Start the development server
```
npm start
```
The frontend application will be available at http://localhost:3000

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

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- OpenAI for providing the GPT API
- Open source libraries that made this project possible
