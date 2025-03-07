# Vehicle Servicing Center Search

A Flask-based web application that helps users find vehicle servicing centers.

## Features
- Search for vehicle servicing centers
- View service center details
- Integration with Google Maps API

## Setup Instructions

1. Clone the repository:
```bash
git clone <your-repository-url>
cd "Search Vehicle Servicing Center"
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory and add:
```
GOOGLE_MAPS_API_KEY=your_api_key_here
```

5. Run the application:
```bash
python app.py
```

## Environment Variables
- `GOOGLE_MAPS_API_KEY`: Your Google Maps API key for location services

## Deployment
This project is configured for deployment on Vercel with the following files:
- `vercel.json`: Vercel deployment configuration
- `build.sh`: Build script for deployment
- `runtime.txt`: Python runtime specification

## Security Note
Make sure to keep your API keys and sensitive information secure. Never commit the `.env` file to version control. 