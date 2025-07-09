import os
from flask import Blueprint, flash, request, render_template, redirect, send_file, current_app, url_for
from flask_login import current_user, login_required
from .ipfs import upload_to_ipfs,fetch_from_pinata
from .encryption import generate_key, encrypt_file, decrypt_file
from .models import db, UploadLog
from io import BytesIO

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        file = request.files.get("file")
        if not file:
            return "No file", 400

        key = generate_key()
        data = file.read()
        encrypted = encrypt_file(data, key)

        filename = f"enc_{file.filename}"
        save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        os.makedirs(current_app.config["UPLOAD_FOLDER"], exist_ok=True)

        with open(save_path, "wb") as f:
            f.write(encrypted)  

        # 2. upload that encrypted file to Pinata
        try:
            cid = upload_to_ipfs(save_path, current_app.config["PINATA_JWT"])
        except Exception as e:
            cid = None
            flash(f"Pinata upload failed: {e}", "error")

        if current_user.id is None:            # unexpected: not logged in?
            flash("Please log in again.", "danger")
            return redirect(url_for('auth.login'))

        log = UploadLog(filename=filename, enc_key=key, cid=cid, user_id=current_user.id)       
        db.session.add(log)
        db.session.commit()

        if os.path.exists(save_path):
            os.remove(save_path)
        return redirect("/")
    
    if current_user.role == 'admin':
        logs = UploadLog.query.all()
    else:
        logs = UploadLog.query.filter_by(user_id=current_user.id).all()
    return render_template("upload.html", logs=logs, current_user=current_user)

@main.route("/download/<int:log_id>")
@login_required
def download(log_id):
    log = UploadLog.query.get_or_404(log_id)
    try:
        cipher_blob = fetch_from_pinata(log.cid)
    except Exception as e:
        return f"IPFS fetch failed: {e}", 502


    try:
        decrypted = decrypt_file(cipher_blob, log.enc_key)
    except Exception as e:
        return f"Decryption failed: {e}", 400

    return send_file(BytesIO(decrypted), download_name="decrypted_" + log.filename[4:], as_attachment=True)
