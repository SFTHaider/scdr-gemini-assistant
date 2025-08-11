# scdr-gemini-assistant
SCDR Gemini Assistant is a natural-language interface for scdr-files-go, built to simplify NOAA SCDR satellite data access. Instead of memorizing command syntax, simply describe what you need in plain English — the assistant generates the correct command, validates it, and can execute it directly in your workflow.

Run the Python Helper Script

The scdr_gemini.py script converts plain English prompts into valid scdr-files-go commands.

Requirements
	•	Python 3.10 or newer
	•	(If using Gemini) an API key stored as GEMINI_API_KEY in a .env file or as an environment variable

Steps
	1.	Download this repository
	•	Clone via git:
git clone https://github.com//scdr-gemini-assistant.git
cd scdr-gemini-assistant
	•	Or click “Code” → “Download ZIP”, then unzip and open the folder.
	2.	(Optional) Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
python -m pip install -U pip
	3.	Install dependencies
If requirements.txt exists:
pip install -r requirements.txt
Otherwise, install manually:
pip install python-dotenv
plus any AI SDKs used (e.g., google-generativeai or openai)
	4.	Set your API key (if using Gemini)
	•	Create a .env file in the project folder:
GEMINI_API_KEY=your_key_here
	•	Or set it in your terminal:
export GEMINI_API_KEY=your_key_here
	5.	Run the script
python scdr_gemini.py “Give me the scdr-files command for extracting MTG FCI data for June 1 to June 10, 2024”
Example output:
scdr-files-go -t MTG-FCI-L1C –start-time “2024-06-01T00:00:00” –end-time “2024-06-10T23:59:59”
