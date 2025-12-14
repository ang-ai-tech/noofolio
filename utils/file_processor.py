"""
File processing utilities for CV and image uploads
"""
import pdfplumber
from docx import Document
from PIL import Image
from pathlib import Path
import io
import base64


class FileProcessor:
    """Process uploaded files (PDF, Word, Images)"""
    
    @staticmethod
    def extract_text_from_pdf(file_content: bytes) -> str:
        """Extract text from PDF file"""
        try:
            text_parts = []
            with pdfplumber.open(io.BytesIO(file_content)) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_parts.append(text)
            
            return "\n\n".join(text_parts)
        except Exception as e:
            raise Exception(f"Error extracting PDF: {str(e)}")
    
    @staticmethod
    def extract_text_from_docx(file_content: bytes) -> str:
        """Extract text from Word document"""
        try:
            doc = Document(io.BytesIO(file_content))
            text_parts = []
            
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text_parts.append(paragraph.text)
            
            return "\n\n".join(text_parts)
        except Exception as e:
            raise Exception(f"Error extracting Word doc: {str(e)}")
    
    @staticmethod
    def process_cv_file(file_content: bytes, filename: str) -> str:
        """Process CV file and extract text"""
        file_ext = Path(filename).suffix.lower()
        
        if file_ext == '.pdf':
            return FileProcessor.extract_text_from_pdf(file_content)
        elif file_ext in ['.doc', '.docx']:
            return FileProcessor.extract_text_from_docx(file_content)
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")
    
    @staticmethod
    def save_uploaded_file(file_content: bytes, filename: str, upload_dir: str = "data/uploads") -> str:
        """Save uploaded file and return path"""
        upload_path = Path(upload_dir)
        upload_path.mkdir(parents=True, exist_ok=True)
        
        # Generate unique filename
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{timestamp}_{filename}"
        
        file_path = upload_path / safe_filename
        
        with open(file_path, 'wb') as f:
            f.write(file_content)
        
        return str(file_path)
    
    @staticmethod
    def process_image(file_content: bytes, filename: str, max_size: tuple = (1200, 1200)) -> dict:
        """Process and optimize image"""
        try:
            # Open image
            img = Image.open(io.BytesIO(file_content))
            
            # Convert RGBA to RGB if necessary
            if img.mode == 'RGBA':
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3])
                img = background
            
            # Resize if too large
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Save to bytes
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=85, optimize=True)
            output.seek(0)
            
            # Convert to base64 for embedding
            img_base64 = base64.b64encode(output.read()).decode('utf-8')
            
            return {
                'filename': filename,
                'data': f'data:image/jpeg;base64,{img_base64}',
                'width': img.width,
                'height': img.height
            }
        except Exception as e:
            raise Exception(f"Error processing image {filename}: {str(e)}")
    
    @staticmethod
    def process_multiple_images(files: list, max_images: int = 10) -> list:
        """Process multiple image uploads"""
        processed_images = []
        
        for i, file in enumerate(files[:max_images]):
            try:
                img_data = FileProcessor.process_image(file['content'], file['filename'])
                processed_images.append(img_data)
            except Exception as e:
                print(f"Failed to process image {file['filename']}: {e}")
                continue
        
        return processed_images