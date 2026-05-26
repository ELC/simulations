"""Shared analysis core for free-market simulations.

Holds aggregation, bootstrap CI, KDE, distribution fitting, mobility metrics
and Altair builders. Only the modules under :mod:`analysis.adapters` import
``scipy``/``statsmodels`` directly; everything else consumes typed wrappers.
"""
