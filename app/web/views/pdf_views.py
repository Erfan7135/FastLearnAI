import os
import shutil
from flask import request, jsonify, Blueprint, session, g, current_app
from app.web.db.models.base import Pdf
from app.web.app import db
from app.web.hooks import login_required, handle_file_upload

pdf_bp = Blueprint('pdf', __name__, url_prefix='/api/pdfs')

@pdf_bp.route('/', methods=['GET'])
@login_required
def list_pdfs():
    pdfs= Pdf.query.filter_by(user_id=g.user.id).all()
    if not pdfs:
        return jsonify([])
    return jsonify([pdf.as_dict() for pdf in pdfs])


# We will add authentication to this later
@pdf_bp.route('/', methods=['POST'])
@login_required
@handle_file_upload
def upload_file(file_id, file_path, file_name):
    upload_dir = current_app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # Move the file to the upload directory
    permanent_file_path = os.path.join(upload_dir, file_id + '.pdf')

    shutil.move(file_path, permanent_file_path)

    # Create a new Pdf object
    pdf =Pdf.create(id=file_id, name=file_name, user_id=g.user.id, 
                    file_path=permanent_file_path)
    
    # TODO Dispatch Celery task to process the PDF
    # process_pdf.delay(pdf.id)

    return jsonify({'message': 'File uploaded successfully', 'pdf': pdf.as_dict()}), 201

@pdf_bp.route("/<string:pdf_id>", methods=["GET"])
@login_required
# @load_model(Pdf) # We will implement load_model in hooks later if needed
def show(pdf_id):
    pdf = Pdf.find_by(id=pdf_id, user_id=g.user.id)
    if not pdf:
        return jsonify({'error': 'PDF not found'}), 404
    return jsonify(
        {
            "pdf": pdf.as_dict(),
            # "download_url": files.create_download_url(pdf.id), # No longer needed
        }
    )