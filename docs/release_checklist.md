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
- [ ] Publish to PyPI, preferably through the `Publish to PyPI` GitHub Actions workflow

## PyPI Trusted Publishing

Configure the PyPI project trusted publisher before using the publishing
workflow:

- Owner: `konoeph`
- Repository: `AgentClaimGuard`
- Workflow name: `publish.yml`
- Environment: `pypi`

After a release tag and GitHub Release are ready, run the `Publish to PyPI`
workflow manually and enter the release tag as the `ref` input.
