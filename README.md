# scdr-gemini-assistant

The SCDR Gemini Assistant is a Python-based tool that converts plain English instructions into valid scdr-files-go commands. It has been created to generate commands that can help communicate with scdr data base at NOAA

Simply tell the assistant what data you want, and it will output the exact scdr-files-go command you need. You can then copy that command into your terminal or integrate it directly into your workflow.

⸻

# Included Files

Main Script
	•	scdr_gemini.py — Processes natural language prompts and generates commands.

Reference Data Files (kept in the repository root):
	•	full_scdr_list.txt — Complete list of SCDR datasets.
	•	AVAIL.txt — Example output from scdr-files-go --available.
	•	result.txt — Example output from an SCDR query.
	•	scdr_command_details.txt — Syntax and options from man scdr-files-go.

⸻

Requirements
	•	Python 3.10+
	•	Internet connection (if using Gemini API)
	•	(Optional) Gemini API key stored as GEMINI_API_KEY in a .env file

⸻
Setup
	#1.	Download the repository
 
 git clone https://github.com/<your-username>/scdr-gemini-assistant.git
 cd scdr-gemini-assistant
 
Or download the ZIP from GitHub and unzip it.

⸻

2. (Optional) Create a virtual environment

python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

⸻

 # 3.	Install dependencies
 pip install -r requirements.txt

⸻

5.	(Optional) Set your Gemini API key
	•	Create a .env file in the same folder as scdr_gemini.py:
GEMINI_API_KEY=your_key_here

•	Or set it in your terminal:
export GEMINI_API_KEY=your_key_here

⸻

# How to Run:

Example 1 — Get MTG FCI data for a date range

INPUT: python scdr_gemini.py "Give me the scdr-files command for extracting MTG FCI data for June 1 to June 10, 2024"
OUTPUT: scdr-files-go -t MTG-FCI-L1C --start-time "2024-06-01T00:00:00" --end-time "2024-06-10T23:59:59"

⸻

# Troubleshooting
	•	FileNotFoundError → Ensure all .txt files are in the same folder as scdr_gemini.py.
	•	ModuleNotFoundError: dotenv → Run pip install python-dotenv.
	•	API key not found → Make sure .env exists and contains GEMINI_API_KEY=your_key_here.

⸻

License

This project is licensed under the MIT License — see the LICENSE file for details.

