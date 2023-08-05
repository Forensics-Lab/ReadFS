import pyzipper
import zipfile
from shutil   import rmtree
from datetime import datetime
from json     import dumps, loads
from os       import path, mkdir, listdir, remove, walk


class Case_Manager:
    def __init__(self):
        self._case_status = None
        self.date         = int(round(datetime.now().timestamp()))

    def _metadata_structure(self):
        return {"case_id": None, "author": None, "date_created": None, "date_modified": None}

    def _sign_export_zip(self, path_to_zip):
        # The key in the future will change
        # This is just a POC
        with open(path_to_zip, 'ab') as zip_file:
            zip_file.write(b"abcdefghij")

    def _check_zip_sig(self, path_to_zip):
        # The key in the future will change
        # This is just a POC
        with open(path_to_zip, 'rb') as zip_file:
            zip_file.seek(-10, 2)
            return zip_file.read() == b"abcdefghij"

    def _zip_folder(self, folder_path, output_path, password):
        with pyzipper.AESZipFile(output_path, 'w', compression=zipfile.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zf:
            zf.setpassword(password.encode())  # Convert password to bytes

            for foldername, subfolders, filenames in walk(folder_path):
                for filename in filenames:
                    file_path = path.join(foldername, filename)
                    arcname = path.relpath(file_path, folder_path)  # Preserve folder structure in zip
                    zf.write(file_path, arcname)

    def _unzip_folder(self, zip_path, output_folder, password):
        with pyzipper.AESZipFile(zip_path, 'r') as zf:
            zf.setpassword(password.encode())  # Convert password to bytes
            zf.extractall(output_folder)

    def root_folder(self):
        return path.abspath("data/cases/")

    def create_file(self, path):
        with open(path, "w") as f:
            f.write("")

    def write_metadata(self, case_id, case_no, author, date_created, evidence_type, metadata_path):
        metadata_structure = self._metadata_structure()
        metadata_structure["case_id"]       = case_id
        metadata_structure["case_no"]       = case_no
        metadata_structure["author"]        = author
        metadata_structure["date_created"]  = date_created
        metadata_structure["date_modified"] = date_created
        metadata_structure["evidence_type"] = evidence_type
        with open(metadata_path, "w") as f:
            f.write(dumps(metadata_structure, indent=4))

    def create(self, case_no, author, evidence_path, evidence_type):
        # Check if the evidence path exists and is a file
        if not path.exists(evidence_path): self._case_status = "FILE_NOT_FOUND"; return
        if not path.isfile(evidence_path): self._case_status = "NOT_A_FILE";     return

        # Cleaning the case number and author name
        case_no = case_no.replace(" ", "_")
        author  = author.replace (" ", "_")

        # Create the case folder and metadata folder
        case_id         = f"{case_no}_{author}_{self.date}"
        case_folder     = path.join(self.root_folder(), case_id)
        metadata_folder = path.join(case_folder,     "metadata")
        metadata_file   = path.join(metadata_folder, "metadata.json")

        # Create the folders and files
        mkdir(case_folder)
        mkdir(metadata_folder)

        # This file will be used to store the metadata about the case (e.g. case number, author, etc.)
        self.create_file(metadata_file)
        self.write_metadata(case_id, case_no, author, self.date, evidence_type, metadata_file)

        # Update the case status
        self._case_status = "SUCCESS"

    def get_case_metadata(self, case_id):
        metadata_path = path.join(self.root_folder(), case_id, "metadata", "metadata.json")
        with open(metadata_path, "r") as f:
            return loads(f.read())

    def status(self):
        return self._case_status

    def reset_status(self):
        self._case_status = None

    def delete(self, case_id):
        rmtree(path.join(self.root_folder(), case_id))
        self._case_status = "SUCCESS"

    def list(self):
        return [dir_ for dir_ in listdir(self.root_folder()) if not "." in dir_]

    def open(self, name):
        ...

    def export(self, dir_to_export, export_path, export_password):
        if not export_path: self._case_status = "EMPTY_EXPORT_PATH"; return
        export_path = path.join(export_path, f"{path.basename(dir_to_export)}_export.zip")
        try:
            # Zip and sign the file
            self._zip_folder(dir_to_export, export_path, export_password)
            self._sign_export_zip(export_path)
            self._case_status = "SUCCESS"
        except FileNotFoundError:
            self._case_status = "INVALID_EXPORT_PATH"
        except RuntimeError:
            self._case_status = "PASSWORD_NOT_PROVIDED"

    def import_(self, path_to_zip, password):
        # Check if path is not empty
        if not path_to_zip: self._case_status = "EMPTY_IMPORT_PATH"; return
        try:
            # Check if zip file is a ReadFS export case
            if not self._check_zip_sig(path_to_zip): self._case_status = "BAD_IMPORT_FILE"; return
            output_folder = path.join(self.root_folder(), path.basename(path_to_zip)[:-11])
            self._unzip_folder(path_to_zip, output_folder, password)
            self._case_status = "SUCCESS"
        except FileNotFoundError:
            self._case_status = "IMPORT_FILE_NOT_FOUND"
        except RuntimeError:
            self._case_status = "INVALID_PASSWORD"
