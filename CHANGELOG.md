# Changelog

## [0.1.4] - 2026-05-22

### Added
- [Parametrize tests] Added support parametrize tests: [38](https://github.com/Khabib73/YATL/issues/38)
- Support run tests without concurrency: [#94](https://github.com/Khabib73/YATL/pull/94)

### Fixed
- CI now tests local package instead of published version
- Non-zero exit code on validation errors  
[#108](https://github.com/Khabib73/YATL/pull/108)

### Changed
- Failed tests are accumulated and displayed at the end
- Improve documentation
- Use filename as test name if name key is missing: [#101](https://github.com/Khabib73/YATL/issues/101)


### Removed
- Removed 'decs' key: [#72](https://github.com/Khabib73/YATL/pull/72)
