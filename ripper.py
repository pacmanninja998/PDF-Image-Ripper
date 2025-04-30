import os
import tkinter as tk
from tkinter import filedialog
import fitz  # PyMuPDF
from PIL import Image
import io

def extract_images_from_pdf(pdf_path):
    """Extract images from a PDF and save to a folder named after the PDF file"""
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_dir = os.path.join(os.path.dirname(pdf_path), base_name + "_images")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    try:
        with fitz.open(pdf_path) as pdf_file:
            for page_index in range(len(pdf_file)):
                page = pdf_file[page_index]
                image_list = page.get_images(full=True)
                
                if not image_list:
                    continue
                
                for image_index, img in enumerate(image_list, start=1):
                    xref = img[0]
                    base_image = pdf_file.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    
                    image = Image.open(io.BytesIO(image_bytes))
                    image.save(os.path.join(output_dir, 
                        f"page_{page_index+1}_img_{image_index}.{image_ext}"))
                    
        return output_dir
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return None

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Ask for PDF files
    pdf_files = filedialog.askopenfilenames(
        title="Select PDF files",
        filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
    )

    if not pdf_files:
        print("No files selected")
        return

    # Process all selected PDFs
    for pdf_path in pdf_files:
        output_dir = extract_images_from_pdf(pdf_path)
        if output_dir:
            print(f"Extracted images from {os.path.basename(pdf_path)} to:")
            print(output_dir)
            # Open the output folder in Explorer
            os.startfile(output_dir)

if __name__ == "__main__":
    main()
