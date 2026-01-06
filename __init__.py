"""
OSRS Sailing Materials Tracker
==============================

A comprehensive Streamlit application for tracking Old School RuneScape 
Sailing skill materials with real-time Grand Exchange prices.

Version: 4.7

Key Improvements in v4.7:
- Timing verification system (wiki-verified vs estimated data)
- API best practices (single /latest call, proper User-Agent)
- Optional osrs-prices package support
- New Sailing item IDs (helms, cannons, keel pieces)
- User transparency for estimated timing data

Modules:
- config: Application settings and constants
- data: Item IDs, costs, timings, locations
- models: Processing chain dataclasses and generators
- services: API clients, lookups, calculations
- ui: Styles, components, charts
- utils: Formatting and color utilities

Research References:
- API: prices.runescape.wiki (RuneLite partnership)
- Historical: api.weirdgloop.org/exchange/history/osrs
- Packages: osrs-prices, rswiki-wrapper, osrsreboxed
"""

__version__ = "4.7"
__author__ = "OSRS Sailing Tracker Team"
__api_version__ = "prices.runescape.wiki v1"
