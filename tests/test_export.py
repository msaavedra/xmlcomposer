
import os
import tempfile
import unittest

import xmlcomposer
import xmlcomposer.export as export

class TestExport(unittest.TestCase):
    
    def test_export_to_file(self):
        original_contents = 'Original Document Text'
        new_contents = 'New Document Text'
        
        fileno, file_name = tempfile.mkstemp()
        backup_name = file_name + '.bak'
        
        try:
            with os.fdopen(fileno, 'wb') as f:
                f.write(original_contents)
            
            doc = xmlcomposer.PCData(new_contents)
            lines = doc.generate(layout=xmlcomposer.MINIMAL_LAYOUT)
            export.to_file(lines, file_name, backup_name)
            
            with open(file_name, 'r') as f:
                file_contents = f.read()
            
            with open(backup_name, 'r') as f:
                backup_contents = f.read()
            
            assert file_contents == new_contents
            assert backup_contents == original_contents
        finally:
            if os.path.exists(file_name):
                os.remove(file_name)
            if os.path.exists(backup_name):
                os.remove(backup_name)


