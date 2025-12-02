#!/usr/bin/env python3
"""
Medical AI Assistant.

Intelligent assistant for symptom analysis and doctor recommendations.
"""

from src.utils.cli import CLI


def main():
    """Main application function."""
    print("🏥 Medical AI Service")
    print("=" * 50)
    
    cli = CLI()
    cli.run()


if __name__ == "__main__":
    main()