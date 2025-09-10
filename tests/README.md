# SimpleNBA-API Test Suite

This directory contains unit tests for the SimpleNBA-API project.

## Running Tests

To run all tests:

```bash
python -m pytest tests/
```

To run tests with coverage:

```bash
python -m pytest tests/ --cov=simplenba --cov-report=html
```

To run a specific test file:

```bash
python -m pytest tests/test_simplenba.py
```

## Test Structure

- `test_simplenba.py` - Main test file containing unit tests for:
  - Data models (Player, Team, Game, PlayerStats)
  - API functionality
  - Utility functions
  - Error handling

## Test Coverage

The tests cover:

- Model creation and validation
- API request handling and error cases
- Utility function calculations
- Data export functionality
- Statistical calculations

## Adding New Tests

When adding new features, please include corresponding tests:

1. Create test methods following the naming convention `test_feature_name`
2. Use meaningful assertions
3. Mock external API calls to avoid rate limiting
4. Test both success and error cases