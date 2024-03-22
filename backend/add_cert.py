def import_crt_to_cacert(crt_file_path, cacert_file_path):
    # Read the contents of the .crt file
    with open(crt_file_path, 'rb') as crt_file:
        crt_contents = crt_file.read()

    # Write the contents to a .pem file
    pem_file_path = 'certificate.pem'
    with open(pem_file_path, 'wb') as pem_file:
        pem_file.write(crt_contents)

    # Append the .pem file to cacert.pem
    with open(cacert_file_path, 'ab') as cacert_file:
        cacert_file.write(b'\n')  # Ensure a newline separator
        cacert_file.write(crt_contents)

# Example usage:
crt_file_path = r'/Users/jmiddleton/Documents/llama-index-python-webapp/backend/llamaindex.crt'
cacert_file_path = r'/Users/jmiddleton/Library/Caches/pypoetry/virtualenvs/app-iwm1hSXD-py3.11/lib/python3.11/site-packages/certifi/cacert.pem'
import_crt_to_cacert(crt_file_path, cacert_file_path)