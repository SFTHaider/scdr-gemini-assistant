import os
import re
from datetime import datetime, timezone
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv(os.path.expanduser("~/.env"))

# --- CONFIG ---
API_KEY = os.getenv("GEMINI_API_KEY")  # put your key in .env or export it
MODEL_NAME = "gemini-1.5-flash"

REFERENCE_FILES = [
    ("result.txt", "Machine-friendly CSV-like availability table"),
    ("scdr_command_details.txt", "Manual page for scdr-files-go CLI"),
    ("AVAIL.txt", "Human-readable availability table"),
    ("full_scdr_list.txt", "Complete dataset availability dump"),
]

SYSTEM_PROMPT = f"""
You are a command-line assistant that translates user requests into valid scdr-files-go commands for accessing NOAA's SCDR archive.

Command format:
scdr-files-go -t <type> [--satname <satellite>] --start-time "YYYY-MM-DDTHH:MM:SS" --end-time "YYYY-MM-DDTHH:MM:SS"

Rules:
• Use dataset type based on the product name (e.g., MTG-FCI-L1C, ABI-L1B-RADC, CRW_SSTA_MAX_YTD_5KM)
• Use --satname only if the dataset type has multiple satellites (e.g., GOES-16, GOES-18)
• Format times exactly as "YYYY-MM-DDTHH:MM:SS"
• Output only the scdr-files-go command, nothing else (no backticks, no prose)
• If the user input does not include an end time, assume a 1-hour window
• If the user says "last 7 days", calculate relative to today
• Assume UTC time unless otherwise stated
• If the request is to list all available data sets, use scdr-files-go --available
Current UTC time: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')}
"""

def load_reference_text():
    parts = []
    for fname, desc in REFERENCE_FILES:
        if os.path.exists(fname):
            with open(fname, "r", encoding="utf-8", errors="ignore") as f:
                parts.append(f"\n===== {desc} ({fname}) =====\n" + f.read())
    return "\n".join(parts)

def init_model():
    if not API_KEY:
        raise RuntimeError("Set GEMINI_API_KEY in your environment or .env file.")
    genai.configure(api_key=API_KEY)
    return genai.GenerativeModel(
        model_name=MODEL_NAME,
        system_instruction=SYSTEM_PROMPT,
        generation_config={
            "temperature": 0.1,
            "top_p": 0.9,
            "top_k": 32,
            "max_output_tokens": 256,
            "response_mime_type": "text/plain",
        },
    )

def postprocess_to_strict_command(text: str) -> str:
    # Strip code fences and grab the first line that starts with scdr-files-go
    t = text.strip()
    t = re.sub(r"^```[a-zA-Z]*\s*|\s*```$", "", t, flags=re.DOTALL).strip()
    # Find the command anywhere in the text
    m = re.search(r"(scdr-files-go\b[^\n\r]*)", t)
    if not m:
        raise ValueError(f"Model did not return a valid scdr command: {text!r}")
    cmd = re.sub(r"\s+", " ", m.group(1).strip())

    # Enforce MTG rule: use L1C and add --satname MTI1 if missing
    if "MTG-FCI" in cmd:
        cmd = cmd.replace("MTG-FCI-L1C", "MTG-FCI-L1C")  # no-op if already L1C
        cmd = cmd.replace("MTG-FCI", "MTG-FCI-L1C")      # upgrade if plain MTG-FCI
        if "--satname" not in cmd:
            cmd += " --satname MTI1"

    return cmd

def get_scdr_command(request: str) -> str:
    model = init_model()
    refs = load_reference_text()
    prompt = f"USER REQUEST:\n{request}\n\nREFERENCE MATERIALS (do not quote):\n{refs}"
    resp = model.generate_content(prompt)

    raw = resp.text if hasattr(resp, "text") else ""
    return postprocess_to_strict_command(raw)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print('Usage: python scdr_command_gen.py "your request here"')
        sys.exit(1)
    user_request = " ".join(sys.argv[1:])  # allow multiple args without extra quoting
    try:
        print(get_scdr_command(user_request))
    except Exception as e:
        print("Error:", e)