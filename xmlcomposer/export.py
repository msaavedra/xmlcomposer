
import os
import shutil
import sys
import tempfile


if os.name == 'nt':
    import win32file as wf
    OPTIONS = wf.REPLACEFILE_WRITE_THROUGH|wf.REPLACEFILE_IGNORE_MERGE_ERRORS
    
    def _replace(old_path, new_path, backup_path=None):
        # ReplaceFile() apparently requires the backup file to already
        # exist, which is not very useful. Make the backup explicitly.
        if backup_path and os.path.exists(new_path):
            shutil.copy(old_path, backup_path)
        wf.ReplaceFile(old_path, new_path, None, OPTIONS)
else:
    def _replace(old_path, new_path, backup_path=None):
        if backup_path and os.path.exists(new_path):
            shutil.copy(new_path, backup_path)
        os.rename(old_path, new_path)


def to_file(lines, file_name, backup_name=None, perms=0622):
    """Safely and carefully write the generated output to a file.
    
    The lines arg should be an iterable containing lines in a file. Typically,
    it will be a generator object returned from the generate() method of
    TextBlock or its descendants.
    
    The filename arg is the path name where the output should be saved.
    
    The backup_name arg is a path where a copy of the old version of the file,
    if any, should be created. Any file currently at that path will be
    overwritten. This arg can be omitted and no backup will be made.
    
    The perms arg is the permissions of the newly written file. The value
    can be anything accepted by the standard os.chmod() function, and
    is platform-dependent.
    
    This method makes an effort to prevent data loss in the event
    of system failure. On POSIX-compliant systems, the new file will
    replace any previous version atomically, so this method can be used
    to write a file into a web server's data directory. Win32 systems
    are questionable though; some references claim that files can be
    replaced atomically, and some say that it is impossible using any
    well-supported Windows APIs.
    """
    base = os.path.split(os.path.abspath(file_name))[0]
    if not os.path.exists(base):
        os.makedirs(base)
    
    fileno, temp_name = tempfile.mkstemp(dir=base)
    with os.fdopen(fileno, 'wb') as f:
        f.writelines(lines)
        f.flush()
        os.fsync(fileno)
    
    _replace(temp_name, file_name, backup_name)
    os.chmod(file_name, perms)

def to_site(*args, **kwargs):
    """This is not implemented yet. When finished, it will upload to a remote
    host.
    """
    pass

