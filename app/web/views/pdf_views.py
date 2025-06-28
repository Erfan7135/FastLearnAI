import os
import uuid
from flask import request, jsonify, Blueprint
from app.web.db.models.base import Pdf
from app.web.app import db

pdf_bp = Blueprint('pdf', __name__, url_prefix='/api/pdfs')

# We will add authentication to this later
@pdf_bp.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename.endswith('.pdf'):
        # Create a secure, unique filename
        filename = str(uuid.uuid4()) + ".pdf"
        
        # Create uploads directory if it doesn't exist
        if not os.path.exists('uploads'):
            os.makedirs('uploads')

        file_path = os.path.join('uploads', filename)
        file.save(file_path)

        # For now, we'll hardcode a user_id. We'll fix this with real auth later.
        hardcoded_user_id = "_NEEDS_REAL_USER_ID_"

        new_pdf = Pdf(name=file.filename, user_id=hardcoded_user_id, file_path=file_path)
        db.session.add(new_pdf)
        db.session.commit()

        # TODO: Dispatch Celery task to process this PDF
        # process_document.delay(new_pdf.id)

        return jsonify({'message': 'File uploaded successfully', 'pdf_id': new_pdf.id}), 201
    else:
        return jsonify({'error': 'Invalid file type, only PDF allowed'}), 400