import streamlit as st
import pypdf
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import io
import numpy as np

# ==================== TESSERACT PATH ====================
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\MURSA\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
# ========================================================

try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

st.set_page_config(page_title="PDF & Image to Text", page_icon="📄", layout="wide")

st.title("📄 PDF & Image to Text Extractor")
st.markdown("Upload any **PDF** or **Image** (JPG, PNG) and get the text instantly. Fully automatic — no settings needed!")

def check_tesseract():
    try:
        ver = pytesseract.get_tesseract_version()
        return True, str(ver)
    except Exception as e:
        return False, str(e)

def preprocess_for_ocr(image):
    """Enhance image for better OCR accuracy"""
    if image.mode != 'L':
        image = image.convert('L')
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.5)
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(2.0)
    image = image.filter(ImageFilter.MedianFilter(size=3))
    image = image.point(lambda x: 0 if x < 150 else 255, '1')
    return image.convert('L')

def extract_from_image(image):
    """Extract text from a single image using OCR"""
    proc = preprocess_for_ocr(image)
    text = pytesseract.image_to_string(proc, lang='eng', config='--psm 6')
    return text.strip()

def extract_standard_from_pdf(pdf_bytes):
    """Try standard text extraction from PDF"""
    try:
        reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
        text = ""
        for i, page in enumerate(reader.pages):
            txt = page.extract_text()
            if txt:
                text += f"\n--- Page {i+1} ---\n{txt}"
        return text.strip(), len(reader.pages)
    except Exception:
        return "", 0

def extract_ocr_from_pdf(pdf_bytes, dpi=300):
    """Extract text from scanned PDF using OCR"""
    if not PYMUPDF_AVAILABLE:
        return "", 0
    
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    total = len(doc)
    text = ""
    
    progress = st.progress(0)
    status = st.empty()
    
    for i in range(total):
        status.text(f"🔍 Reading page {i+1} of {total}...")
        progress.progress((i + 1) / total)
        
        page = doc.load_page(i)
        mat = fitz.Matrix(dpi/72, dpi/72)
        pix = page.get_pixmap(matrix=mat)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        page_text = extract_from_image(img)
        if page_text:
            text += f"\n--- Page {i+1} ---\n{page_text}"
    
    doc.close()
    progress.empty()
    status.empty()
    return text.strip(), total

def smart_extract_pdf(pdf_bytes):
    """Auto-detect: standard first, fallback to OCR"""
    text, pages = extract_standard_from_pdf(pdf_bytes)
    
    # If standard extraction got good text, use it
    if len(text) > 100 and len(text.split()) > 20:
        return text, pages, "Standard Text"
    
    # Otherwise use OCR
    st.info("📄 This looks like a scanned document. Running OCR...")
    text, pages = extract_ocr_from_pdf(pdf_bytes)
    return text, pages, "OCR (Scanned)"

# ============ DEPENDENCY CHECK ============
tess_ok, tess_ver = check_tesseract()
if not tess_ok:
    st.error("❌ Tesseract OCR not found! Please install it and update the path in the code.")
    st.stop()

if not PYMUPDF_AVAILABLE:
    st.error("❌ PyMuPDF not installed! Run: `pip install PyMuPDF`")
    st.stop()

st.success("✅ System Ready")

# ============ FILE UPLOAD ============
uploaded = st.file_uploader(
    "Upload your file",
    type=["pdf", "png", "jpg", "jpeg"],
    help="Supports PDF documents and images"
)

if uploaded:
    file_name = uploaded.name
    file_bytes = uploaded.getvalue()
    file_type = uploaded.type
    
    st.info(f"📁 **{file_name}** | {len(file_bytes)/1024:.1f} KB")
    
    # Show preview
    if file_type == "application/pdf":
        if PYMUPDF_AVAILABLE:
            try:
                doc = fitz.open(stream=file_bytes, filetype="pdf")
                st.caption(f"Total pages: {len(doc)}")
                
                # Show first page thumbnail
                page = doc.load_page(0)
                pix = page.get_pixmap(matrix=fitz.Matrix(0.5, 0.5))
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                st.image(img, caption="Preview", width=400)
                doc.close()
            except Exception:
                pass
    else:
        # It's an image
        image = Image.open(io.BytesIO(file_bytes))
        st.image(image, caption="Uploaded Image", width=400)
    
    # Extract Button
    if st.button("🔍 Extract Text", type="primary", use_container_width=True):
        with st.spinner("Processing... Please wait."):
            
            if file_type == "application/pdf":
                result_text, pages, method = smart_extract_pdf(file_bytes)
            else:
                # Image file
                image = Image.open(io.BytesIO(file_bytes))
                result_text = extract_from_image(image)
                pages = 1
                method = "OCR (Image)"
            
            # Display Results
            if not result_text:
                st.error("❌ Could not extract any text. The file may be blank, corrupted, or contain only images without text.")
            else:
                st.success(f"✅ Done! Method: **{method}** | Pages processed: **{pages}**")
                
                # Stats
                c1, c2, c3 = st.columns(3)
                c1.metric("Characters", len(result_text))
                c2.metric("Words", len(result_text.split()))
                c3.metric("Lines", result_text.count('\n') + 1)
                
                # Show text
                st.subheader("📋 Extracted Text")
                st.text_area("You can copy text from here:", value=result_text, height=400)
                
                # Download
                st.download_button(
                    label="💾 Download as .txt file",
                    data=result_text.encode('utf-8'),
                    file_name=f"{file_name.split('.')[0]}_extracted.txt",
                    mime="text/plain"
                )
else:
    st.markdown("---")
    st.markdown("""
    ### How it works:
    1. **Upload** any PDF or Image file using the box above
    2. **Click** the 'Extract Text' button
    3. **View** and **Download** the extracted text automatically
    
    The app automatically detects if your PDF is text-based or scanned, and handles both.
    """)