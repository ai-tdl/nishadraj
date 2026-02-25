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
"""
import json
import hashlib
import os
from datetime import datetime

TASK_REGISTRY_PATH = "d:/IMP/GitHub/nishadraj/system/task_registry.json"

class TaskEngine:
    def __init__(self, registry_path=TASK_REGISTRY_PATH):
        self.registry_path = registry_path
        self.load_registry()

    def load_registry(self):
        with open(self.registry_path, 'r') as f:
            self.registry = json.load(f)

    def save_registry(self):
        self.registry['metadata']['last_updated'] = datetime.now().isoformat()
        self.registry['metadata']['registry_hash'] = self.compute_registry_hash()
        with open(self.registry_path, 'w') as f:
            json.dump(self.registry, f, indent=2)

    def compute_registry_hash(self):
        # Compute hash of the tasks list specifically for integrity
        tasks_str = json.dumps(self.registry['tasks'], sort_keys=True)
        return hashlib.sha256(tasks_str.encode()).hexdigest()

    def get_next_executable_task(self):
        for task in self.registry['tasks']:
            if task['status'] == 'PENDING':
                if self.verify_dependencies(task['id']):
                    return task
        return None

    def update_task_status(self, task_id, new_status):
        for task in self.registry['tasks']:
            if task['id'] == task_id:
                task['status'] = new_status
                task['updated_at'] = datetime.now().isoformat()
                self.save_registry()
                return True
        return False

    def verify_dependencies(self, task_id):
        target_task = next((t for t in self.registry['tasks'] if t['id'] == task_id), None)
        if not target_task:
            return False
        
        for dep_id in target_task.get('dependencies', []):
            dep_task = next((t for t in self.registry['tasks'] if t['id'] == dep_id), None)
            if not dep_task or dep_task['status'] != 'COMPLETED':
                return False
        return True

if __name__ == "__main__":
    engine = TaskEngine()
    print(f"Registry Hash: {engine.compute_registry_hash()}")
