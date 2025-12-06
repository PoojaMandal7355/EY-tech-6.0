"""File handling utilities"""
import os
import shutil
from pathlib import Path
from fastapi import UploadFile
from app.core.config import settings


class FileHandler:
    """Utility class for file operations"""
    
    @staticmethod
    def ensure_upload_dir():
        """Ensure upload directory exists"""
        upload_dir = Path(settings.upload_dir)
        upload_dir.mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    async def save_upload_file(file: UploadFile, subdirectory: str = "") -> tuple[str, int]:
        """
        Save an uploaded file to disk.
        
        Args:
            file: Uploaded file
            subdirectory: Subdirectory within uploads folder
            
        Returns:
            Tuple of (file_path, file_size)
            
        Raises:
            ValueError: If file size exceeds max limit
        """
        FileHandler.ensure_upload_dir()
        
        # Check file size
        contents = await file.read()
        file_size = len(contents)
        
        if file_size > settings.max_upload_size:
            raise ValueError(
                f"File size {file_size} exceeds maximum {settings.max_upload_size}"
            )
        
        # Create subdirectory if needed
        if subdirectory:
            file_dir = Path(settings.upload_dir) / subdirectory
            file_dir.mkdir(parents=True, exist_ok=True)
        else:
            file_dir = Path(settings.upload_dir)
        
        # Save file
        file_path = file_dir / file.filename
        
        with open(file_path, "wb") as f:
            f.write(contents)
        
        # Return relative path and size
        relative_path = str(file_path.relative_to(Path.cwd()))
        return relative_path, file_size
    
    @staticmethod
    def delete_file(file_path: str) -> None:
        """
        Delete a file.
        
        Args:
            file_path: Path to file
            
        Raises:
            FileNotFoundError: If file not found
        """
        path = Path(file_path)
        if path.exists():
            path.unlink()
        else:
            raise FileNotFoundError(f"File {file_path} not found")
    
    @staticmethod
    def get_file_type(filename: str) -> str:
        """
        Get file type from filename.
        
        Args:
            filename: File name
            
        Returns:
            File type/extension
        """
        return Path(filename).suffix.lstrip(".")
