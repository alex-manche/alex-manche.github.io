#!/usr/bin/env python3
"""Synchronise the al-folio BibTeX file from DOI metadata.

Discovery strategy:
1. Always keep DOIs listed in publication_sources.json.
2. Query Crossref for works that carry the configured ORCID iD.
3. If ORCID public API credentials are available, also query ORCID directly.
4. Resolve each DOI with BibTeX content negotiation and write papers.bib.

The script uses only Python's standard library so it runs cleanly in GitHub Actions.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / 'publication_sources.json'
OUTPUT = ROOT / '_bibliography' / 'papers.bib'
USER_AGENT = 'alex-manche.github.io publication-sync/1.0 (https://github.com/alex-manche/alex-manche.github.io)'


def request_json(url: str, *, headers: dict[str, str] | None = None, data: bytes | None = None) -> dict:
    h = {'User-Agent': USER_AGENT, 'Accept': 'application/json'}
    if headers:
        h.update(headers)
    req = Request(url, headers=h, data=data, method='POST' if data is not None else 'GET')
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode('utf-8'))


def normalise_doi(value: str) -> str:
    value = value.strip()
    value = re.sub(r'^https?://(?:dx\.)?doi\.org/', '', value, flags=re.I)
    value = re.sub(r'^doi:\s*', '', value, flags=re.I)
    return value.strip().rstrip('.').lower()


def crossref_orcid_dois(orcid: str) -> set[str]:
    params = urlencode({'filter': f'orcid:{orcid}', 'rows': 1000, 'select': 'DOI'})
    url = f'https://api.crossref.org/works?{params}'
    try:
        payload = request_json(url)
    except Exception as exc:
        print(f'[warn] Crossref ORCID discovery failed: {exc}', file=sys.stderr)
        return set()
    items = payload.get('message', {}).get('items', [])
    return {normalise_doi(x['DOI']) for x in items if x.get('DOI')}


def orcid_token(client_id: str, client_secret: str) -> str:
    data = urlencode({
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials',
        'scope': '/read-public',
    }).encode()
    payload = request_json(
        'https://orcid.org/oauth/token',
        headers={'Accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'},
        data=data,
    )
    return payload['access_token']


def orcid_dois(orcid: str, token: str) -> set[str]:
    url = f'https://pub.orcid.org/v3.0/{quote(orcid)}/works'
    payload = request_json(
        url,
        headers={'Accept': 'application/vnd.orcid+json', 'Authorization': f'Bearer {token}'},
    )
    found: set[str] = set()
    for group in payload.get('group', []):
        candidates = []
        if group.get('external-ids'):
            candidates.extend(group['external-ids'].get('external-id', []))
        for summary in group.get('work-summary', []):
            if summary.get('external-ids'):
                candidates.extend(summary['external-ids'].get('external-id', []))
        for ext in candidates:
            if str(ext.get('external-id-type', '')).lower() == 'doi' and ext.get('external-id-value'):
                found.add(normalise_doi(ext['external-id-value']))
    return found


def fetch_bibtex(doi: str) -> str:
    url = 'https://doi.org/' + quote(doi, safe='/()')
    req = Request(url, headers={'User-Agent': USER_AGENT, 'Accept': 'application/x-bibtex'})
    with urlopen(req, timeout=30) as resp:
        text = resp.read().decode('utf-8').strip()
    if not text.startswith('@'):
        raise ValueError('DOI resolver did not return BibTeX')
    return text


def field(entry: str, name: str) -> str:
    m = re.search(rf'\b{name}\s*=\s*[{{\"]([^}}\"]+)', entry, flags=re.I)
    return m.group(1).strip() if m else ''


def add_fields(entry: str, doi: str, selected: bool) -> str:
    additions = []
    if not re.search(r'\bbibtex_show\s*=', entry, flags=re.I):
        additions.append('bibtex_show = {true}')
    if not re.search(r'\bdoi\s*=', entry, flags=re.I):
        additions.append(f'doi = {{{doi}}}')
    if selected and not re.search(r'\bselected\s*=', entry, flags=re.I):
        additions.append('selected = {true}')
    if not additions:
        return entry
    pos = entry.rfind('}')
    if pos < 0:
        return entry
    head = entry[:pos].rstrip()
    if not head.endswith(','):
        head += ','
    return head + '\n  ' + ',\n  '.join(additions) + '\n}' + entry[pos+1:]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--validate-only', action='store_true', help='validate configuration without network access')
    args = parser.parse_args()

    cfg = json.loads(CONFIG.read_text())
    orcid = cfg['orcid']
    manual = {normalise_doi(x) for x in cfg.get('manual_dois', [])}
    selected = {normalise_doi(x) for x in cfg.get('selected_dois', [])}
    excluded = {normalise_doi(x) for x in cfg.get('exclude_dois', [])}
    if args.validate_only:
        assert re.fullmatch(r'\d{4}-\d{4}-\d{4}-\d{3}[\dX]', orcid)
        assert manual
        print(f'configuration OK: {orcid}, {len(manual)} manual DOI(s)')
        return 0

    dois = set(manual)
    discovered_crossref = crossref_orcid_dois(orcid)
    dois |= discovered_crossref
    print(f'Crossref discovery: {len(discovered_crossref)} DOI(s)')

    cid = os.environ.get('ORCID_CLIENT_ID', '').strip()
    secret = os.environ.get('ORCID_CLIENT_SECRET', '').strip()
    if cid and secret:
        try:
            token = orcid_token(cid, secret)
            discovered_orcid = orcid_dois(orcid, token)
            dois |= discovered_orcid
            print(f'ORCID discovery: {len(discovered_orcid)} DOI(s)')
        except Exception as exc:
            print(f'[warn] ORCID API discovery failed: {exc}', file=sys.stderr)
    else:
        print('[info] ORCID credentials not set; using Crossref + manual DOI discovery.')

    dois -= excluded
    entries = []
    failures = []
    for i, doi in enumerate(sorted(dois), 1):
        try:
            entry = fetch_bibtex(doi)
            entry = add_fields(entry, doi, doi in selected)
            entries.append((field(entry, 'year'), doi, entry))
            print(f'[{i:02d}/{len(dois):02d}] {doi}')
        except (HTTPError, URLError, ValueError, TimeoutError) as exc:
            failures.append((doi, str(exc)))
            print(f'[warn] {doi}: {exc}', file=sys.stderr)
        time.sleep(0.10)

    if not entries:
        print('No BibTeX entries were fetched; leaving existing bibliography untouched.', file=sys.stderr)
        return 1

    entries.sort(key=lambda x: (x[0], x[1]), reverse=True)
    header = (
        '% AUTO-GENERATED by scripts/update_publications.py\n'
        '% Sources: manual DOI list + Crossref ORCID metadata + optional ORCID Public API.\n'
        '% Add custom selections in publication_sources.json; do not hand-edit this file after enabling sync.\n\n'
    )
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(header + '\n\n'.join(e[2] for e in entries) + '\n', encoding='utf-8')
    print(f'Wrote {len(entries)} entries to {OUTPUT.relative_to(ROOT)}')
    if failures:
        print(f'{len(failures)} DOI(s) could not be refreshed; see warnings above.', file=sys.stderr)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
