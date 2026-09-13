from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
import database as db
from fpdf import FPDF
import io
import qrcode
from PIL import Image
import secrets

app = Flask(__name__)
app.secret_key = "sih_maharashtra_tech_lead_secret_key"

# Ensure database is initialized at startup
db.init_db()

@app.route("/")
def home():
    if "username" in session:
        return (f"<h1>Hello guys this is our home page</h1>"
                f"<h3>Currently logged in as {session['username']}</h3>")
    return "<h1>Hello Guys this is our home page.</h1>"


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")

        success = db.register_user(username, password, role)

        if success:
            flash("Account created! Please log in.", "success")
            return redirect(url_for("login"))
        else:
            flash("Username already exists!", "danger")
            return render_template("registerform.html")

    return render_template("registerform.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        stored_pass = db.verify_user(username)

        if stored_pass and stored_pass == password:
            user_profile = db.get_user_profile(username)

            session["username"] = user_profile["username"]
            session["role"] = user_profile["role"]
            session.permanent = True

            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials!", "danger")
            return render_template("login.html")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
        
    conn = db.get_db_connection()
    user_role = session.get('role', 'Startup')
    
    # Check for Evaluator / Admin roles
    if user_role in ["Expert Evaluator", "Government Evaluator"]:
        # Evaluators view all submissions across startups
        milestones = conn.execute("SELECT * FROM milestones").fetchall()
        conn.close()
        return render_template("evaluator_dashboard.html", milestones=milestones)
    else:
        # Startups view only their own submissions
        user_milestones = db.get_user_milestones(session["username"])
        conn.close()
        return render_template(
            "dashboard.html", 
            username=session["username"], 
            role=session["role"],
            milestones=user_milestones
        )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/admin/users")
def admin_users():
    if "username" not in session:
        flash("Please log in first.", "danger")
        return redirect(url_for("login"))

    users_list = db.get_all_users()
    return render_template("admin_users.html", users=users_list)


@app.route("/certificate/<int:project_id>")
def view_certificate(project_id):
    if "username" not in session:
        return redirect(url_for("login"))

    milestone = db.get_milestone_by_id(project_id)
    
    # Allow certificates for status 'Approved' or 'Completed'
    if not milestone or milestone["status"] not in ["Completed", "Approved"]:
        flash("Certificate not available yet.", "warning")
        return redirect(url_for("dashboard"))

    username = milestone["username"]
    milestone_title = milestone["title"]

    # Generate or retrieve signature
    cert_sig = milestone["certificate_signature"] if milestone["certificate_signature"] else f"TEMP-SIG-{project_id}"

    # 1. Build Verification URL for QR Code
    BASE_URL = "https://crudeness-stable-referee.ngrok-free.dev"
    verification_url = f"{BASE_URL}/startup/{username}"

    # 2. Generate QR Code in Memory (BytesIO)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1,
    )
    qr.add_data(verification_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    qr_buffer = io.BytesIO()
    qr_img.save(qr_buffer, format="PNG")
    qr_buffer.seek(0)

    # 3. Create PDF with FPDF2
    pdf = FPDF()
    pdf.add_page()

    # Document Header
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 15, "MAHARASHTRA STATE INNOVATION SOCIETY", ln=True, align="C")
    
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 10, "OFFICIAL PILOT COMPLETION CERTIFICATE", ln=True, align="C")
    pdf.ln(8)
    
    # Divider Line
    pdf.set_line_width(0.5)
    pdf.line(10, 45, 200, 45)
    pdf.ln(10)
    
    # Certificate Body
    pdf.set_font("Helvetica", "", 12)
    pdf.multi_cell(
        0, 8, 
        f"This is to certify that '{username.upper()}' has successfully completed and verified "
        f"the required deliverables for the project work scope under the Maharashtra State Sandbox Framework."
    )
    pdf.ln(8)
    
    # Project Details
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 8, f"Certificate Ref ID: MSIS-PILOT-{project_id:04d}", ln=True)
    pdf.cell(0, 8, f"Digital Signature: {cert_sig}", ln=True)
    pdf.cell(0, 8, f"Milestone Scope: {milestone_title}", ln=True)
    pdf.cell(0, 8, f"Status: VERIFIED & APPROVED", ln=True)
    pdf.cell(0, 8, f"Recipient Account: {username}", ln=True)
    
    pdf.ln(15)
    # Footer Signoff
    pdf.set_font("Helvetica", "I", 10)
    pdf.cell(0, 6, "Digitally generated via SIH Government Procurement Portal", ln=True, align="R")
    pdf.cell(0, 6, "No physical signature required.", ln=True, align="R")

    # Embed QR Code directly from memory buffer
    pdf.image(qr_buffer, x=160, y=210, w=35, h=35, type="PNG")

    # QR Code Caption
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_xy(160, 246)
    pdf.cell(35, 5, "Scan to Verify", align="C")

    # 4. Stream PDF directly back to browser
    pdf_bytes = pdf.output()
    pdf_buffer = io.BytesIO(pdf_bytes)
    pdf_buffer.seek(0)

    return send_file(
        pdf_buffer,
        mimetype="application/pdf",
        as_attachment=False,
        download_name=f"Certificate_Project_{project_id}.pdf"
    )


@app.route("/startup/<string:startup_username>")
def public_startup_profile(startup_username):
    conn = db.get_db_connection()
    
    milestones = conn.execute(
        "SELECT * FROM milestones WHERE username = ?", 
        (startup_username,)
    ).fetchall()
    
    conn.close()

    if not milestones:
        flash("Startup profile not found.", "warning")
        return redirect(url_for("login"))

    return render_template(
        "public_profile.html", 
        startup_name=startup_username, 
        milestones=milestones
    )


@app.route("/update_status/<int:milestone_id>/<string:new_status>", methods=["POST"])
def update_status(milestone_id, new_status):
    if session.get("role") not in ["Expert Evaluator", "Government Evaluator"]:
        flash("Unauthorized access.", "danger")
        return redirect(url_for("dashboard"))

    conn = db.get_db_connection()
    
    if new_status in ["Approved", "Completed"]:
        sig = f"GOVT-VERIFIED-{secrets.token_hex(4).upper()}"
        conn.execute(
            "UPDATE milestones SET status = 'Approved', certificate_signature = ? WHERE id = ?",
            (sig, milestone_id)
        )
    else:
        conn.execute(
            "UPDATE milestones SET status = ? WHERE id = ?",
            (new_status, milestone_id)
        )
        
    conn.commit()
    conn.close()
    
    flash(f"Milestone updated to {new_status}!", "success")
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    with app.app_context():
        db.init_db()
        if hasattr(db, 'seed_default_accounts'):
            db.seed_default_accounts()
    app.run("0.0.0.0", port=5000, debug=True)