import io
from flask import Flask, send_file
from fpdf import FPDF

# ... your existing app setup ...
app = Flask(__name__)
app.secret_key = "sih_secret_key"

@app.route("/test-pdf")
def test_pdf():
    # 1. Initialize fpdf2
    pdf = FPDF()
    pdf.add_page()
    
    # 2. Add Content / Styling
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 15, "MAHARASHTRA STATE INNOVATION SOCIETY", ln=True, align="C")
    
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "DEMO PILOT AGREEMENT & CERTIFICATE", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Helvetica", "", 12)
    pdf.multi_cell(0, 8, "This is a live preview generated on the fly using fpdf2 and Flask send_file. "
                        "No temporary files were saved to the disk!")
    pdf.ln(5)
    
    # Dummy data box
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 8, "Project: Smart Traffic Control System (Pune District)", ln=True)
    pdf.cell(0, 8, "Selected Startup: Nexus Innovations Pvt Ltd", ln=True)
    pdf.cell(0, 8, "Status: APPROVED FOR PILOT STAGE", ln=True)
    pdf.cell(0, 8, "Sanctioned Sandbox Budget: Rs. 2,50,000", ln=True)

    # 3. Stream to memory buffer
    pdf_bytes = pdf.output()
    pdf_buffer = io.BytesIO(pdf_bytes)
    pdf_buffer.seek(0)

    # 4. Stream inline to browser
    return send_file(
        pdf_buffer,
        mimetype="application/pdf",
        as_attachment=False,
        download_name="SIH_Test_Certificate.pdf"
    )

if __name__ == "__main__":
    app.run(debug=True)