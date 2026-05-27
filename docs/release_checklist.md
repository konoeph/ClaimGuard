# Release Checklist

Use this checklist before publishing an AgentClaimGuard release.

- [ ] Update version in `pyproject.toml`
- [ ] Update server version if applicable
- [ ] Update `CHANGELOG.md`
- [ ] Run `python -m pytest -q`
- [ ] Run `python -m compileall agentclaimguard examples tests`
- [ ] Run relevant demos
- [ ] Push to `main`
- [ ] Confirm GitHub Actions is green
- [ ] Create an annotated tag
- [ ] Publish the GitHub Release
