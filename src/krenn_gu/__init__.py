"""Shared modules for the Krenn-Gu repository migration.

Currently contains only ``paths`` (shared repository path discovery).
Scripts that need these shared helpers insert ``src/`` into
``sys.path`` via the repository root; everything else stays
self-contained.
"""
