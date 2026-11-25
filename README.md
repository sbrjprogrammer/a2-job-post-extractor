# Job Post Extractor

A command-line tool that extracts structured information from messy job posting text using Gemini and Pydantic.

## Features

- Extracts job title, company, location, salary, currency, skills, remote status, and experience
- Uses a Pydantic schema for structured validation
- Keeps the extraction prompt in a separate file
- Returns JSON output through the command line
- Includes validation retry handling

## Requirements

- Python
- uv
- Gemini API key

## Setup

Clone the repository:

```bash
git clone https://github.com/sbrjprogrammer/a2-job-post-extractor.git
cd a2-job-post-extractor
```

Install dependencies:

```bash
uv sync
```

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key
GEMINI_MODEL=your_model_name
```

## Usage

```bash
uv run extract.py "Hiring MERN Developer in Karachi. Skills: React, Node.js."
```

The program returns structured JSON.

## Project Structure

```text
.
├── extract.py
├── schema.py
├── prompts/
│   └── extract.txt
├── samples.md
├── README.md
└── pyproject.toml
```

## Samples

See `samples.md` for five sample inputs and their extracted outputs, including edge cases.

## Security

API keys are stored in `.env` and should never be committed to Git.