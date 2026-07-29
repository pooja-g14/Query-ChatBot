# Setup Guidelines

This guide explains how to configure the Dynamic Schema Text-to-SQL ChatBot system.

## 1. Prerequisites

Make sure you have the following installed on your machine:
- **Python**: Version 3.9 or higher is recommended.
- **PostgreSQL**: A running PostgreSQL instance with database tables.

## 2. Environment Configuration

The application requires two environment variables to operate:

1. **`DATABASE_URL`**: The connection string for your PostgreSQL database.
   - Format: `postgresql://[user]:[password]@[host]:[port]/[database_name]`
2. **`GEMINI_API_KEY`**: Your Gemini API key from Google AI Studio.


## 3. Installation

1. Navigate to the project root directory.
2. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   # On Windows (PowerShell):
   .\venv\Scripts\Activate
   # On Linux/macOS:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install --no-cache-dir -r requirements.txt
   ```