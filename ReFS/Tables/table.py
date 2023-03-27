from typing import Union
from Managers.Bytes import Formater
from Managers.Handlers import Config

class Table:
    def __init__(self, byteArray:Union[list[bytes], tuple[bytes], set[bytes]]) -> None:
        self.byteArray = byteArray
        self.formater = Formater()

    def tableID(self, val:str) -> str:
        tableIDNames = Config().get_file_contents("ReFS/Identifiers/Tables/tableIdentifiers.json")
        id = str(int(val, 16))
        return tableIDNames[id] if id in tableIDNames else "Other directory table"