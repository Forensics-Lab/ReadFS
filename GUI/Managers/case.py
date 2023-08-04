import shutil
from shutil   import rmtree
from datetime import datetime
from json     import dumps, loads
from os       import path, mkdir, listdir, rename, getcwd

class Case_Manager:
    def __init__(self, ):
        self._case_status = None
        self.date         = int(round(datetime.now().timestamp()))

    def _metadata_structure(self):
        return {"case_id": None, "author": None, "date_created": None, "date_modified": None}

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

    def delete(self, case_id):
        rmtree(path.join(self.root_folder(), case_id))
        self._case_status = "SUCCESS"

    def list(self):
        return listdir(self.root_folder())

    def open(self, name):
        ...

    def close(self, name):
        ...

    def export(self, dir_to_export, export_path):
        if export_path:
            export_name = f"{path.basename(dir_to_export)}_export"
            shutil.make_archive(export_name, "zip", dir_to_export)
            src = path.join(getcwd(), f"{export_name}.zip")
            dst = path.join(export_path, f"{export_name}.zip")
            rename(src, dst)
            self._case_status = "SUCCESS"
        else:
            self._case_status = "EXPORT_PATH_NOT_SPECIFIED"

    def import_(self, path):
        ...
