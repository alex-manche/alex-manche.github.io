# alex-manche.github.io

Academic website for Alexis Manche, built with the current **al-folio v1.x** plugin architecture.

## What is included

- Distinctive materials-science visual identity (teal/indigo + orange spectral accent)
- About, research, publications, projects/software, code and CV pages
- BibTeX publications rendered with `jekyll-scholar`
- Scheduled publication discovery from Crossref + optional ORCID Public API
- RenderCV-compatible `_data/cv.yml`
- Downloadable PDF CV in `assets/pdf/`
- GitHub Actions deployment to `gh-pages`

## First deployment

1. Create a **public** repository named exactly `alex-manche.github.io`.
2. Copy this repository into it and push to `main`.
3. GitHub → **Settings → Actions → General → Workflow permissions** → enable **Read and write permissions**.
4. Run the **Deploy site** workflow once (or push a change).
5. After the `gh-pages` branch appears, GitHub → **Settings → Pages** → deploy from `gh-pages` / root.
6. The site will be available at `https://alex-manche.github.io`.

## Publication automation

The website always keeps the DOI list in `publication_sources.json`. Every Monday, `.github/workflows/update-publications.yml`:

1. queries Crossref for works associated with ORCID `0000-0002-8505-474X`;
2. optionally queries the ORCID Public API directly;
3. resolves each DOI as BibTeX;
4. regenerates `_bibliography/papers.bib`;
5. commits the change if metadata or publications changed.

### Recommended: enable ORCID discovery

Create ORCID **Public API credentials** in your ORCID developer tools, then add two repository secrets:

- `ORCID_CLIENT_ID`
- `ORCID_CLIENT_SECRET`

Without those secrets the workflow still works from the manual DOI seed list and Crossref's ORCID metadata, but direct ORCID discovery is skipped.

### Recommended: enable automatic re-deployment after publication updates

GitHub does not let a commit made with the default `GITHUB_TOKEN` trigger another workflow. For fully hands-off publication → deploy automation, create a fine-grained GitHub PAT with **Contents: Read and write** for this repository and store it as a repository secret named `PAT`.

If you do not add a `PAT`, publication updates still commit successfully; just run **Deploy site** manually after an automated update.

## Editing the site

- Home: `_pages/about.md`
- Research: `_pages/research.md`
- Projects: `_projects/*.md`
- News: `_news/*.md`
- CV: `_data/cv.yml`
- Publication source configuration: `publication_sources.json`
- Styling: `_sass/_themes.scss`
- Visual assets: `assets/img/*.svg`

## Local validation

The official al-folio project recommends Docker for local development. After installing Docker, use the al-folio development image/workflow from the upstream documentation, or build through GitHub Actions.

You can always validate the publication configuration without network access:

```bash
python scripts/update_publications.py --validate-only
```
