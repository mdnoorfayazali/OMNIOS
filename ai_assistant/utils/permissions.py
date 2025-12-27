import json
import os
from ai_assistant.utils.logger import setup_logger

logger = setup_logger(__name__)

class PermissionManager:
    """
    Manages user permissions for safe execution.
    Persists decisions to a file.
    """
    def __init__(self, storage_file="permissions.json"):
        self.storage_file = storage_file
        self.permissions = self._load_permissions()

    def _load_permissions(self):
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def _save_permissions(self):
        try:
            with open(self.storage_file, 'w') as f:
                json.dump(self.permissions, f, indent=4)
        except Exception as e:
            logger.error(f"Failed to save permissions: {e}")

    def check_permission(self, action: str, target: str) -> str:
        """
        Returns: 'ALLOWED', 'DENIED', or 'UNKNOWN'
        """
        key = f"{action}:{target}"
        return self.permissions.get(key, "UNKNOWN")

    def grant_permission(self, action: str, target: str):
        key = f"{action}:{target}"
        self.permissions[key] = "ALLOWED"
        self._save_permissions()

    def deny_permission(self, action: str, target: str):
        key = f"{action}:{target}"
        self.permissions[key] = "DENIED"
        self._save_permissions()

# Global instance
permission_manager = PermissionManager()
