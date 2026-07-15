from services.pdf_service import PDFService

pdf = PDFService()

pdf.convert(
    "output/DOCX/CT0398_Anusha Punnapu.docx",
    "output/PDF/CT0398_Anusha Punnapu.pdf"
)

print("PDF Created Successfully")