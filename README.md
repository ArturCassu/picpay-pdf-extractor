# FastAPI PDF Extractor

This project is a FastAPI application that extracts transaction data from PDF files and saves it to an Excel file. It utilizes the `pdfplumber` library for PDF extraction and `pandas` for data manipulation and saving to Excel.

## Project Structure

```
fastapi-pdf-extractor
├── app
│   ├── main.py               # Entry point of the FastAPI application
│   ├── api
│   │   └── routes.py         # API routes for uploading PDF and extracting data
│   ├── services
│       └── extractor.py       # Logic for extracting data from PDF files
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

## Installation

1. Clone the repository:

   ```
   git clone <repository-url>
   cd fastapi-pdf-extractor
   ```

2. Create a virtual environment (optional but recommended):

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

## Usage

1. Start the FastAPI application:

   ```
   uvicorn app.main:app --reload
   ```

2. Use the `/upload` endpoint to upload a PDF file and trigger the extraction process.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.