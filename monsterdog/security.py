#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MONSTERDOG AEGIS SECURITY - Partie V
Module de sécurité et vérification d'intégrité
"""

import hashlib
import secrets
import time
from typing import Dict, Any


class AegisSecurity:
    """
    Système de sécurité AEGIS.
    Génère et vérifie des tokens SHA-512 pour la validation des sessions.
    """
    
    def __init__(self):
        self.tokens = {}
        self.session_start = time.time()
        
    def generate_token(self, data: str = None) -> str:
        """
        Génère un token SHA-512 unique.
        
        Args:
            data: Données optionnelles à inclure dans le hash
            
        Returns:
            Token SHA-512 en hexadécimal
        """
        if data is None:
            # Génère des données aléatoires sécurisées
            data = secrets.token_hex(32)
        
        # Ajoute un timestamp pour garantir l'unicité
        timestamp = str(time.time())
        combined = f"{data}{timestamp}{self.session_start}"
        
        # Génère le hash SHA-512
        token = hashlib.sha512(combined.encode('utf-8')).hexdigest()
        
        # Stocke le token avec son timestamp
        self.tokens[token] = {
            "created": time.time(),
            "data": data
        }
        
        return token
    
    def verify(self, token: str) -> bool:
        """
        Vérifie qu'un token existe et est valide.
        
        Args:
            token: Token à vérifier
            
        Returns:
            True si le token est valide, False sinon
        """
        return token in self.tokens
    
    def hash_file(self, filepath: str) -> str:
        """
        Génère un hash SHA-512 d'un fichier.
        
        Args:
            filepath: Chemin du fichier
            
        Returns:
            Hash SHA-512 en hexadécimal
        """
        sha512 = hashlib.sha512()
        
        try:
            with open(filepath, 'rb') as f:
                while chunk := f.read(8192):
                    sha512.update(chunk)
            return sha512.hexdigest()
        except Exception as e:
            return f"ERROR: {str(e)}"
    
    def get_session_info(self) -> Dict[str, Any]:
        """Retourne les informations de la session de sécurité."""
        return {
            "session_duration": time.time() - self.session_start,
            "tokens_issued": len(self.tokens),
            "status": "ACTIVE"
        }
