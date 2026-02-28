import uuid
from firebase_admin import storage

def upload_to_firebase(file_obj, folder="shoes"):
    """
    Upload một đối tượng file từ Django lên Firebase và trả về URL public.
    """
    bucket = storage.bucket()
    
    # Tạo tên file độc nhất để tránh ghi đè
    ext = file_obj.name.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    blob_path = f"{folder}/{filename}"
    
    blob = bucket.blob(blob_path)
    
    # Upload trực tiếp từ stream của InMemoryUploadedFile
    blob.upload_from_file(file_obj, content_type=file_obj.content_type)
    
    # Cho phép truy cập công khai
    blob.make_public()
    
    return blob.public_url, blob_path