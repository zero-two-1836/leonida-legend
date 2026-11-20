#!/usr/bin/env python3
"""Build app/data/trophies.json for Leonida Legend.

The official fields (name, description, grade) are read from the verified
official list carried in ../repo3/app/data/trophies.json — itself checked
entry-for-entry against the kit starter's list — so they can never drift in
transcription. Everything else (kind, phase, steps, pitfalls, times, counts,
hidden flags and per-trophy sources) is this entry's own guide material,
written for Leonida Legend and keyed by the official list's ids.

Run:  python3 tools/build_data.py
Out:  app/data/trophies.json
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve()
REPO = HERE.parent.parent
OFFICIAL = REPO.parent / "repo3" / "app" / "data" / "trophies.json"
OUT = REPO / "app" / "data" / "trophies.json"

# Named sources. "url" is given only where the page was opened and checked
# while this guide was written; the rest are named, as the bounty allows.
SOURCES = {
    "psn": {
        "name": "PlayStation's official GTA VI trophy list — names, descriptions, grades and tracked counts",
    },
    "psnprofiles": {
        "name": "PSNProfiles' GTA VI trophy list — the same official list, with per-trophy rarity and counts",
    },
    "exophase": {
        "name": "Exophase's GTA VI trophy listing — cross-check of the official names and grades",
    },
    "powerpyx": {
        "name": "PowerPyx, “GTA 6 Trophy Guide & Roadmap” — roadmap, difficulty and method notes",
        "url": "https://www.powerpyx.com/gta-6-grand-theft-auto-vI-trophy-guide-roadmap/",
    },
    "sixshore": {
        "name": "SixShore, “GTA 6 Trophy and Achievement List: All 55, Missables and Roadmap” — hidden-trophy split and method confirmations",
        "url": "https://sixshore.com/gta-6/guides/trophies-and-achievements/",
    },
    "gtadb": {
        "name": "GTADB, “GTA 6 PS5 Trophies & Platinum Guide” — cross-checked list and platinum overview",
        "url": "https://gtadb.net/articles/gta-6-trophies-platinum-guide/?show_secrets=1",
    },
    "egamers": {
        "name": "EGamers, “GTA 6 Trophy List: All 55 Trophies and Achievements” — hidden/non-hidden grade split",
        "url": "https://egamers.io/gta-6-trophy-list-all-55-trophies-and-achievements-plus-the-hardest-ones/",
    },
}

# kind: story | side | missable | collectibles | activities | cleanup
# phase: 1 story, 2 the 100% engine, 3 collectibles & world, 4 strangers, 5 cleanup
G = {}

G[1] = dict(
    kind="cleanup", type="Platinum", phase=5, missable=False, hidden=False,
    count=None, time="Pops last — ~200 h in",
    guide="The platinum is automatic: it lands the moment the other 54 trophies are all "
          "earned, with no multiplayer and no DLC involved. Treat this entry as the "
          "finish line of the roadmap rather than a task of its own — if everything "
          "else in the tracker is ticked, Vice Got a Price! follows on its own.",
    steps=[
        "Work the five roadmap phases in order; the story first, the 100% checklist second.",
        "Keep the one missable, Positive Mental Attitude, protected from Chapter 1 onward.",
        "When the tracker shows 54 of 54, the platinum pops with the last trophy — no extra step.",
    ],
    watchout="Nothing about the platinum itself can be missed, but it inherits the one "
             "missable below it: lose the Chapter 1 meditation and this waits for a second playthrough.",
    sources=["psn", "powerpyx", "gtadb"],
)

G[2] = dict(
    kind="story", type="Story — opening mission", phase=1, missable=False, hidden=True,
    count=None, time="Story · automatic",
    guide="A story trophy for finishing Gone Fishing, the opening mission of Chapter 1. "
          "It cannot be missed and needs no preparation: play the prologue through its "
          "final cutscene and the trophy lands as the mission closes. Use the opener to "
          "learn the basics it teaches — movement, the phone and the WAiNK app — because "
          "the whole roadmap assumes them.",
    steps=[
        "Start the story and play Gone Fishing from the first scene.",
        "Follow the mission markers to the end; there are no branches or fail states that cost the trophy.",
        "The trophy pops as the closing cutscene ends.",
    ],
    watchout="",
    sources=["psn", "powerpyx"],
)

G[3] = dict(
    kind="story", type="Story — chapter", phase=1, missable=False, hidden=True,
    count=None, time="Story · automatic",
    guide="Awarded for completing Chapter 1. Chapter trophies in this list pop a little "
          "late — expect this one shortly after you clear the first mission or two of "
          "Chapter 2, which is normal and not a bug. While you are still in Chapter 1, "
          "do the one thing the whole run depends on: the morning meditation at Jason's "
          "house (see Positive Mental Attitude).",
    steps=[
        "Play Chapter 1's missions in order until the chapter closes.",
        "During Chapter 1, follow Lucia to the balcony at Jason's house and meditate when the moment comes.",
        "Keep playing into Chapter 2; the chapter trophy registers as the next chapter gets going.",
    ],
    watchout="Do not rush out of Chapter 1: the balcony meditation there is the run's only "
             "real missable risk, and it is gone once the chapter ends.",
    sources=["psn", "powerpyx", "sixshore"],
)

G[4] = dict(
    kind="story", type="Story — chapter", phase=1, missable=False, hidden=True,
    count=None, time="Story · automatic",
    guide="Awarded for completing Chapter 2. Like the other chapter trophies it can land "
          "a mission or two into the next chapter. Chapter 2 is when the game opens up: "
          "both Jason and Lucia become playable together, the real-estate app arrives, "
          "and partner trophies such as Hot Together first become possible — but none of "
          "that is required for this trophy, which is pure story progress.",
    steps=[
        "Finish Chapter 2's mission chain.",
        "Optionally, once both characters can roam together, start chipping at partner and world trophies.",
        "The trophy pops as Chapter 3 gets under way.",
    ],
    watchout="",
    sources=["psn", "powerpyx"],
)

G[5] = dict(
    kind="story", type="Story — chapter", phase=1, missable=False, hidden=True,
    count=None, time="Story · automatic",
    guide="Awarded for completing Chapter 3. By now the map, the fences and the dye-pack "
          "jammer story beat are all in play, and several side strands open (Andy's call "
          "comes in Chapter 3, Randy's list and Tyrone's strand start here too). The "
          "trophy itself stays automatic: finish the chapter and it follows, a little "
          "late like the others.",
    steps=[
        "Finish Chapter 3's mission chain.",
        "Pick up the Chapter 3 side strands as they appear — Andy (Lucia), Randy, Tyrone (Jason).",
        "The trophy pops as Chapter 4 gets under way.",
    ],
    watchout="",
    sources=["psn", "powerpyx"],
)

G[6] = dict(
    kind="story", type="Story — chapter", phase=1, missable=False, hidden=True,
    count=None, time="Story · automatic",
    guide="Awarded for completing Chapter 4, the last full chapter before the endgame. "
          "An optional mission in Chapter 4 opens the bank jobs that Maximum Withdrawal "
          "and several money trophies feed on, so take it when it appears. Before you "
          "roll into the final mission, sweep up any meditation spots you still owe — "
          "the checklist later only asks for 15 of 18, but the trophy wants all 18.",
    steps=[
        "Finish Chapter 4's mission chain, including the optional bank-job opener.",
        "Check the meditation counter before accepting the final mission; finish the set if it is short.",
        "The trophy pops as the endgame begins.",
    ],
    watchout="The final mission is the point of no return for tidy routing: bank the "
             "meditation set and a fresh manual save before you take it.",
    sources=["psn", "powerpyx", "sixshore"],
)

G[7] = dict(
    kind="story", type="Story — final mission", phase=1, missable=False, hidden=True,
    count=None, time="Story · automatic",
    guide="The gold for completing the final mission. There is no mission replay in this "
          "game, so treat the finale as a one-way door: save in a fresh manual slot "
          "before you accept it, confirm the meditation counter is complete, then play "
          "it through. Free roam continues after the credits and everything the 100% "
          "checklist needs stays reachable — the story ending locks nothing else away.",
    steps=[
        "Save in a fresh slot before accepting the final mission (15 manual slots exist — use them).",
        "Confirm Positive Mental Attitude is complete, or finish the last spots first.",
        "Play the final mission to its end; the gold pops with the ending.",
        "After the credits, open Progress → Stats: the 100% Completion checklist is now live.",
    ],
    watchout="No mission replay exists, so a pre-finale save is your only way back if a "
             "cleanup idea needs the pre-ending world state.",
    sources=["psn", "powerpyx"],
)

G[8] = dict(
    kind="story", type="Story — named mission", phase=1, missable=False, hidden=True,
    count=None, time="Story · automatic",
    guide="A story trophy for completing Breakfast Run, one of the six named main "
          "missions that carry their own trophy. It is unmissable and purely a matter "
          "of reaching it in the chain: story missions are linear, and this pops on "
          "completion whatever route you took through it.",
    steps=[
        "Follow the main mission chain until Breakfast Run is offered.",
        "Complete the mission; the trophy pops at the mission-complete screen.",
    ],
    watchout="",
    sources=["psn", "sixshore"],
)

G[9] = dict(
    kind="story", type="Story — named mission", phase=1, missable=False, hidden=True,
    count=None, time="Story · automatic",
    guide="A story trophy for completing The Cartel Heist, one of the six named main "
          "missions with their own trophy. Unmissable story progress. Heist-style "
          "missions are also where the game teaches the robbery loop — casing, entry, "
          "escape — that the bank-vault and shop trophies later ask you to repeat in "
          "free roam, so it is worth learning the pattern here where failure is cheap.",
    steps=[
        "Follow the main mission chain until The Cartel Heist is offered.",
        "Complete the mission; the trophy pops at the mission-complete screen.",
    ],
    watchout="",
    sources=["psn", "sixshore"],
)

G[10] = dict(
    kind="story", type="Story — named mission", phase=1, missable=False, hidden=True,
    count=None, time="Story · automatic",
    guide="A story trophy for completing Child's Play, one of the six named main "
          "missions with their own trophy. Unmissable: reach it in the chain and finish "
          "it, and the trophy follows automatically.",
    steps=[
        "Follow the main mission chain until Child's Play is offered.",
        "Complete the mission; the trophy pops at the mission-complete screen.",
    ],
    watchout="",
    sources=["psn", "sixshore"],
)

G[11] = dict(
    kind="story", type="Story — named mission", phase=1, missable=False, hidden=True,
    count=None, time="Story · automatic",
    guide="A story trophy for completing Headliners, one of the six named main missions "
          "with their own trophy. Unmissable story progress — no choices inside the "
          "mission change whether it lands.",
    steps=[
        "Follow the main mission chain until Headliners is offered.",
        "Complete the mission; the trophy pops at the mission-complete screen.",
    ],
    watchout="",
    sources=["psn", "sixshore"],
)

G[12] = dict(
    kind="story", type="Story — named mission", phase=1, missable=False, hidden=True,
    count=None, time="Story · automatic",
    guide="A story trophy for completing VCIA Takedown, one of the six named main "
          "missions with their own trophy. Unmissable. The airport it is named for "
          "matters again later: Catch Me If You Can asks you to steal a passenger jet "
          "from a VCIA gate in free roam, so the layout you learn here is not wasted.",
    steps=[
        "Follow the main mission chain until VCIA Takedown is offered.",
        "Complete the mission; the trophy pops at the mission-complete screen.",
    ],
    watchout="",
    sources=["psn", "sixshore"],
)

G[13] = dict(
    kind="story", type="Story — named mission", phase=1, missable=False, hidden=True,
    count=None, time="Story · automatic",
    guide="A story trophy for completing Operation Savage Glory, one of the six named "
          "main missions with their own trophy. Unmissable story progress, and the "
          "last of the named-mission trophies: after this one, the story list is down "
          "to chapters and the finale.",
    steps=[
        "Follow the main mission chain until Operation Savage Glory is offered.",
        "Complete the mission; the trophy pops at the mission-complete screen.",
    ],
    watchout="",
    sources=["psn", "sixshore"],
)

G[14] = dict(
    kind="cleanup", type="Completion — 100% checklist", phase=2, missable=False, hidden=False,
    count=None, time="The long haul — most of the ~200 h",
    guide="The hardest trophy on the list: attain 100% on the completion checklist that "
          "appears under Progress → Stats → 100% Completion once the story is done. The "
          "checklist is far kinder than its name — closer to 60% of everything the game "
          "tracks. Progress made during the story already counts, and nothing on it is "
          "missable, so this is a marathon of steady sweeping rather than a skill test.",
    steps=[
        "Finish the story; the checklist only becomes visible afterwards.",
        "Bank the fixed quotas: 200 of 277 base vehicles scanned with WAiNK, 100 of 255 animals studied through binoculars, 50 of 66 weapons owned.",
        "Complete the full sets the checklist insists on: every robbery, underwater discovery, shooting-range challenge, drone race and Bret quest.",
        "Reach 70 of the 80 Challenges, 300 stunts, and 15 of the 18 meditation spots (the trophy for the spots wants all 18 anyway).",
        "Take any 100 optional missions along the way — there are several hundred, far more than needed.",
        "When a category sits short, sweep only that category; the stats screen names what is missing.",
    ],
    watchout="Do not grind the checklist before the story ends — it is invisible until "
             "then, and story progress feeds it for free. Cheats disable trophies and "
             "saving, so keep them off this save entirely.",
    sources=["psn", "powerpyx", "sixshore"],
)

G[15] = dict(
    kind="activities", type="Grind — stunts", phase=2, missable=False, hidden=False,
    count=250, time="15–25 h, mostly en route",
    guide="Complete 250 stunts of any kind. The game counts four families — stunt "
          "jumps, flights under bridges, knife flights and base jumps — and tracks far "
          "more of them (397) than the trophy asks for, so you never need the brutal "
          "ones. The 100% checklist later wants 300, so every stunt banked here is "
          "banked twice. The efficient play is opportunistic: whenever a ramp, bridge "
          "or rooftop is on your route, take the stunt instead of driving past it.",
    steps=[
        "Learn the four stunt families early; the stats screen tracks each family's count.",
        "Sweep stunts district by district whenever travel takes you near a cluster.",
        "Save finicky knife flights and base jumps for a dedicated session with a fast plane and a parachute.",
        "At 250 the silver pops; keep going to 300 only if you are chasing the 100% checklist (you are).",
    ],
    watchout="Stunts only register when they are completed cleanly — a crashed landing "
             "does not count, so bail out rather than ride a doomed attempt into the ground.",
    sources=["psn", "powerpyx", "sixshore"],
)

G[16] = dict(
    kind="activities", type="Activities — sampler", phase=3, missable=False, hidden=False,
    count=9, time="1–2 h",
    guide="Try each type of activity once. There are nine types to sample: fishing, "
          "hunting, golf, shooting ranges, pool, basketball, a video game, a race and a "
          "stunt. One attempt at each is enough — no wins, medals or completions are "
          "required — which makes this the cheapest tour of the game's side content and "
          "a good early checklist for learning where everything lives.",
    steps=[
        "Work the nine types in any order: fishing, hunting, golf, shooting range, pool, basketball, video game, race, stunt.",
        "Use map icons to route a single trip that passes several activity types.",
        "The ninth distinct type tried pops the trophy.",
    ],
    watchout="A video game counts as its own type — the TV games at home or an arcade "
             "cabinet both qualify, and Stick Fiddler wants one played to the end anyway.",
    sources=["psn", "powerpyx", "sixshore"],
)

G[17] = dict(
    kind="activities", type="Skill — shooting range golds", phase=2, missable=False, hidden=False,
    count=42, time="6–10 h",
    guide="Earn a gold medal in all 42 Shooting Range challenges — the count PlayStation "
          "itself tracks. Gold is about accuracy streaks rather than raw speed: learn "
          "each challenge's target pattern with a clearing run first, then replay "
          "immediately while the pattern is fresh. Work one weapon class at a time so "
          "the handling carries over, and leave the tightest accuracy challenges for "
          "last, when the range weapons feel familiar. The checklist requires every "
          "range challenge completed as well, so golds close two boxes at once.",
    steps=[
        "Clear every challenge once to learn its targets and medal thresholds.",
        "Replay in weapon-class order, banking golds class by class.",
        "Replay a challenge immediately after a near-miss — the pattern is still in your hands.",
        "Save the tightest accuracy challenges for last; the 42nd gold pops the silver.",
    ],
    watchout="Tilting at one stubborn challenge wastes hours: medals are per-challenge "
             "and nothing is lost by reordering, so move on and come back with fresher aim.",
    sources=["psn", "powerpyx", "psnprofiles"],
)

G[18] = dict(
    kind="activities", type="Racing — drone races", phase=2, missable=False, hidden=False,
    count=14, time="2–3 h",
    guide="Win a Top Fun drone race at every location — 14 locations in all. A win at "
          "each is required, not just a finish, but the races are short and restart "
          "instantly, so the method is repetition: run a course until its line is "
          "memorised, win it, and move on. Drone races are also on the 100% checklist's "
          "must-complete list, so these wins are never wasted effort.",
    steps=[
        "Take each race once at learning pace to see the gate order.",
        "Replay immediately, cutting the corners you now know are safe.",
        "Tick locations off on the map; the 14th location won pops the trophy.",
    ],
    watchout="Only first place counts — a photo-finish second is still a loss, so "
             "restart rather than finishing out a race that has gone wrong.",
    sources=["psn", "powerpyx", "sixshore"],
)

G[19] = dict(
    kind="activities", type="Racing — 20 wins", phase=3, missable=False, hidden=False,
    count=20, time="3–4 h",
    guide="Win 20 different races. The word that matters is “different”: repeating one "
          "easy race 20 times does nothing. Work through the race calendar instead — "
          "each event won is struck off — and favour the shorter street races early, "
          "where the fields are softest. Race wins also feed the Challenges total that "
          "One Last Thing counts, so this grind pulls double duty.",
    steps=[
        "Open the race list and work it top to bottom, one win per event.",
        "Upgrade your daily car's handling before the longer point-to-point events.",
        "The 20th distinct race won pops the trophy.",
    ],
    watchout="Check the counter after each win — if it did not move, that event was "
             "already banked and the win did not count toward the 20.",
    sources=["psn", "powerpyx"],
)

G[20] = dict(
    kind="activities", type="Activities — fishing duel", phase=1, missable=False, hidden=False,
    count=None, time="~30 min once invited",
    guide="Beat Cal in a fishing challenge. Cal is met during Chapter 1, and afterwards "
          "he texts you a fishing spot and the challenge opens. Fishing is a timing "
          "minigame — cast, watch the water, strike on the bite and play the fish in "
          "without snapping the line. You only have to out-catch Cal once; if a round "
          "goes badly, the challenge can simply be taken again.",
    steps=[
        "Meet Cal during Chapter 1's story.",
        "Wait for his text naming the fishing spot, then travel there and accept the challenge.",
        "Out-catch him over the round; the trophy pops on the win.",
    ],
    watchout="Do not ignore the text thread — the challenge is only offered through it, "
             "and it is easy to bury under later messages.",
    sources=["psn", "sixshore"],
)

G[21] = dict(
    kind="activities", type="Activities — video games", phase=3, missable=False, hidden=False,
    count=None, time="~30 min",
    guide="Complete an arcade game — play one of the in-game video games through to the "
          "end. Three run on the TV at home and a fourth waits on arcade machines out "
          "in the world. “Complete” means finishing it, not just starting it, so pick "
          "the shortest game on the TV and see it through in one sitting.",
    steps=[
        "At home, turn on the TV and pick any of its three games (or find an arcade cabinet).",
        "Play it through to its ending screen.",
        "The trophy pops on completion.",
    ],
    watchout="Quitting mid-game banks nothing — this is a completion, not an attempt; "
             "Master of None is the one that only asks you to try.",
    sources=["psn", "sixshore"],
)

G[22] = dict(
    kind="side", type="Strangers — Andy's strand", phase=4, missable=False, hidden=True,
    count=None, time="1–2 h",
    guide="Complete the final mission for Andy. Andy's strand is Lucia-only and starts "
          "with a phone call in Chapter 3; from there it runs as a chain — each job "
          "done puts the next marker on the map — until the final mission closes it. "
          "Strands never expire for trophy purposes: if Andy goes quiet, story "
          "progress or time is usually the gate, and every trophy strand giver returns "
          "after the story and stays.",
    steps=[
        "Answer Andy's call in Chapter 3 (play as Lucia — the strand is hers).",
        "Follow the strand markers job by job, returning after each cooldown.",
        "Finish the strand's final mission; the trophy pops and the strand counts toward Strangers & Freaks.",
    ],
    watchout="Playing as Jason stalls this chain — switch to Lucia when Andy's marker "
             "is the one you are chasing.",
    sources=["psn", "sixshore"],
)

G[23] = dict(
    kind="side", type="Strangers — Kenton's strand", phase=4, missable=False, hidden=True,
    count=None, time="1–2 h",
    guide="Complete the final mission for Kenton. Kenton's strand is a treasure-diving "
          "chain across 7 shipwrecks. He goes quiet after Chapter 1 and returns later "
          "in the story — that silence is scripted, not a missable window, so do not "
          "restart anything over it. Work the wrecks as the strand hands them to you "
          "and close the chain with his final mission.",
    steps=[
        "Start Kenton's strand when he first appears in Chapter 1.",
        "Dive the shipwrecks he names — 7 in total — as each is revealed.",
        "When he resurfaces later in the story, finish the chain and his final mission.",
    ],
    watchout="Kenton's long quiet stretch looks like a failed strand; it is not. His "
             "marker returns, and he stays available after the story.",
    sources=["psn", "sixshore"],
)

G[24] = dict(
    kind="side", type="Strangers — Billy's strand", phase=4, missable=False, hidden=True,
    count=None, time="1–2 h",
    guide="Complete the final mission for Billy. Billy's strand opens in Chapter 2 and "
          "centres on the mud club in Kelly County. Like every strand it is a chain: "
          "do a job, wait for the next marker, repeat, and the final mission ends it "
          "and pays the trophy. It also counts as one of the eight closed strands "
          "Strangers & Freaks is counting.",
    steps=[
        "Pick up Billy's strand when it opens in Chapter 2.",
        "Work the chain of jobs around the Kelly County mud club.",
        "Finish the final mission; the trophy pops.",
    ],
    watchout="",
    sources=["psn", "sixshore"],
)

G[25] = dict(
    kind="side", type="Strangers — 8 strands", phase=4, missable=False, hidden=False,
    count=8, time="8–12 h for the set",
    guide="Complete 8 mission strands for strangers across Leonida. Only some side "
          "questlines count as strands — the named chains (Andy, Kenton, Billy, Randy, "
          "Tyrone, Bret and their peers) are the reliable ones, and the five "
          "single-trophy strands in this guide already give you most of the eight. "
          "Strands are chains, so the discipline is finishing what you start: a "
          "half-done strand counts for nothing until its final mission closes it.",
    steps=[
        "Open every strand you meet while travelling; a started strand shows its next marker on the map.",
        "Finish strands one at a time so chains are not left dangling.",
        "Mind the character locks: Andy is Lucia-only; Tyrone and Bret are Jason-only.",
        "Count closed strands, not started ones — at 8 finished chains the silver pops.",
    ],
    watchout="Strangers & Freaks is not part of the 100% checklist, so it is commonly "
             "the trophy still standing after A Long Road — schedule it, don't assume it.",
    sources=["psn", "powerpyx", "sixshore"],
)

G[26] = dict(
    kind="side", type="Strangers — Randy's strand", phase=4, missable=False, hidden=True,
    count=16, time="2–3 h",
    guide="Complete the final mission for Randy. Randy's strand, open from Chapter 3, "
          "is a wish list of 16 sports cars to find and deliver. The cars are specific "
          "models, so the hunt is the work: learn where each model spawns or parks, "
          "take it cleanly, and deliver it undamaged enough to count. WAiNK-scanning "
          "cars as you travel (for Whip It Good and the checklist) teaches you the "
          "spawn map this strand needs.",
    steps=[
        "Start Randy's strand in Chapter 3 and take the wish list.",
        "Deliver the 16 named sports cars one by one as you find them in the world.",
        "Deliver the last car and finish his final mission; the trophy pops.",
    ],
    watchout="A wrecked delivery can fail the hand-over — once you have a wish-list "
             "car, drive it like it is made of glass.",
    sources=["psn", "sixshore"],
)

G[27] = dict(
    kind="side", type="Strangers — Tyrone's strand", phase=4, missable=False, hidden=True,
    count=None, time="1–2 h",
    guide="Complete the final mission for Tyrone. Tyrone's strand is Jason-only, runs "
          "from Chapter 3, and is about shutting down labs around Vice City. Follow "
          "the chain of lab jobs as Jason until the final mission closes the strand; "
          "it counts toward the eight strands of Strangers & Freaks like the others.",
    steps=[
        "Pick up Tyrone's strand as Jason from Chapter 3.",
        "Work the chain, shutting down each lab the strand names.",
        "Finish the final mission; the trophy pops.",
    ],
    watchout="Lucia cannot advance this chain — if the marker will not trigger, check "
             "which character you are playing.",
    sources=["psn", "sixshore"],
)

G[28] = dict(
    kind="missable", type="MISSABLE — meditation spots", phase=1, missable=True, hidden=False,
    count=18, time="Spread across the story",
    guide="Meditate at every spot across Leonida — 18 spots — and the list's one "
          "genuinely missable trophy. The danger is a single spot: during Chapter 1, "
          "one morning at Jason's house, Lucia says she is going to meditate and walks "
          "out to the balcony. Follow her and accept the optional moment; she shows "
          "you how meditation works. That spot is gone after Chapter 1. Guide writers "
          "disagree on whether it counts toward the 18 — it raises the meditation "
          "counter, but is not marked like the others — so do it anyway: it takes a "
          "minute and removes the only real risk on the list. The remaining spots are "
          "found out in the world as new areas open, and the last of them needs both "
          "characters playable, which only happens from Chapter 2 onward.",
    steps=[
        "Chapter 1, Jason's house: when Lucia heads to the balcony to meditate, follow her and join in. Do not let the chapter end first.",
        "As each new area opens during the story, sweep its meditation spots before pushing on — the tracker counts them here.",
        "Keep a manual save from before the final mission until the counter reads 18.",
        "At 18 spots the trophy pops; note the 100% checklist only asks for 15, so the last 3 are for this trophy alone.",
    ],
    watchout="MISSABLE: the Chapter 1 balcony meditation disappears when Chapter 1 "
             "ends. Everything else on the list can be cleaned up after the story — "
             "this one moment cannot.",
    sources=["psn", "powerpyx", "sixshore"],
)

G[29] = dict(
    kind="side", type="Strangers — Bret's hunt", phase=4, missable=False, hidden=True,
    count=None, time="1–3 h",
    guide="Hunt a unique animal for Bret. Bret's strand is Jason-only and runs from "
          "Chapter 2; he deals in target decks of animals to hunt, and somewhere in "
          "his chain a unique animal is the trophy's trigger. Guide writers have not "
          "pinned down exactly which animal it is — the safe method is thoroughness: "
          "clear Bret's target decks as he issues them, and the unique hunt lands "
          "inside that work. Bret's quests are also mandatory for the 100% checklist, "
          "so none of this effort is wasted either way.",
    steps=[
        "Pick up Bret's strand as Jason from Chapter 2.",
        "Hunt the targets in each deck he issues, studying animals through binoculars as you go (the checklist wants 100 studied).",
        "Keep clearing decks — all 15 of them are needed for 100% — and the unique-animal hunt completes inside the chain.",
    ],
    watchout="Do not stop at the trophy: Bret's full set of decks is on the 100% "
             "checklist, so leaving his chain half-done just postpones the same work.",
    sources=["psn", "sixshore", "powerpyx"],
)

G[30] = dict(
    kind="collectibles", type="Collectibles — card sets", phase=3, missable=False, hidden=False,
    count=3, time="10–15 h",
    guide="Complete 3 collectible card sets. There are 18 sets in the game, so the "
          "trophy asks for any three closed sets, not a specific trio — pick the sets "
          "your travels have already filled most. Cards are grabbed one at a time "
          "across the whole map and the counter never goes down, so every card you "
          "pass during the story is permanent progress. Note the split in demands: "
          "the trophy needs 3 sets, while the 100% checklist is reported to want as "
          "many as 15 — finish three for the silver, and let the checklist decide "
          "whether you keep collecting.",
    steps=[
        "Grab every card you pass during the story — backtracking for singles is the slow way.",
        "After the story, open the collection screen and choose the set nearest completion.",
        "Finish that set, then repeat for two more; the third closed set pops the silver.",
    ],
    watchout="Chasing a “nearly done” set across the map for one last card is the "
             "classic time sink — sweep by district and let sets close as a by-product.",
    sources=["psn", "sixshore", "powerpyx"],
)

G[31] = dict(
    kind="collectibles", type="Collectibles — WAiNK scans", phase=2, missable=False, hidden=False,
    count=100, time="8–12 h, mostly en route",
    guide="WAiNK It at 100 locations: scan 100 spots with the WAiNK phone app. "
          "Landmarks, curiosities and sculptures all count — if it looks like the kind "
          "of thing a tourist would photograph, it probably scans. Build the habit "
          "early: the same app scans vehicles for Whip It Good and the checklist's "
          "200-vehicle quota, so a player who scans everything on sight finishes "
          "this trophy without ever sitting down to grind it.",
    steps=[
        "From Chapter 1, scan every landmark, curiosity and sculpture the app flags.",
        "Scan vehicles with the same habit — the counters share the effort.",
        "If the count stalls late, sweep the dense downtown districts where spots cluster; the 100th scan pops the silver.",
    ],
    watchout="Scannable spots are one-and-done — re-scanning a counted spot adds "
             "nothing, so keep moving rather than re-checking old ground.",
    sources=["psn", "powerpyx", "sixshore"],
)

G[32] = dict(
    kind="activities", type="Grind — challenges", phase=2, missable=False, hidden=False,
    count=50, time="Comes on the way to 100%",
    guide="Complete 50 Challenges. The game holds 80 challenges in eight groups of "
          "ten, and this trophy asks for any 50 of them — you choose which. The 100% "
          "checklist raises the bar to 70, so treat 50 as a milestone on a longer "
          "road rather than a finish line: pick the groups that suit how you play, "
          "bank the easy tens first, and let the last group you touch be the one you "
          "would have skipped.",
    steps=[
        "Open the Challenges screen and clear the groups closest to your play style first.",
        "Track the running total here; at 50 the trophy pops.",
        "Keep going toward 70 only for the checklist — the trophy itself is already yours.",
    ],
    watchout="There is no prize for doing the hardest challenges first: 50 of 80 "
             "means the eight or nine nastiest individual challenges can simply be left.",
    sources=["psn", "powerpyx", "sixshore"],
)

G[33] = dict(
    kind="activities", type="Partner — wanted escape", phase=5, missable=False, hidden=False,
    count=None, time="~15 min once set up",
    guide="Lose a 4-star Wanted Level with your partner and escape the heat. This "
          "needs both characters roaming together, which only opens up in Chapter 2, "
          "and a genuine 4-star heat to lose — bank jobs hand you 4 stars as a matter "
          "of course, so the natural setup is to finish a bank job with your partner "
          "along and then do the escaping properly: break line of sight, swap cars "
          "out of view, and wait out the stars somewhere quiet.",
    steps=[
        "Play until both characters can roam together (Chapter 2 onward).",
        "With your partner along, raise a 4-star wanted level — a bank job does this reliably.",
        "Break pursuit: leave the search area, change vehicles unseen, and hide until the stars clear.",
        "The trophy pops when the heat is fully lost with your partner present.",
    ],
    watchout="Your partner must be with you when the stars clear, not just when they "
             "were raised — keep them in the car for the whole escape.",
    sources=["psn", "sixshore"],
)

G[34] = dict(
    kind="activities", type="Partner — shop chain", phase=5, missable=False, hidden=False,
    count=3, time="~20 min once set up",
    guide="Rob 3 shops back-to-back with your partner without losing your Wanted "
          "Level. The chain is the skill: the wanted level from the first robbery "
          "must still be alive when the third shop is robbed, so the three shops "
          "need to be a short drive apart and the driving between them direct — no "
          "hiding, no waiting out stars. Expect the trophy a few breaths after the "
          "third robbery rather than on the spot; give it about 30 seconds before "
          "you assume it failed.",
    steps=[
        "Choose three shops within a short drive of each other and scout the route first.",
        "Rob the first shop with your partner and leave as the wanted level rises.",
        "Drive straight to the second and third, robbing each before the stars can clear.",
        "Stay wanted until the trophy registers, then lose the heat however you like.",
    ],
    watchout="Losing the wanted level for even a moment between shops breaks the "
             "chain — if the stars start flashing their final warning, commit a small "
             "crime in view of the police to keep the heat alive.",
    sources=["psn", "sixshore", "powerpyx"],
)

G[35] = dict(
    kind="collectibles", type="Collectibles — vehicle discovery", phase=2, missable=False, hidden=False,
    count=100, time="Comes naturally while travelling",
    guide="Discover 100 vehicles. “Discover” is generous: scanning a vehicle with the "
          "WAiNK app is enough — you do not have to drive, own or even enter it. That "
          "makes this a habit trophy. Every new model you pass on the street is a "
          "free tick, and the habit pays triple: the scans also feed You WAiNKer! "
          "and the checklist's 200-of-277 vehicle quota, and they teach you where "
          "Randy's wish-list cars live.",
    steps=[
        "Scan every unfamiliar vehicle model with WAiNK as you travel.",
        "Rich districts and the airport spawn the rarer models — sweep them when passing.",
        "The 100th distinct vehicle discovered pops the trophy.",
    ],
    watchout="Duplicates do not count — the counter tracks distinct models, so a "
             "street full of the same sedan is worth exactly one scan.",
    sources=["psn", "sixshore", "powerpyx"],
)

G[36] = dict(
    kind="cleanup", type="Feat — Combat Focus", phase=5, missable=False, hidden=False,
    count=None, time="~15 min once set up",
    guide="Take down 5 enemies in a single use of Combat Focus. The setup matters "
          "more than the aim: you need five valid targets alive in front of you when "
          "the ability starts, because it does not refill mid-use. Gang members "
          "count as enemies for this; soldiers, police and civilians appear not to. "
          "A gang hangout or an illegal operation with a clustered group is the "
          "reliable stage — soften nobody beforehand, walk in, trigger Combat Focus "
          "and drop five before it runs dry.",
    steps=[
        "Find a gang spot where at least five members stand in the open.",
        "Approach with a full Combat Focus meter and a loaded automatic weapon.",
        "Trigger Combat Focus and take down five gang members inside the one activation.",
    ],
    watchout="Wasting the meter on two or three early targets strands the attempt — "
             "if the group is too small, leave and find a bigger one instead.",
    sources=["psn", "sixshore"],
)

G[37] = dict(
    kind="cleanup", type="Feat — airport jet theft", phase=5, missable=False, hidden=True,
    count=None, time="~15 min",
    guide="Make an unscheduled departure at VCIA: steal a passenger jet docked at a "
          "gate at Vice City International Airport and fly it away — roughly a "
          "kilometre out is what the guides measure. Airport security answers "
          "quickly, so the method is commitment: sprint to a parked jet, get aboard "
          "before the response converges, taxi straight out and climb. The wanted "
          "level does not need to be lost for the trophy, only the departure made.",
    steps=[
        "Enter VCIA and find a passenger jet parked at a gate.",
        "Board it fast, before security pins you on the apron.",
        "Taxi out, take off and put about a kilometre between you and the airport.",
    ],
    watchout="Dawdling on the apron is how this fails — pick the jet nearest a "
             "taxiway so the takeoff roll is short.",
    sources=["psn", "sixshore"],
)

G[38] = dict(
    kind="cleanup", type="Feat — tank theft", phase=5, missable=False, hidden=True,
    count=None, time="~20 min",
    guide="“Kinda hot in these Rhinos” — steal a military tank. Tanks are found at "
          "Mile Zero Air Station in the southwest of the map. A military base means "
          "an instant, heavy response, so go in with a fast approach vehicle, a full "
          "health bar and an exit route already in mind: the trophy is for the theft "
          "itself, and a Rhino is its own getaway vehicle once you are inside it.",
    steps=[
        "Travel to Mile Zero Air Station in the southwest.",
        "Reach a parked tank and climb in under fire.",
        "Drive it out of the base; the trophy pops on the theft.",
    ],
    watchout="Approach on foot from the fence line rather than driving in — a car "
             "stops at the gate; a runner sometimes does not.",
    sources=["psn", "sixshore"],
)

G[39] = dict(
    kind="cleanup", type="Crime — stealth robbery", phase=5, missable=False, hidden=False,
    count=None, time="~20 min once equipped",
    guide="Rob a jewelry store without being detected. The tool for the job is the "
          "Snap Gun, which a Chapter 3 main mission hands you — before that, this "
          "trophy is simply not available, so do not waste attempts on it early. "
          "With the Snap Gun in hand the robbery is a quiet one: enter calm, disable "
          "the store's ability to raise the alarm, take the goods and walk out "
          "before anyone knows it happened. Detection at any point voids the run, "
          "not the trophy — leave, let the area cool, and try again.",
    steps=[
        "Progress the story until the Chapter 3 mission gives you the Snap Gun.",
        "Pick a jewelry store and enter without drawing attention.",
        "Rob it using the Snap Gun approach and leave undetected; the trophy pops on the clean getaway.",
    ],
    watchout="Any detection — a raised alarm, a witness call, a wanted star — voids "
             "the attempt. If it goes loud, abandon the run instead of finishing it.",
    sources=["psn", "sixshore"],
)

G[40] = dict(
    kind="cleanup", type="Crime — bank vaults", phase=2, missable=False, hidden=False,
    count=5, time="3–5 h",
    guide="Rob 5 bank vaults and escape. Bank jobs open through an optional mission "
          "in Chapter 4; there are 8 banks in all, and the trophy needs any 5 "
          "robbed with a clean escape after each. The shape of a job is consistent: "
          "case the vault and the exits, stage the getaway car before you go in, "
          "rob fast, and lose the wanted level completely — an escape only counts "
          "when the heat is gone. Bank jobs are also the best late-game money "
          "(Treat Yo Self and Little Boxes send their regards) and they reliably "
          "raise the 4-star heat that Hot Together wants, so these robberies are "
          "the engine room of the whole cleanup phase. The checklist, note, wants "
          "all 8 banks eventually.",
    steps=[
        "Take the Chapter 4 optional mission that opens bank jobs.",
        "Case a bank: vault, exits, and where the getaway car waits.",
        "Rob the vault, leave immediately, and lose the wanted level completely.",
        "Repeat at four more banks; the fifth clean escape pops the silver.",
    ],
    watchout="An escape that ends in arrest or death banks nothing — when a job "
             "goes wrong early, cut your losses and restart the robbery rather "
             "than the count.",
    sources=["psn", "sixshore", "powerpyx"],
)

G[41] = dict(
    kind="cleanup", type="Crime — armored truck", phase=5, missable=False, hidden=False,
    count=None, time="~15 min",
    guide="Rob an armored truck and escape. Two reliable routes: the first bank job "
          "counts on its own, so most players earn this without trying; if you want "
          "it earlier, an armored truck's back doors can be blown open with a sticky "
          "bomb out in free roam. Either way the shape is the same — open the truck, "
          "take the money, and lose the wanted level that follows.",
    steps=[
        "Either play the first bank job, or find an armored truck in traffic.",
        "Open it — the job does it for you; in free roam, a sticky bomb on the rear doors works.",
        "Take the cash and escape the heat; the trophy pops once you are clear.",
    ],
    watchout="In free roam the truck keeps driving while you set up — block it with "
             "your own vehicle first so the bomb run is not a chase.",
    sources=["psn", "sixshore"],
)

G[42] = dict(
    kind="collectibles", type="Exploration — full map", phase=2, missable=False, hidden=False,
    count=None, time="2–3 h",
    guide="Explore all of Leonida: clear the fog from the entire map. Every district "
          "you physically visit lifts its fog permanently, and most of the map "
          "clears itself during the story and the strand work. What remains is "
          "usually coastline, islands and the empty corners — and for those, a plane "
          "is fastest by a wide margin: one slow lap of the state at altitude "
          "finishes what weeks of driving would miss.",
    steps=[
        "Let story and side work clear the mainland as you go.",
        "Check the map for surviving fog patches — they cluster on coasts and islands.",
        "Take a plane and sweep the remaining patches in one flight; the trophy pops at full coverage.",
    ],
    watchout="Fog clears where you have actually been, not where you have looked — "
             "a distant island seen through binoculars is still fog until you land on it.",
    sources=["psn", "sixshore"],
)

G[43] = dict(
    kind="cleanup", type="Crime — gang operations", phase=2, missable=False, hidden=False,
    count=9, time="4–6 h for the trophy; more for all 39",
    guide="Rob an illegal operation belonging to each gang — 9 gangs, one operation "
          "robbed from each. The operations are marked businesses of the gangs "
          "across the state, and robbing one is a short, loud job: get in, take "
          "what is valuable, get out. Variety is the whole requirement, so track "
          "which gangs you have hit rather than how many operations — nine "
          "robberies of the same gang count once. The 100% checklist wants every "
          "one of the 39 operations eventually, so a completionist will pass this "
          "trophy on the way; the bowling-alley operation in Port Gellhorn also "
          "carries Let's Go Bowling, so rob that one properly when you reach it.",
    steps=[
        "Open the map and list one operation per gang — 9 gangs in total.",
        "Rob one operation from each, ticking gangs off as you go.",
        "The ninth gang's first robbed operation pops the trophy.",
    ],
    watchout="Repeat robberies of an already-hit gang add money, not progress — if "
             "the counter stalls, you have been robbing family businesses.",
    sources=["psn", "sixshore"],
)

G[44] = dict(
    kind="cleanup", type="Hidden feat — Ocean Beach", phase=5, missable=False, hidden=True,
    count=None, time="~10 min",
    guide="“Enjoy a cocktail with a view on Ocean Beach.” A hidden one-off feat: the "
          "description is the whole instruction — be on Ocean Beach, with a cocktail, "
          "somewhere with a view. Guide writers list the exact trigger as still "
          "unconfirmed, so treat this as an experiment with a strong hint: buy or "
          "take a cocktail at a beachfront spot on Ocean Beach and linger somewhere "
          "scenic rather than drinking on the move. It costs a few dollars and a "
          "minute to try, and it is the kind of trophy that pops while you are "
          "testing it.",
    steps=[
        "Travel to Ocean Beach, the beachfront strip of Vice City.",
        "Get a cocktail from a beachfront bar or stand.",
        "Drink it somewhere with a view over the water; the trophy should pop on the spot.",
    ],
    watchout="Marked unconfirmed by the guide writers at the time of writing — if "
             "the beachfront attempt fails, try the rooftop and pier spots along "
             "the same strip before concluding anything.",
    sources=["psn", "sixshore"],
)

G[45] = dict(
    kind="cleanup", type="Hidden feat — showroom escape", phase=5, missable=False, hidden=True,
    count=None, time="~10 min",
    guide="“Smash your way out of a vehicle showroom in classic style.” A hidden "
          "feat in the series' oldest tradition: get inside a vehicle showroom, "
          "take one of its cars, and leave through the glass rather than the door. "
          "The exact trigger is listed as unconfirmed by guide writers, but the "
          "description leaves little room for doubt about the shape of it — car, "
          "showroom, window, out.",
    steps=[
        "Find a vehicle showroom with display cars inside.",
        "Get in one of the display cars.",
        "Drive it straight out through the showroom glass; the trophy pops on the exit.",
    ],
    watchout="Leaving by the door, however fast, is just theft — the smash through "
             "the glass is the trophy.",
    sources=["psn", "sixshore"],
)

G[46] = dict(
    kind="activities", type="Crime — bowling operation", phase=4, missable=False, hidden=True,
    count=None, time="~20 min",
    guide="“Follow-through at the Kolt & Associates' bowling alley”: take all 3 key "
          "valuables from the Kingpin Bowling gang operation in Port Gellhorn. "
          "This is a robbery with a checklist inside it — the operation holds three "
          "key valuables, and all three must leave with you in the one job. The "
          "robbery returns later if it goes wrong, so it is not missable; and "
          "because the operation belongs to a gang, a thorough job here also counts "
          "toward Pest Control.",
    steps=[
        "Travel to the Kingpin Bowling operation in Port Gellhorn.",
        "Rob it thoroughly, hunting down all 3 key valuables before you leave.",
        "Escape with all three; the trophy pops on the completed robbery.",
    ],
    watchout="Leaving with two of the three valuables is the standard failure — "
             "sweep the back rooms before you run, not after.",
    sources=["psn", "sixshore"],
)

G[47] = dict(
    kind="cleanup", type="Grind — strength", phase=5, missable=False, hidden=True,
    count=None, time="Comes naturally; a few gym sessions to finish",
    guide="“A partnership with mass appeal”: max out strength on both Jason and "
          "Lucia. Strength rises as you work out and fight, and working out "
          "together builds both characters at once, which is the efficient route: "
          "take your partner to the gym or the beach workout spots and train as a "
          "pair. It comes naturally across a 200-hour run for most players; if one "
          "character lags at the end, a few focused sessions close the gap.",
    steps=[
        "Use gyms and workout spots with your partner along so both characters progress.",
        "Check each character's strength stat; train whichever one lags.",
        "When both sit at maximum, the trophy pops.",
    ],
    watchout="Solo training only builds the character you are playing — the "
             "partnership in the description is the method, not a flavour line.",
    sources=["psn", "sixshore"],
)

G[48] = dict(
    kind="cleanup", type="Grind — criminal profile", phase=5, missable=False, hidden=True,
    count=500, time="Comes naturally across the run",
    guide="“Choices made (for better or worse)”: do 500 things that change your "
          "criminal profile. Robberies, escapes, thefts and general mayhem all "
          "nudge the profile, and across a full platinum run this totals itself "
          "without a single dedicated minute — guide writers describe it as a "
          "trophy that simply arrives. Turn on criminal-profile notifications in "
          "the UI settings if you want to watch it climb. One caution from the "
          "guides, unrelated to the count: the Irredeemable profile tier is "
          "permanent once reached and makes police more aggressive, which makes "
          "later cleanup harder — you can still earn everything, just under more "
          "heat.",
    steps=[
        "Play normally — crimes, robberies and escapes all count.",
        "Optionally enable profile notifications in UI settings to watch the total.",
        "The 500th profile-changing act pops the trophy.",
    ],
    watchout="Nothing here can be missed, but a permanently Irredeemable profile "
             "makes the police fiercer for the rest of the run — a cost, not a lock.",
    sources=["psn", "sixshore", "powerpyx"],
)

G[49] = dict(
    kind="cleanup", type="Hidden feat — unconfirmed", phase=5, missable=False, hidden=True,
    count=None, time="Unknown — see the note",
    guide="“Second time's the charm.” The most mysterious line on the list: at the "
          "time of writing, guide writers list this trophy's trigger as not yet "
          "confirmed, with a suspected link to a Payday Loans store. Honesty is "
          "the guide here: nobody reputable has published a verified method yet. "
          "The working theory to test is a repeat visit — do something at a Payday "
          "Loans store, then do it a second time, matching the description's "
          "“second time”. If you crack it, you are ahead of the published guides; "
          "if not, leave it for the cleanup phase and check the sources below for "
          "updates — this entry will be revised as a confirmed method appears.",
    steps=[
        "Find a Payday Loans store in the world.",
        "Interact with it — borrow or rob — then repeat the same act a second time.",
        "If the trophy does not pop, leave it and re-check the cited guides for a confirmed method.",
    ],
    watchout="Do not burn hours on this one early: it is a five-minute experiment "
             "or a later lookup, not a grind, and it blocks nothing else.",
    sources=["psn", "sixshore"],
)

G[50] = dict(
    kind="cleanup", type="Hidden feat — unconfirmed", phase=5, missable=False, hidden=True,
    count=None, time="Unknown — see the note",
    guide="“What the hell just happened?” Guide writers list this trigger as not "
          "yet confirmed, with a suspected UFO questline behind it — a strange-"
          "sighting chain somewhere in the state. Like Bad Luck, I Guess, the "
          "honest guide is a pointer, not a recipe: keep an eye out for odd "
          "lights, odd people and odd rumours as you clear the map (The Goodtime "
          "State's full sweep passes most of the state's strange corners), and "
          "follow any sighting chain you find to its end. Check the cited guides "
          "for a confirmed route before dedicating a session to it.",
    steps=[
        "While exploring, follow up any UFO or strange-sighting rumours and markers.",
        "See any sighting chain through to its conclusion.",
        "Re-check the cited guides for a confirmed method before grinding this one.",
    ],
    watchout="Unconfirmed at the time of writing — schedule it late, when the "
             "published guides have had time to catch up.",
    sources=["psn", "sixshore"],
)

G[51] = dict(
    kind="activities", type="Feat — vehicle melee", phase=4, missable=False, hidden=True,
    count=None, time="~10 min once set up",
    guide="“Bowl 'em over with a melee drive-by.” The in-game hint points at a "
          "melee attack delivered from a moving vehicle, and the leading theory "
          "among guide writers is a kick from a motorcycle: ride alongside a "
          "pedestrian or rival and strike them from the bike at speed. Set it up "
          "somewhere quiet with a lone target, match their pace, and swing as you "
          "pass — the contact has to be a melee hit from the vehicle, not a "
          "collision.",
    steps=[
        "Take a motorcycle to a quiet road with pedestrians or a lone rider.",
        "Ride alongside a target at matched speed.",
        "Land a melee strike from the bike as you pass; the trophy pops on the hit.",
    ],
    watchout="Running the target over does not count — that is a collision, and "
             "the trophy wants the melee swing itself to connect.",
    sources=["psn", "sixshore"],
)

G[52] = dict(
    kind="cleanup", type="Money — laundering", phase=5, missable=False, hidden=False,
    count=250000, countStep=5000, countPrefix="$", time="Accumulates across robberies",
    guide="Earn $250,000 laundering Marked Bills through your contacts. Marked "
          "bills come from robberies, and fences turn them into clean money at a "
          "rate — the total is cumulative across the whole run, so this is less a "
          "task than a habit: always fence marked bills rather than sitting on "
          "them. The dye-pack jammer, unlocked in a Chapter 3 main mission, makes "
          "marked bills far more common from then on, which is when this counter "
          "starts to move quickly. Bank vaults are the richest source late-game.",
    steps=[
        "Rob as normal; pick up marked bills whenever a job pays them out.",
        "After the Chapter 3 mission unlocks the dye-pack jammer, prioritise jobs that pay marked bills.",
        "Fence every batch through your contacts; the $250,000 cumulative total pops the trophy.",
    ],
    watchout="Marked bills in your pocket are worth nothing to this counter — "
             "only laundered money counts, so fence early and often.",
    sources=["psn", "sixshore", "powerpyx"],
)

G[53] = dict(
    kind="cleanup", type="Money — spending", phase=5, missable=False, hidden=False,
    count=100000, countStep=5000, countPrefix="$", time="Accumulates across the run",
    guide="Spend $100,000 across all shops. Any shop counts — guns, car mods and "
          "tattoos move the total fastest — and the spending is money a platinum "
          "run spends anyway: garages alone want $160,000, and a garage is bought "
          "through a shop-like flow you will be using for Little Boxes. If this "
          "counter is somehow short at the end, the fix is pleasant: buy the "
          "best weapons and the fullest car upgrades you have been putting off.",
    steps=[
        "Spend normally on weapons, vehicle mods, clothes and tattoos as you play.",
        "Buy the garages for Little Boxes; the run's spending usually passes $100,000 on its own.",
        "If short late, top up with high-end weapon and car purchases; the cumulative total pops the trophy.",
    ],
    watchout="Only shop spending counts — property and fines do not move it, so "
             "check the counter before assuming the garages finished it.",
    sources=["psn", "sixshore"],
)

G[54] = dict(
    kind="cleanup", type="Money — garages", phase=5, missable=False, hidden=False,
    count=8, time="~1 h, once you hold ~$160,000",
    guide="Purchase all garage properties — 8 purchasable garages, about $160,000 "
          "in total. The real-estate app that sells them arrives in Chapter 2, so "
          "the only real requirement is the money, and bank vaults are the "
          "late-game earner the guides point at. Garages are not just a purchase "
          "trophy: the storage they provide is what On the Spot needs to register "
          "10 vehicles, so buy early rather than last if you can afford it.",
    steps=[
        "Unlock the real-estate app (Chapter 2) and list the 8 garages.",
        "Build the ~$160,000 asking total — bank vaults are the fastest source.",
        "Buy all 8; the eighth purchase pops the trophy.",
    ],
    watchout="Buying garages one at a time as cash allows is fine — nothing about "
             "this trophy expires or scales with story progress.",
    sources=["psn", "sixshore", "powerpyx"],
)

G[55] = dict(
    kind="collectibles", type="Collectibles — Scooter Bros", phase=3, missable=False, hidden=False,
    count=10, time="1–2 h, after garages",
    guide="Register 10 vehicles to the Scooter Bros app. Registration needs "
          "somewhere to keep the cars, so this trophy pairs with Little Boxes: "
          "garage space first, registrations second. Any 10 vehicles count — "
          "take cars you actually like off the street, register them in the app, "
          "and the set builds quickly. Scanning for Whip It Good will already "
          "have shown you where the interesting models spawn.",
    steps=[
        "Buy garage space (Little Boxes) so registered cars have somewhere to live.",
        "Take 10 vehicles you want to keep and register each in the Scooter Bros app.",
        "The 10th registration pops the trophy.",
    ],
    watchout="Without garage space the app has nowhere to put a registration — "
             "if the option is greyed out, the garages are the missing step.",
    sources=["psn", "sixshore"],
)

# ---------------------------------------------------------------------------
# Roadmap, missables briefing and about text (this entry's own words).

ROADMAP = [
    dict(
        phase=1, title="Story first — and protect the one missable",
        hours="60–80 hours",
        text="Play the five chapters from Gone Fishing to the final mission. Story "
             "trophies (12 of them, all hidden) cannot be missed, but one moment "
             "can: in Chapter 1, follow Lucia to the balcony at Jason's house and "
             "meditate. Along the way, build the two habits that pay for the whole "
             "run — scan every new vehicle with WAiNK, and study new animals "
             "through the binoculars. Keep a manual save at the start and end of "
             "each chapter; there is no mission replay.",
    ),
    dict(
        phase=2, title="The 100% engine",
        hours="~100 hours",
        text="After the credits, Progress → Stats holds the 100% Completion "
             "checklist — the real platinum. Work its fixed quotas: 200 of 277 "
             "vehicles scanned, 100 of 255 animals studied, 70 of 80 challenges, "
             "300 stunts, every shooting-range challenge gold, every drone race, "
             "every robbery and Bret's full decks. A Long Road pops when the "
             "checklist does, and most grind trophies fall inside this phase.",
    ),
    dict(
        phase=3, title="Collectibles and the world counters",
        hours="15–20 hours",
        text="Close the three card sets the trophy asks for, finish the WAiNK "
             "scans and the 100 discovered vehicles (both should be nearly done "
             "from Phase 1 habits), clear the last fog off the map with a plane, "
             "and register 10 vehicles to Scooter Bros once the garages are "
             "bought. District-by-district sweeps, never single-item trips.",
    ),
    dict(
        phase=4, title="Strangers and side strands",
        hours="~10 hours",
        text="Finish the named strands — Andy (Lucia only), Kenton, Billy, Randy, "
             "Tyrone (Jason only) and Bret — until 8 strands are closed for "
             "Strangers & Freaks. Strand givers who go quiet always come back "
             "after the story, so nothing here can be lost; it is simply last "
             "because the checklist never asks for it.",
    ),
    dict(
        phase=5, title="Crime, money and the one-off feats",
        hours="10–15 hours",
        text="Spend and launder your way through the money trophies, rob the "
             "last bank vaults and gang operations, buy the 8 garages, and pick "
             "off the hidden one-off feats — a jet from VCIA, a tank from Mile "
             "Zero, a cocktail on Ocean Beach. When the 54th trophy lands, Vice "
             "Got a Price! follows on its own.",
    ),
]

ABOUT = (
    "Leonida Legend is an offline guide and progress tracker for all 55 "
    "PlayStation 5 trophies of Grand Theft Auto VI. Every trophy carries a "
    "guide written for this app — what to do, in what order, what it costs in "
    "time, and what can go wrong — and every guide names its sources beside "
    "the text: the official PlayStation trophy list for the names, "
    "descriptions, grades and tracked counts, cross-checked against the "
    "PSNProfiles and Exophase listings, with methods drawn from the published "
    "guides cited per trophy. Difficulty and time figures on the roadmap are "
    "PowerPyx's published estimates (4/10, about 200 hours), and where the "
    "guide writers have not confirmed a method yet, the guide says so instead "
    "of guessing."
)

MISSABLE_NOTE = (
    "One trophy on this list can be missed: Positive Mental Attitude. A single "
    "meditation — Lucia's, on the balcony at Jason's house during Chapter 1 — "
    "disappears when the chapter ends, and guide writers cannot yet confirm "
    "whether the trophy's 18 spots can be completed without it. Do it when it "
    "comes up: it takes a minute, and it is the only moment on the list that "
    "cannot be cleaned up later. Everything else that looks missable is not: "
    "strand givers return after the story, the bowling operation can be "
    "robbed again, and free roam continues after the credits."
)

# ---------------------------------------------------------------------------

def main():
    official = json.loads(OFFICIAL.read_text(encoding="utf-8"))
    trophies = []
    for item in official["trophies"]:
        g = G[item["id"]]
        entry = {
            "id": item["id"],
            "name": item["name"],
            "description": item["description"],
            "grade": item["grade"],
            "kind": g["kind"],
            "type": g["type"],
            "phase": g["phase"],
            "missable": g["missable"],
            "hidden": g["hidden"],
            "guide": g["guide"],
            "steps": g["steps"],
            "watchout": g["watchout"],
            "time": g["time"],
            "sources": [SOURCES[k] for k in g["sources"]],
        }
        if g.get("count"):
            entry["count"] = g["count"]
            entry["countStep"] = g.get("countStep", 1)
            if g.get("countPrefix"):
                entry["countPrefix"] = g["countPrefix"]
        trophies.append(entry)

    doc = {
        "game": official["game"],
        "platform": official["platform"],
        "list": official["list"],
        "about": ABOUT,
        "missableNote": MISSABLE_NOTE,
        "roadmap": ROADMAP,
        "trophies": trophies,
    }
    OUT.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT} with {len(trophies)} trophies")


if __name__ == "__main__":
    main()
