from app.interfaces.pdf_interface import PDFInterface
from helpers.pdf_helper import (
    validate_pdf_file,
    extract_text_from_pdf,
    chunk_pdf_text,
    build_gemini_prompt,
    call_gemini_api,
    parse_gemini_response,
)
from logger import log_line


class PDFService(PDFInterface):
    def process_pdf(self, file) -> dict:
        """
        Process a PDF and extract Q&A pairs (without vectorization).
        These Q&As can later be sent for admin approval before vectorization.
        """
        pdf_bytes = validate_pdf_file(file)
        full_text = extract_text_from_pdf(pdf_bytes)
        chunks = chunk_pdf_text(full_text)

        if not chunks:
            raise Exception("No content extracted from PDF")

        qa_results = []

        print(f"Processing {len(chunks)} chunks from PDF...")
        print(" ")

        for chunk in chunks:
            try:
                print("processing chunk with heading:", chunk.get("heading"))
                prompt = build_gemini_prompt(chunk["text"])
                print(" ")

                print("prompt built, calling Gemini API...")
                status, raw_text, data = call_gemini_api(prompt)
                print(" ")

                print("Gemini API call complete, parsing response...")
                qa_list = parse_gemini_response(data, raw_text, chunk["text"])
                print(" ")

                print(f"Extracted {len(qa_list)} Q&A pairs")
                qa_results.extend(qa_list)

            except Exception as e:
                log_line({"error": str(e), "chunk_heading": chunk.get("heading")})
                continue

        final_output = {
            "total_chunks": len(chunks),
            "total_qa_generated": len(qa_results),
            "qa_results": qa_results   # <-- clean JSON without vectors
        }

        log_line({"message": "PDF processing complete", "summary": qa_results})
        return final_output
