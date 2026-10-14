# Codebook: license and attribution terms of open physics data

The survey instrument and coded data behind the study of what license and
attribution terms physics collaborations attach to their public data
releases. Developed by the organizers of the SESAPS 2026 moderated
discussion "Open physics data: what license and attribution terms should it
carry?" (det-lab/open-physics-data-terms), and kept separate from it so
that the codebook can be versioned, reused, and cited on its own.

## Layout

- `codebook/` — the codebook, one file per version (`codebook-v0.2.pdf`
  and `.md`). The current working copy is a Google Doc; export it here at
  each tagged version.
- `catalog/catalog.csv` — summary table, one row per collaboration.
- `catalog/catalog-full.csv` — every coded field, one row per release
  (exported from the coding sheet when a coding round is complete).
- `catalog/to-check.csv` — items awaiting a human check, with the URL and
  what to look for.

## Releasing a new version

Do this whenever the codebook changes in a way that affects coding (v0.3
after the meeting with Suzie Allard, and so on).

1. In the working Google Doc, set the version line at the top ("Draft
   v0.3, <date>") and rename the Doc so its title ends in "(draft v0.3)";
   the PDF's metadata title comes from the Doc title.
2. Export the Doc into `codebook/`: File → Download → PDF as
   `codebook-v0.3.pdf`, and File → Download → Markdown as
   `codebook-v0.3.md`. Keep earlier versions' files.
3. If the author list changed, update `authors` in `CITATION.cff` and
   `creators` in `.zenodo.json`. If the coded catalog changed, export it to
   `catalog/`.
4. Commit and push to `main`.

The rest is automatic: the workflow sees the new `codebook-v0.3.pdf`, sets
`version` in `CITATION.cff`, publishes the GitHub release `v0.3` (Zenodo
archives it and mints the version DOI; the concept DOI stays the same and is
written into `CITATION.cff` the first time), and asks the session website
to rebuild so its "Papers and survey methods" page shows the new version.
Making the release by hand on GitHub works too; the same workflow then
syncs the DOI.

Each version has its own DOI; the concept DOI in `CITATION.cff` always
resolves to the latest. A paper that uses the codebook should cite the
version it used.

## Workflows and secrets

- `release.yml` — runs on a push that adds `codebook/codebook-v*.pdf`, on a
  published release, or by hand: creates the release if it is missing,
  waits for Zenodo, writes the concept DOI into `CITATION.cff`, and asks
  the session website to rebuild.
- `diagnose.yml` — run by hand to see what the Zenodo lookup finds for a
  tag, if a release did not sync.

Secrets: `SITE_DISPATCH_TOKEN` (a fine-grained GitHub token with access to
`det-lab/open-physics-data-terms-site`, Contents: read and write) so the
website rebuilds after a release; without it, rebuild the site by hand.
`ZENODO_TOKEN` is optional: with it the lookup can also see records still
pending community review.

## License

CC BY 4.0 (see LICENSE).
