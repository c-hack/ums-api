"""
Module for loading the profile adapter
"""

import importlib.util
from .profile_adapter_skel import ProfileAdapter


def load_profile_adapter(path_to_adapter: str) -> ProfileAdapter:
    """
    Load the profile adapter
    """

    try:
        spec = importlib.util.spec_from_file_location("ums_api.profile_adapter.loaded", path_to_adapter)
        profile_adapter = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(profile_adapter)
        return profile_adapter.ProfileAdapter()
    except Exception as err:
        raise ValueError("Could not load the profile adpater") from err
