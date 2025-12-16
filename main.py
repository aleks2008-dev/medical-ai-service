#!/usr/bin/env python3
"""
Medical AI Assistant.

Intelligent assistant for symptom analysis and doctor recommendations.
"""

from src.utils.cli import CLI
from src import __version__, __description__


def main():
    """Main application function."""
    print(f"🏥 {__description__}")
    print(f"📦 Version: {__version__}")
    print("=" * 50)
    
    cli = CLI()
    cli.run()


if __name__ == "__main__":
    main()