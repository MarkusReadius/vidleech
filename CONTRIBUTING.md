# Contributing to Vidleech

Thank you for your interest in contributing to Vidleech! This document provides guidelines and instructions for contributing.

## Development Setup

1. Fork and clone the repository:
```bash
git clone https://github.com/your-username/vidleech.git
cd vidleech
```

2. Install Poetry (if not already installed):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

3. Install dependencies:
```bash
poetry install
```

4. Run the application:
```bash
poetry run python src/main.py
```

## Code Style

We use several tools to maintain code quality:

- **Black**: For code formatting
- **isort**: For import sorting
- **flake8**: For code linting

Run formatters before committing:
```bash
poetry run black .
poetry run isort .
poetry run flake8
```

## Testing

Run tests with pytest:
```bash
poetry run pytest
```

## Commit Messages

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or modifying tests
- `chore:` Maintenance tasks

Examples:
```
feat: add support for new video platform
fix: resolve download progress calculation
docs: update installation instructions
```

## Pull Request Process

1. Create a new branch for your feature/fix:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and commit them following the commit message guidelines

3. Push to your fork and submit a pull request

4. Ensure your PR:
   - Passes all tests
   - Has proper commit messages
   - Updates documentation as needed
   - Includes a description of changes

## Code Review

- All submissions require review
- We may suggest changes or improvements
- The PR must pass all checks before merging

## Questions?

Feel free to open an issue for any questions or concerns.
