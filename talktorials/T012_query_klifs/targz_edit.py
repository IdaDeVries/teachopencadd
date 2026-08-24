# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.17.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import tarfile
import io

def modify_file_in_targz(targz_path, file_in_targz_path, line_modifications):
    """
    Modifies specified lines of a file inside a .tar.gz archive in memory.

    Args:
        targz_path (str): Path to the source .tar.gz file.
        file_in_targz_path (str): Path of the file to modify inside the archive.
        line_modifications (dict): A dictionary where keys are 1-based line numbers
                                   to modify and values are the new content for those lines.
    """
    in_memory_tar = io.BytesIO()

    try:
        with tarfile.open(targz_path, 'r:gz') as tar_in:
            with tarfile.open(fileobj=in_memory_tar, mode='w:gz') as tar_out:
                for member in tar_in.getmembers():
                    # Extract the file object for the current member
                    file_object = tar_in.extractfile(member)

                    if member.name == file_in_targz_path and file_object is not None:
                        # Read and decode the content
                        content = file_object.read().decode('utf-8')
                        lines = content.splitlines()

                        # Modify the specified lines (adjusting for 0-based index)
                        for line_num, new_content in line_modifications.items():
                            if 0 < line_num <= len(lines):
                                lines[line_num - 1] = new_content

                        # Join lines and encode back to bytes
                        modified_content = '\n'.join(lines).encode('utf-8')

                        # IMPORTANT: Update the size of the member info
                        member.size = len(modified_content)

                        # Create a new in-memory file with the modified content
                        modified_file_object = io.BytesIO(modified_content)

                        # Add the modified file to the new tar archive
                        tar_out.addfile(member, modified_file_object)
                    else:
                        # If it's not the file to modify, or if it's a directory,
                        # add it to the new tar archive as is.
                        tar_out.addfile(member, file_object)

        # Write the in-memory tarball back to the disk
        with open(targz_path, 'wb') as f:
            f.write(in_memory_tar.getvalue())

    except tarfile.ReadError:
        print(f"Error: Not a valid tar.gz file or file is corrupted: {targz_path}")
    except KeyError:
        print(f"Error: File not found in the archive: {file_in_targz_path}")

