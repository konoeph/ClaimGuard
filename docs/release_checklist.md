# Release Checklist

Use this checklist before publishing an AgentClaimGuard release.

- [ ] Update version in `pyproject.toml`
- [ ] Update server version if applicable
- [ ] Update `CHANGELOG.md`
- [ ] Run `python -m pytest -q`
- [ ] Run `python -m compileall agentclaimguard examples tests`
- [ ] Run relevant demos
- [ ] Install release tools with `pip install -e ".[release]"`
- [ ] Build wheel and sdist with `python -m build`
- [ ] Validate distributions with `python -m twine check dist/*`
- [ ] Optionally publish to TestPyPI
- [ ] Verify install in a fresh virtual environment
- [ ] Push to `main`
- [ ] Confirm GitHub Actions is green
- [ ] Create an annotated tag
- [ ] Publish the GitHub Release
- [ ] Publish to PyPI through the `Publish to PyPI` GitHub Actions workflow
- [ ] Verify install from PyPI in a fresh virtual environment

## PyPI Trusted Publishing

PyPI publishing should use the `Publish to PyPI` GitHub Actions workflow.
The project is configured for PyPI Trusted Publishing with:

- Owner: `konoeph`
- Repository: `AgentClaimGuard`
- Workflow name: `publish.yml`
- Environment: `pypi`

After a release tag and GitHub Release are ready, run the `Publish to PyPI`
workflow manually and enter the release tag as the `ref` input.

## Manual PyPI Fallback

Manual token-based upload should only be used if Trusted Publishing is
temporarily unavailable:

```bash
python -m build
python -m twine check dist/*
python -m twine upload dist/*
```
