"""
Project: NishadRaj OS
Author: Jawahar R Mallah
Role: Software Architect
Organization: AITDL
Websites: https://aitdl.com | https://nishadraj.com
Governance Version: 1.1.0
This file is part of NishadRaj OS.
Licensed under AGPL-3.0 with Additional Governance Protection Terms.
Copyright © Jawahar R Mallah | AITDL

Module: Transparency API
Objective: Expose read-only governance and security status metrics.
"""

import json
import os

LOCK_FILE = "governance/governance.lock.json"
SCHEMA_FILE = "governance/ai-governance.schema.json"

class TransparencyAPI:
    def get_status(self):
        """Returns the high-level system status."""
        try:
            with open(LOCK_FILE, 'r') as f:
                lock = json.load(f)
            return {
                "system_status": lock.get("system_status", "UNKNOWN"),
                "governance_version": lock.get("_meta", {}).get("governance_version", "1.1.0"),
                "license_model": lock.get("license_model", "OPEN_SOURCE_CONTROLLED")
            }
        except:
            return {"error": "Unable to read lock file"}

    def get_governance_metrics(self):
        """Returns active schema hashes and enforcement flags."""
        try:
            with open(LOCK_FILE, 'r') as f:
                lock = json.load(f)
            return {
                "schema_hash": lock.get("governance_schema_hash"),
                "signature_enforced": lock.get("digital_signature_enforced"),
                "attribution_enforced": lock.get("author_attribution_enforced")
            }
        except:
            return {"error": "Unable to read governance data"}

if __name__ == "__main__":
    api = TransparencyAPI()
    print("Transparency API initialized (Mock Output):")
    print(json.dumps(api.get_status(), indent=4))
