"""
Project: NishadRaj OS
Author: Jawahar R Mallah
Organization: AITDL
License: AGPL-3.0 + Governance Protection Terms
Copyright © Jawahar R Mallah | AITDL
"""

import json
import hashlib
import os
from jsonschema import Draft7Validator
from jsonschema.exceptions import ValidationError

# Correct path for local imports if needed, but here we assume security is a package or in PYTHONPATH
try:
    from security.signature_manager import verify_all_governance_files
except ImportError:
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from system.signature_manager import verify_all_governance_files

SCHEMA_PATH = "governance/ai-governance.schema.json"
LOCK_PATH = "governance/governance.lock.json"

def compute_sha256(filepath: str) -> str:
    with open(filepath, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest().upper()

def validate_schema_structure():
    if not os.path.exists(SCHEMA_PATH):
        raise FileNotFoundError(f"Schema file missing: {SCHEMA_PATH}")
        
    with open(SCHEMA_PATH) as f:
        schema = json.load(f)

    # Deterministic Draft 7 structural verification
    try:
        Draft7Validator.check_schema(schema)
    except ValidationError as e:
        raise Exception(f"Schema structural validation failed: {e.message}")

    return True


def validate_schema_hash():
    if not os.path.exists(LOCK_PATH):
        raise FileNotFoundError(f"Lock file missing: {LOCK_PATH}")

    with open(LOCK_PATH) as f:
        lock_data = json.load(f)

    expected_hash = lock_data.get("governance_schema_hash")
    actual_hash = compute_sha256(SCHEMA_PATH)

    if expected_hash != actual_hash:
        raise Exception(f"Governance schema hash mismatch detected.\nExpected: {expected_hash}\nActual:   {actual_hash}")

    return True

def validate_signature_integrity():
    # Calling the verified existence in signature_manager
    if not verify_all_governance_files():
        raise Exception("Digital signature verification failed for one or more governance files.")
    return True

def full_check():
    validate_schema_structure()
    validate_schema_hash()
    validate_signature_integrity()
    return True

if __name__ == "__main__":
    try:
        full_check()
        print("Governance validation PASSED (Deterministic Mode).")
    except Exception as e:
        print(f"Governance validation FAILED: {e}")
        import sys
        sys.exit(1)
