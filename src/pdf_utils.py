import os
import multiprocessing
from unstructured.partition.pdf import partition_pdf


def extract_text_from_pdf(pdf_path):
    try:
        elements = partition_pdf(filename=pdf_path)
        return "\n".join([str(element) for element in elements])
    except Exception as e:
        return f"Error extracting {pdf_path}: {str(e)}"


def pdf_file_paths(pdf_directory):
    return [
        os.path.join(pdf_directory, f)
        for f in os.listdir(pdf_directory)
        if f.endswith(".pdf")
    ]


def process_pdfs(pdf_directory):
    pdf_files = pdf_file_paths(pdf_directory)
    with multiprocessing.Pool(processes=min(4, os.cpu_count())) as pool:
        texts = pool.map(extract_text_from_pdf, pdf_files)
    return texts
