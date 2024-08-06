#!/usr/bin/env python3
"""Module that holds Class describing Authontication"""
from flask import request
from typing import List, TypeVar
import fnmatch


class Auth:
    """Checks out API Authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks out whether a given API path requires authentication ot not
        """
        if path is None:
            return True
        elif excluded_paths is None or not excluded_paths:
            return True
        else:
            for y in excluded_paths:
                if fnmatch.fnmatch(path, y):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """Returns the authorization header from request object"""
        if request is None:
            return None
        hd = request.headers.get('Authorization')
        if hd is None:
            return None
        return hd

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns a User instance using info form request"""
        return None
