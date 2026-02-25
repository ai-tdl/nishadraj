"""
Project: NishadRaj OS
Author: Jawahar R Mallah
Organization: AITDL
License: AGPL-3.0 + Governance Protection Terms
Copyright © Jawahar R Mallah | AITDL
"""

import sys
import os

# Ensure root is in path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from system.validator_agent import preflight_check

def enforce_governance(task_id: str):
    """
    Enforces governance by running a preflight check using the system validator.
    """
    return preflight_check(task_id)
