import fitz  # PyMuPDF
from PIL import Image
import io
import os

OFFSET = 2

def pdf_to_jpg(pdf_path, output_dir, max_size_kb=200):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    pdf_document = fitz.open(pdf_path)
    for page_num in range(len(pdf_document)):
        page_num_offset = page_num - OFFSET
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        
        img_data = pix.tobytes()
        image = Image.open(io.BytesIO(img_data))

        file_name = f"Quran{page_num_offset:04}.jpg"
        output_path = os.path.join(output_dir, file_name)
        
        # Save the image with quality adjustment to meet the file size requirement
        quality = 95  # Start with a high quality
        while True:
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG', quality=quality)
            file_size_kb = len(img_byte_arr.getvalue()) / 1024
            if file_size_kb <= max_size_kb or quality <= 10:
                break
            quality -= 5
        
        with open(output_path, 'wb') as img_file:
            img_file.write(img_byte_arr.getvalue())
    
    print("Conversion completed successfully.")

# Example usage
pdf_to_jpg('../standard1-quran-copy.pdf', '../quran_pages')