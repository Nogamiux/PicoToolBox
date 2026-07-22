from __future__ import annotations

from dataclasses import dataclass

import requests

API_BASE = "https://api.github.com"
TIMEOUT = 15

REPOS = {
    "pico_loader": "LNH-team/pico-loader",
    "pico_launcher": "LNH-team/pico-launcher",
    "dspico_hybrid_fw": "coderkei/dspico-hybrid-fw",
    "pico_theme_switcher": "Nogamiux/Pico-theme-switcher",
}


@dataclass
class ReleaseAsset:
    name: str
    download_url: str
    size: int


@dataclass
class ReleaseInfo:
    repo: str
    tag_name: str
    name: str
    published_at: str
    assets: list[ReleaseAsset]
    html_url: str


class GitHubError(RuntimeError):
    pass


def _headers():
    return {"Accept": "application/vnd.github+json", "User-Agent": "dspico-updater"}


def get_latest_release(repo_key: str) -> ReleaseInfo:
    repo = REPOS[repo_key]
    url = f"{API_BASE}/repos/{repo}/releases/latest"
    try:
        resp = requests.get(url, headers=_headers(), timeout=TIMEOUT)
    except requests.RequestException as exc:
        raise GitHubError(f"Connessione a GitHub fallita: {exc}") from exc

    if resp.status_code == 403:
        raise GitHubError("Limite di richieste GitHub raggiunto, riprova più tardi.")
    if resp.status_code == 404:
        raise GitHubError(f"Nessuna release trovata per {repo}.")
    if not resp.ok:
        raise GitHubError(f"Errore GitHub ({resp.status_code}) per {repo}.")

    data = resp.json()
    assets = [
        ReleaseAsset(
            name=a["name"],
            download_url=a["browser_download_url"],
            size=a.get("size", 0),
        )
        for a in data.get("assets", [])
    ]
    return ReleaseInfo(
        repo=repo,
        tag_name=data.get("tag_name", "?"),
        name=data.get("name") or data.get("tag_name", "?"),
        published_at=data.get("published_at", ""),
        assets=assets,
        html_url=data.get("html_url", ""),
    )


def check_all_updates(keys: list[str] | None = None) -> dict[str, ReleaseInfo]:
    target_keys = keys if keys is not None else list(REPOS)
    return {key: get_latest_release(key) for key in target_keys}