# Contributing to Architecture Auditor Pro

Thank you for your interest in contributing to Architecture Auditor Pro! This document provides guidelines and information for contributors.

## 🚀 Quick Start for Contributors

1. **Fork** the repository
2. **Clone** your fork locally
3. **Create** a feature branch
4. **Make** your changes
5. **Test** thoroughly
6. **Submit** a pull request

## 📋 Development Setup

### Prerequisites

- Python 3.8+
- Git
- Virtual environment tool (venv, conda, etc.)

### Local Development

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/architecture-auditor.git
cd architecture-auditor/architecture-auditor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies

# Run tests
python -m pytest tests/

# Run the auditor on itself (dogfooding!)
python intelligent_auditor.py . --verbose
```

## 🎯 Types of Contributions

### 🐛 Bug Reports

When reporting bugs, please include:

- **Clear description** of the issue
- **Steps to reproduce** the problem
- **Expected vs actual behavior**
- **Environment details** (OS, Python version, etc.)
- **Sample code** or project structure (if applicable)

### ✨ Feature Requests

For new features, please provide:

- **Use case description** - Why is this needed?
- **Proposed solution** - How should it work?
- **Alternative approaches** - Other ways to solve the problem
- **Implementation ideas** - Technical approach (if you have one)

### 🔧 Code Contributions

We welcome:

- **New architecture patterns** detection
- **Additional project types** support
- **Performance improvements**
- **Documentation enhancements**
- **Test coverage improvements**
- **Bug fixes**

## 📝 Coding Standards

### Code Quality Requirements

All contributions must meet our quality standards:

```bash
# Your code should pass our own auditor!
python intelligent_auditor.py . --min-score 85

# Code formatting
black .
isort .

# Linting
flake8 .
pylint intelligent_auditor.py

# Type checking
mypy intelligent_auditor.py
```

### Architecture Patterns

When adding new pattern detection:

1. **Research thoroughly** - Understand the pattern completely
2. **Add to documentation** - Update `arquitecturas-software-clase1.html`
3. **Create tests** - Include positive and negative test cases
4. **Update configuration** - Add to `architecture_patterns.json`
5. **Document indicators** - Clear detection criteria

### Clean Code Principles

Follow the same principles we audit:

- **Functions < 20 lines**
- **Classes < 15 methods**
- **Meaningful names**
- **Single responsibility**
- **Proper error handling**
- **Appropriate comments**

## 🧪 Testing Guidelines

### Test Structure

```
tests/
├── unit/                 # Unit tests
│   ├── test_auditor.py
│   └── test_patterns.py
├── integration/          # Integration tests
│   └── test_full_audit.py
├── fixtures/            # Test data
│   ├── sample_projects/
│   └── expected_results/
└── conftest.py          # Pytest configuration
```

### Writing Tests

```python
def test_mvc_pattern_detection():
    """Test MVC pattern detection with proper structure."""
    # Arrange
    project_structure = create_test_project({
        'models/': ['user.py', 'product.py'],
        'views/': ['user_view.py'],
        'controllers/': ['user_controller.py']
    })
    
    # Act
    auditor = IntelligentArchitectureAuditor(project_structure)
    results = auditor.audit_project()
    
    # Assert
    assert 'MVC' in results['architecture_patterns']['patterns_detected']
    assert results['architecture_patterns']['score'] >= 25
```

### Test Coverage

- **Minimum 80% coverage** for new code
- **100% coverage** for critical functions
- **Integration tests** for major features
- **Performance tests** for optimization changes

## 📚 Documentation

### Code Documentation

```python
def detect_clean_architecture(self) -> bool:
    """
    Detect Clean Architecture pattern implementation.
    
    Based on Uncle Bob's Clean Architecture principles, this method
    looks for the characteristic directory structure and dependency
    flow of Clean Architecture.
    
    Returns:
        bool: True if Clean Architecture pattern is detected
        
    References:
        - Clean Architecture book by Robert C. Martin
        - arquitecturas-software-clase1.html section on Clean Architecture
    """
```

### User Documentation

- Update `README.md` for user-facing changes
- Update `arquitecturas-software-clase1.html` for architecture patterns
- Add examples for new features
- Include configuration options

## 🔄 Pull Request Process

### Before Submitting

1. **Rebase** on latest main branch
2. **Run all tests** and ensure they pass
3. **Update documentation** as needed
4. **Add changelog entry** if applicable
5. **Self-review** your changes

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Refactoring

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed
- [ ] Auditor passes on own codebase

## Documentation
- [ ] README updated
- [ ] Architecture documentation updated
- [ ] Code comments added
- [ ] Changelog updated

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Tests pass locally
- [ ] No breaking changes (or clearly documented)
```

### Review Process

1. **Automated checks** must pass
2. **Code review** by maintainers
3. **Testing** in different environments
4. **Documentation review**
5. **Final approval** and merge

## 🏆 Recognition

### Contributors Hall of Fame

We recognize contributors in:

- **README.md** acknowledgments
- **Release notes** for significant contributions
- **Annual contributor report**
- **Conference presentations** (with permission)

### Contribution Levels

- **🥉 Bronze**: First contribution merged
- **🥈 Silver**: 5+ contributions or major feature
- **🥇 Gold**: 10+ contributions or architectural improvements
- **💎 Diamond**: Core maintainer status

## 📞 Getting Help

### Communication Channels

- **GitHub Discussions**: General questions and ideas
- **GitHub Issues**: Bug reports and feature requests
- **Email**: maintainers@architectureauditor.com
- **Discord**: [Architecture Auditor Community](https://discord.gg/architecture-auditor)

### Mentorship Program

New contributors can request mentorship:

1. **Comment on issues** tagged `good-first-issue`
2. **Join our Discord** for real-time help
3. **Attend office hours** (Fridays 2-4 PM UTC)
4. **Pair programming sessions** available

## 📋 Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of:

- Experience level
- Gender identity and expression
- Sexual orientation
- Disability
- Personal appearance
- Body size
- Race
- Ethnicity
- Age
- Religion
- Nationality

### Expected Behavior

- **Be respectful** and inclusive
- **Give constructive feedback**
- **Accept criticism gracefully**
- **Focus on what's best** for the community
- **Show empathy** towards others

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Personal or political attacks
- Publishing private information
- Inappropriate sexual content

### Enforcement

Violations can be reported to conduct@architectureauditor.com. All reports will be reviewed and investigated promptly and fairly.

## 🎯 Roadmap & Priorities

### Current Priorities

1. **Performance optimization** for large codebases
2. **Additional language support** (JavaScript, Java, C#)
3. **Cloud integration** features
4. **Advanced reporting** capabilities
5. **Machine learning** pattern detection

### How to Align Contributions

- Check **GitHub Projects** for current sprint
- Look for **help-wanted** labels
- Discuss **major features** before implementation
- Consider **backward compatibility**

---

## 🙏 Thank You

Every contribution, no matter how small, makes Architecture Auditor Pro better for everyone. We appreciate your time and effort in helping us build the best code quality tool possible!

**Happy coding!** 🚀

---

*This contributing guide is a living document. Please suggest improvements!*