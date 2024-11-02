#!/usr/bin/env python3
import secrets

# Generate a secure random URL-safe token for JWT
secret_key = secrets.token_urlsafe(32)
print(secret_key)

