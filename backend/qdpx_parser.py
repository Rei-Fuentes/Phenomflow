import zipfile
import xml.etree.ElementTree as ET
import os
from typing import List, Dict, Any, Optional
import tempfile
import shutil

class QDPXParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.project_data = {}
        self.codes = []
        self.code_groups = []

    def parse(self) -> Dict[str, Any]:
        """
        Main method to parse the QDPX file and extract relevant data.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                # Unzip the QDPX file
                with zipfile.ZipFile(self.file_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                
                # Find the .qde file (XML project data)
                qde_file = None
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        if file.endswith('.qde'):
                            qde_file = os.path.join(root, file)
                            break
                    if qde_file:
                        break
                
                if not qde_file:
                    raise FileNotFoundError("No .qde file found in the QDPX archive.")

                # Parse the XML
                self._parse_xml(qde_file)
                
                return {
                    "codes": self.codes,
                    "code_groups": self.code_groups,
                    "project_info": self.project_data
                }

            except Exception as e:
                raise ValueError(f"Error parsing QDPX file: {str(e)}")

    def _parse_xml(self, xml_file: str):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Namespace handling (QDA-XML often uses namespaces)
        # We'll try to handle it generically by stripping namespaces or using wildcard
        # For simplicity in this implementation, we'll traverse and look for tag names ending in 'Code'
        
        # Extract Project Info
        self.project_data = {
            "name": root.get("name"),
            "created": root.get("creationDateTime"),
            "modified": root.get("modifiedDateTime"),
            "creator": root.get("creatingUserGUID") # In a real app we'd resolve this to a name if available
        }

        # Extract Codes
        # The structure is usually <CodeBook><Codes><Code ... /></Codes></CodeBook>
        # We need to handle namespaces properly. The sample showed xmlns="urn:QDA-XML:project:1.0"
        ns = {'qda': 'urn:QDA-XML:project:1.0'}
        
        # Find CodeBook/Codes
        # Note: The sample XML showed <CodeBook><Codes><Code ...>
        # We will search for all 'Code' elements
        
        for code_elem in root.findall(".//qda:Code", ns):
            code_data = {
                "name": code_elem.get("name"),
                "guid": code_elem.get("guid"),
                "color": code_elem.get("color"),
                "is_codable": code_elem.get("isCodable") == "true",
                "comment": code_elem.get("comment", "")
            }
            self.codes.append(code_data)

        # If no codes found with namespace, try without (fallback)
        if not self.codes:
            for code_elem in root.findall(".//Code"):
                 code_data = {
                    "name": code_elem.get("name"),
                    "guid": code_elem.get("guid"),
                    "color": code_elem.get("color"),
                    "is_codable": code_elem.get("isCodable") == "true",
                    "comment": code_elem.get("comment", "")
                }
                 self.codes.append(code_data)

def extract_codes_from_qdpx(file_path: str) -> List[Dict[str, Any]]:
    """
    Helper function to quickly get just the codes.
    """
    parser = QDPXParser(file_path)
    data = parser.parse()
    return data["codes"]
