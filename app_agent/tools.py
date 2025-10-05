import httpx

FPL_BOOTSTRAP_URL = "https://fantasy.premierleague.com/api/bootstrap-static/"

async def fpl_bootstrap():
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(FPL_BOOTSTRAP_URL)
        r.raise_for_status()
        data = r.json()
        # Return only a tiny slice for the POC
        players = [
            {
                "id": p["id"],
                "web_name": p["web_name"],
                "now_cost": p["now_cost"],
                "form": p.get("form", "0"),
                "team": p["team"],
                "status": p["status"],
                "selected_by_percent": p.get("selected_by_percent", "0.0"),
            }
            for p in data.get("elements", [])[:200]
        ]
        teams = data.get("teams", [])
        events = data.get("events", [])
        return {"players": players, "teams": teams, "events": events}

async def optimize_squad(candidates):
    """Very naive heuristic for POC: pick captain as highest (form, then cost).
    Returns one suggested transfer in/out if we see an injured popular player.
    """
    if not candidates:
        return {
            "captain": "",
            "transfers_out": [],
            "transfers_in": [],
            "rationale": "No candidates provided",
        }

    # Sort by form (desc), then price (desc)
    ranked = sorted(
        candidates,
        key=lambda x: (float(x.get("form", "0") or 0), x.get("now_cost", 0)),
        reverse=True,
    )
    captain = ranked[0]["web_name"]

    # Very naive transfer suggestion: if top-1 is 'doubtful'/'injured', swap to next
    injured_status = {"i", "d"}  # i=injured, d=doubtful in FPL API
    transfers_out, transfers_in = [], []
    if ranked and ranked[0].get("status") in injured_status:
        transfers_out = [ranked[0]["web_name"]]
        # Find first fully-available alt
        alt = next((p for p in ranked[1:] if p.get("status") == "a"), None)
        if alt:
            transfers_in = [alt["web_name"]]

    return {
        "captain": captain,
        "transfers_out": transfers_out,
        "transfers_in": transfers_in,
        "rationale": "POC heuristic based on form and availability",
    }