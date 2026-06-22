"""
Deprecated since 0.7.0b1. Will be removed in 0.1.0
Use `functions` module instead, example:
from david8.functions import multi_if
"""
from .core.fn_generator import MultiIfFactory as _MultiIfFactory

multi_if = _MultiIfFactory()
