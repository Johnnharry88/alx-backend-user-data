#!/usr/bin/env python3
"""Module of BAsic Authentication for users"""
import base64
from .auth import Auth
from typing import TypeVar

from models.user import User


class BasicAuth(auth):
    """Implementation of Basic Authoirzation metod"""
    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """Works on the base64 part of the authorization header
        for a basic Authorization"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        paswd = authorization_header.split(" ")[-1]
        return None

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """ Decodes the base64- enocded string"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded = base64_authorizatin_header.encode('utf-8')
            alx = base64.b64decode(decoded)
            return alx.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> str:
        """ Returns user credential form base64-decoded val"""
        if decoded_base64_authorization_header is None:
            return(None, None)
        if not isinstance(decode_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header.split(':')[0]:
            return (None, None)
        email = decode_base64_authorization_header.split(':')[0]
        password = decoded_base64_authorization_header[len(email) + 1:]
        return (email, password)

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """Retrieves a user based on  ther user's authentiation"""
        if type(user_email) == str and type(user_pwd) == str:
            try:
                user = Users.search({'email': user_email})
            except Exception:
                return None
            x = len(user)
            if x <= 0:
                return None
            if user[0].is_valid_password(user_pwd):
                return user[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the user froma reuest"""
        auth_hd = self.authorization_header(request)
        b64_token = self.extract_base64_authorization_header(auth_hd)
        auth_tok = self.decode_base64_authorization_header(b64_token)
        emai, password = self.extract_user_credentials(auth_tok)
        return self.user_object_from_credentials(email, password)
