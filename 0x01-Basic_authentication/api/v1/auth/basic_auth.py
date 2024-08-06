#!/usr/bin/env python3
"""Module of BAsic Authentication for users"""
import base64
from .auth import Auth
from typing import TypeVar, Tuple
import re
import binascii

from models.user import User


class BasicAuth(Auth):
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
        patter = r'Basic (?P<token>.+)'
        match_x = re.fullmatch(patter, authorization_header.strip())
        if match_x is None:
            return None
        return match_x.group('token')

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """ Decodes the base64- enocded string"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            alx = base64.b64decode(
                base64_authorization_header.encode('utf-8'),
            )
            return alx.decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """ Returns user credential form base64-decoded val"""
        if decoded_base64_authorization_header is None:
            return(None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        email, password = decoded_base64_authorization_header.split(':')
        return (email, password)

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """Retrieves a user based on  ther user's authentiation"""
        if user_email is None or not isinstance (user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            user = Users.search({'email': user_email})
            if not user or user == []:
                return None
            for u in user:
                if u.is_valid_password(user_pwd):
                    return u
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the user froma reuest"""
        auth_hd = self.authorization_header(request)
        b64_token = self.extract_base64_authorization_header(auth_hd)
        auth_tok = self.decode_base64_authorization_header(b64_token)
        emai, password = self.extract_user_credentials(auth_tok)
        return self.user_object_from_credentials(email, password)
