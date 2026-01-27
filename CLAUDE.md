# CLAUDE.md - AI Assistant Guidelines

This document provides essential context and guidelines for AI assistants working with the Claude repository.

## Repository Overview

**Project**: Claude
**Status**: Initial development phase
**Primary Branch**: `claude/claude-md-mkwimav0zi1jxrlw-OvdjY`

This repository is in its early stages and serves as a foundation for future development. The project structure and conventions outlined below should be followed as the codebase grows.

## Project Structure

```
Claude/
├── README.md          # Project overview and documentation
├── CLAUDE.md          # AI assistant guidelines (this file)
└── (future directories will be documented here)
```

### Planned Structure Conventions

When adding new code to this repository, follow these organizational patterns:

- **`src/`** - Main source code
- **`tests/`** - Test files (mirror the src/ structure)
- **`docs/`** - Additional documentation
- **`scripts/`** - Utility and automation scripts
- **`config/`** - Configuration files

## Development Workflow

### Git Conventions

1. **Branch Naming**: Use descriptive branch names prefixed appropriately
   - Feature: `feature/description`
   - Bugfix: `fix/description`
   - Claude AI branches: `claude/session-id`

2. **Commit Messages**: Write clear, descriptive commit messages
   - Use imperative mood: "Add feature" not "Added feature"
   - Keep first line under 72 characters
   - Include context in the body when needed

3. **Pushing Changes**:
   ```bash
   git push -u origin <branch-name>
   ```

### Code Quality Standards

- Write clean, readable code with meaningful variable names
- Include appropriate comments for complex logic
- Follow language-specific style guides (to be defined per language)
- Avoid over-engineering; keep solutions simple and focused

## For AI Assistants

### Before Making Changes

1. **Read first**: Always read files before modifying them
2. **Understand context**: Review related files to understand the codebase
3. **Check for existing patterns**: Follow established conventions in the codebase
4. **Avoid assumptions**: Ask for clarification when requirements are unclear

### When Writing Code

1. **Security**: Never introduce vulnerabilities (injection attacks, XSS, etc.)
2. **Simplicity**: Only make changes that are directly requested or clearly necessary
3. **No over-engineering**: Don't add features, refactor, or make "improvements" beyond what was asked
4. **Test coverage**: Include tests for new functionality when a testing framework is present

### File Operations

- Prefer editing existing files over creating new ones
- Use appropriate tools for file operations (Read, Edit, Write)
- Never guess at file contents - always read first

### Communication

- Be concise and direct
- Focus on technical accuracy
- Provide file paths with line numbers when referencing code: `path/to/file.ext:line_number`

## Build & Development Commands

> **Note**: Commands will be added here as the project develops.

Currently, no build system is configured. When one is added:

```bash
# Placeholder for future commands
# npm install / pip install / cargo build / etc.
# npm test / pytest / cargo test / etc.
# npm run build / python setup.py build / etc.
```

## Testing

> **Note**: Testing framework to be determined.

When tests are added:
- Place test files in the `tests/` directory
- Follow naming convention: `test_*.py` or `*.test.js` (language-dependent)
- Aim for meaningful test coverage

## Configuration Files

Current configuration:
- `.git/config` - Git repository configuration

Future configuration files should be documented here as they are added.

## Dependencies

No dependencies are currently configured. When added:
- Document major dependencies and their purposes
- Keep dependencies minimal and well-justified
- Use lock files for reproducible builds

## Known Issues & Limitations

None currently documented.

## Quick Reference

| Action | Command/Approach |
|--------|------------------|
| Push changes | `git push -u origin <branch-name>` |
| Run tests | (To be configured) |
| Build project | (To be configured) |
| Lint code | (To be configured) |

---

*This document should be updated as the project evolves. Last updated: 2026-01-27*
