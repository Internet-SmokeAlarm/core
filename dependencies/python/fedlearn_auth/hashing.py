from passlib.hash import argon2
from .auth_constants import AuthConstants


def hash_secret(key):
    return argon2.using(rounds=AuthConstants.ROUNDS,
                        memory_cost=AuthConstants.MEMORY_COST).hash(key)


def verify_key(key, hash):
    return argon2.verify(key, hash)
