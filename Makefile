.PHONY: demo presentation help

# Default target
help:
	@echo "Available commands:"
	@echo "  make demo        - Run the Python Diffie-Hellman key exchange demo"
	@echo "  make presentation - Run the Slidev presentation"
	@echo "  make help        - Show this help message"

# Run the Python demo
demo:
	@python demo_runner.py

# Run the Slidev presentation
presentation:
	@slidev presentation/slides.md
