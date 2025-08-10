# scdr-gemini-assistant
SCDR Gemini Assistant is a natural-language interface for scdr-files-go, built to simplify NOAA SCDR satellite data access. Instead of memorizing command syntax, simply describe what you need in plain English — the assistant generates the correct command, validates it, and can execute it directly in your workflow.

# SCDR Gemini Assistant Data Files
This repository contains reference `.txt` files used for natural-language to `scdr-files-go` command generation.

## Files
- `full_scdr_list.txt` — Complete list of SCDR datasets.
- `result.txt` — Example output from an SCDR query.
- `scdr_command_details.txt` — Command syntax and options extracted from `man scdr-files-go`.

## Instructions
1. **View a file**: Click on it in the file list.  
2. **Download a file**: Click the file name, then click **Download raw file**.  
3. **Use in code**:  
   ```python
   with open("full_scdr_list.txt") as f:
       datasets = [line.strip() for line in f]
