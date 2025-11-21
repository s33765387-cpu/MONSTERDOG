import json
import hashlib
import os
import datetime

VERSION = "vΩ.FINAL"

def hash_file(filepath):
    h = hashlib.sha512()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def generate():
    manifest = {
        "project": "MONSTERDOG FRAMEWORK",
        "version": VERSION,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "files": {}
    }

    # Scan des fichiers python
    for root, dirs, files in os.walk("."):
        # Ignore les répertoires cachés et __pycache__
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        
        for file in files:
            if file.endswith(".py") or file.endswith(".md") or file.endswith(".txt"):
                path = os.path.join(root, file)
                try:
                    manifest["files"][path] = hash_file(path)
                except Exception as e:
                    print(f"Erreur lors du hash de {path}: {e}")

    # Signature globale
    manifest_str = json.dumps(manifest, sort_keys=True)
    global_hash = hashlib.sha512(manifest_str.encode('utf-8')).hexdigest()
    manifest["signature_integrity"] = global_hash

    with open("MANIFEST_RELEASE.json", "w") as f:
        json.dump(manifest, f, indent=4)
    
    print(f"✅ MANIFESTE GÉNÉRÉ : MANIFEST_RELEASE.json")
    print(f"🔐 SIGNATURE GLOBALE : {global_hash[:64]}...")

if __name__ == "__main__":
    generate()
