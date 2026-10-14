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
after the meeting with Suzie Allard, and so on). Each version gets its own
DOI; the concept DOI in `CITATION.cff` always resolves to the latest.

1. In the working Google Doc, set the version line at the top (e.g.
   "Draft v0.3, <date>") and rename the Doc so its title ends in
   "(draft v0.3)"; the PDF's metadata title comes from the Doc title.
2. Export the Doc twice into `codebook/`: File → Download → PDF as
   `codebook-v0.3.pdf`, and File → Download → Markdown as
   `codebook-v0.3.md`. Keep the earlier versions' files.
3. Update `CITATION.cff`: `version: 0.3` and `date-released`. If the author
   list changed, update `authors` here and `creators` in `.zenodo.json`.
4. If the coded catalog changed with the codebook, export the current
   coding sheet to `catalog/catalog-full.csv` and update `catalog.csv`.
5. Commit and push to `main`.
6. On GitHub, Releases → "Draft a new release": create tag `v0.3` on
   `main`, title "Codebook v0.3", one line on what changed, Publish.
   Zenodo archives the release within a few minutes, mints the DOI, and
   submits the record to the `open-physics-data-terms` community.
7. First release only: copy the **concept DOI** from the Zenodo record (the
   one under "Cite all versions") into `CITATION.cff` as `doi:` and push.
   Later versions keep the same concept DOI. The session website reads it
   from here.

## License

CC BY 4.0 (see LICENSE).
