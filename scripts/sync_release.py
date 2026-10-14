#!/usr/bin/env python3
"""Keep CITATION.cff and GitHub releases in step with the codebook files and Zenodo.

Run on push to main (a new codebook/codebook-vX.Y.pdf creates the release) and on
release published (reads the DOI back from Zenodo). Idempotent.

 1. Version = highest codebook/codebook-vX.Y.pdf. If CITATION.cff says an older
    version, update it (version, date-released).
 2. If no GitHub release/tag vX.Y exists, create it (GITHUB_TOKEN).
 3. Wait for Zenodo's record of tag vX.Y; write the concept DOI into CITATION.cff
    if missing. Commit and push if anything changed.
Env: GITHUB_TOKEN, GITHUB_REPOSITORY.
"""
import datetime, os, re, subprocess, sys, time
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from zenodo_lookup import find_record  # noqa: E402

REPO = os.environ.get("GITHUB_REPOSITORY", "det-lab/open-physics-data-codebook")
GH = os.environ.get("GITHUB_TOKEN")
CFF = ROOT / "CITATION.cff"
H = {"Authorization": f"Bearer {GH}", "Accept": "application/vnd.github+json"}


def sh(*cmd, check=True):
    print("+", " ".join(cmd), flush=True)
    return subprocess.run(cmd, check=check, text=True, capture_output=True).stdout


def cff_get(key):
    m = re.search(rf"^{key}:\s*(.+?)\s*$", CFF.read_text(), re.M)
    return m.group(1).strip('"') if m else None


def cff_set(key, value):
    s = CFF.read_text()
    if re.search(rf"^#? ?{key}:", s, re.M):
        s = re.sub(rf"^#? ?{key}:.*$", f"{key}: {value}", s, count=1, flags=re.M)
    else:
        s = s.rstrip("\n") + f"\n{key}: {value}\n"
    CFF.write_text(s)


def vkey(v):
    return tuple(int(x) for x in v.split("."))


def main():
    files = sorted((ROOT / "codebook").glob("codebook-v*.pdf"))
    versions = [re.search(r"codebook-v(\d+\.\d+)\.pdf$", f.name).group(1) for f in files]
    if not versions:
        print("no codebook PDF"); return
    version = max(versions, key=vkey)
    tag = f"v{version}"
    changed = False
    if cff_get("version") != version:
        cff_set("version", version); cff_set("date-released", datetime.date.today().isoformat()); changed = True

    r = requests.get(f"https://api.github.com/repos/{REPO}/releases/tags/{tag}", headers=H, timeout=60)
    if r.status_code == 404:
        if changed:
            sh("git", "config", "user.name", "github-actions[bot]")
            sh("git", "config", "user.email", "github-actions[bot]@users.noreply.github.com")
            sh("git", "add", "CITATION.cff"); sh("git", "commit", "-m", f"Codebook {tag}"); sh("git", "push"); changed = False
        r = requests.post(f"https://api.github.com/repos/{REPO}/releases", headers=H, timeout=60,
                          json={"tag_name": tag, "target_commitish": "main", "name": f"Codebook {tag}",
                                "body": f"Codebook {tag}: codebook/codebook-{tag}.pdf and .md."})
        r.raise_for_status(); print("created release", r.json().get("html_url"))

    doi = cff_get("doi")
    if not doi or "XXXX" in doi:
        print("waiting for Zenodo ...")
        rec, deadline = None, time.time() + 900
        while not rec and time.time() < deadline:
            rec = find_record(REPO, tag)
            if not rec: time.sleep(30)
        if not rec or not rec.get("conceptdoi"):
            sys.exit("Zenodo record not found after 15 minutes; is the GitHub integration on for this repository?")
        cff_set("doi", rec["conceptdoi"]); changed = True
        print("concept DOI", rec["conceptdoi"], "version DOI", rec["doi"])

    if changed:
        sh("git", "config", "user.name", "github-actions[bot]")
        sh("git", "config", "user.email", "github-actions[bot]@users.noreply.github.com")
        sh("git", "add", "CITATION.cff"); sh("git", "commit", "-m", f"CITATION.cff for {tag}"); sh("git", "push")
    print("done", tag, cff_get("doi"))


if __name__ == "__main__":
    main()
