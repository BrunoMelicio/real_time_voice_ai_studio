# CLAUDE.md - AI Assistant Guidelines

This document provides context and guidelines for AI assistants working with this repository.

## Project Overview

**Repository**: claude_code_test
**Status**: New/Initializing
**Last Updated**: 2026-02-01

<!-- TODO: Add project description when codebase is populated -->
This repository is currently being initialized. Update this section with:
- Project purpose and goals
- Target users/audience
- Key features

## Codebase Structure

<!-- TODO: Update when project structure is established -->
```
claude_code_test/
├── CLAUDE.md          # AI assistant guidelines (this file)
└── .git/              # Git repository
```

### Directory Conventions

When the project is populated, document directories here:

| Directory | Purpose |
|-----------|---------|
| `src/`    | Source code |
| `tests/`  | Test files |
| `docs/`   | Documentation |
| `scripts/`| Build/utility scripts |

## Development Workflow

### Getting Started

```bash
# Clone the repository
git clone <repository-url>
cd claude_code_test

# Install dependencies (update based on project type)
# npm install    # for Node.js
# pip install -r requirements.txt  # for Python
# cargo build    # for Rust
```

### Common Commands

<!-- TODO: Add actual commands when project is configured -->
```bash
# Build
# npm run build

# Test
# npm test

# Lint
# npm run lint

# Format
# npm run format
```

### Branch Strategy

- `main` / `master`: Production-ready code
- `develop`: Integration branch for features
- `feature/*`: New features
- `fix/*`: Bug fixes
- `claude/*`: AI-assisted development branches

## Code Conventions

### General Principles

1. **Clarity over cleverness**: Write readable, maintainable code
2. **Consistency**: Follow existing patterns in the codebase
3. **Minimal changes**: Make focused changes that address the specific task
4. **No over-engineering**: Avoid adding unnecessary abstractions or features

### Style Guidelines

<!-- TODO: Add language-specific conventions -->
- Follow the project's linting configuration
- Use meaningful variable and function names
- Keep functions small and focused
- Add comments only where logic isn't self-evident

### Commit Messages

Use clear, descriptive commit messages:
```
<type>: <short description>

[optional body with more details]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `test`: Adding/updating tests
- `chore`: Maintenance tasks

## Testing Requirements

<!-- TODO: Update with actual testing requirements -->
- Write tests for new features
- Ensure existing tests pass before committing
- Aim for meaningful test coverage

## AI Assistant Guidelines

### Before Making Changes

1. **Read first**: Always read relevant files before modifying them
2. **Understand context**: Explore related code to understand patterns
3. **Check existing patterns**: Follow conventions already in the codebase
4. **Verify requirements**: Ensure you understand what's being asked

### When Making Changes

1. **Minimal scope**: Only change what's necessary for the task
2. **Preserve style**: Match the existing code style
3. **Avoid side effects**: Don't introduce unrelated changes
4. **Security awareness**: Never introduce vulnerabilities (injection, XSS, etc.)
5. **No unnecessary features**: Don't add features that weren't requested

### After Making Changes

1. **Verify builds**: Ensure the project still builds
2. **Run tests**: Check that all tests pass
3. **Review changes**: Double-check your modifications
4. **Clear commits**: Write descriptive commit messages

### Things to Avoid

- Adding features beyond what's requested
- Creating unnecessary abstractions
- Adding excessive comments or documentation
- Modifying code unrelated to the task
- Introducing breaking changes without discussion
- Committing sensitive data (credentials, API keys)

## Key Files

<!-- TODO: Document important files as they are created -->
| File | Purpose |
|------|---------|
| `CLAUDE.md` | AI assistant guidelines |
| `README.md` | Project documentation |
| `package.json` | Node.js dependencies and scripts |
| `.env.example` | Environment variable template |

## Dependencies

<!-- TODO: Document key dependencies -->
### Production Dependencies

- TBD

### Development Dependencies

- TBD

## Configuration

### Environment Variables

<!-- TODO: Document required environment variables -->
| Variable | Description | Required |
|----------|-------------|----------|
| `NODE_ENV` | Environment (development/production) | No |

### Build Configuration

<!-- TODO: Document build configuration -->
- TBD

## Troubleshooting

### Common Issues

<!-- TODO: Add common issues and solutions -->
1. **Issue**: TBD
   - **Solution**: TBD

## Additional Resources

<!-- TODO: Add relevant links -->
- [Project Documentation](./docs/)
- [Contributing Guidelines](./CONTRIBUTING.md)
- [Issue Tracker](<repository-issues-url>)

---

*This CLAUDE.md file should be updated as the project evolves. Keep it current to help AI assistants work effectively with the codebase.*
