// Progress store for Leonida Legend.
//
// Everything the tracker remembers — which trophies are earned, the counter
// value of every counted trophy, and the spoiler-shield setting — lives in
// one localStorage record on the reader's own machine. Nothing is sent
// anywhere. The record can be exported to a JSON file and imported back on
// another browser, and reset to a blank run.

const STORAGE_KEY = "leonida-legend-progress-v1";

function blankState() {
  return { earned: [], counters: {}, spoilers: false };
}

function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return blankState();
    const parsed = JSON.parse(raw);
    return {
      earned: Array.isArray(parsed.earned) ? parsed.earned : [],
      counters: parsed.counters && typeof parsed.counters === "object" ? parsed.counters : {},
      spoilers: Boolean(parsed.spoilers),
    };
  } catch {
    return blankState();
  }
}

export function createStore(onChange) {
  let state = loadState();

  function save() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    } catch {
      // Storage can be unavailable (private mode); the tracker still works
      // for the session, it just cannot remember between visits.
    }
    onChange(state);
  }

  return {
    get state() {
      return state;
    },
    isEarned(id) {
      return state.earned.includes(id);
    },
    setEarned(id, earned, trophiesById) {
      const has = state.earned.includes(id);
      if (earned && !has) state.earned.push(id);
      if (!earned && has) state.earned = state.earned.filter((x) => x !== id);
      // Un-earning a counted trophy pulls its counter back below the target
      // so the two never disagree.
      const trophy = trophiesById.get(id);
      if (!earned && trophy && trophy.count && (state.counters[id] ?? 0) >= trophy.count) {
        state.counters[id] = trophy.count - 1;
      }
      save();
    },
    counterOf(id) {
      return state.counters[id] ?? 0;
    },
    setCounter(id, value, trophiesById) {
      const trophy = trophiesById.get(id);
      const clean = Math.max(0, Math.floor(Number(value) || 0));
      state.counters[id] = clean;
      // A counter that reaches its target earns the trophy on its own.
      if (trophy && trophy.count) {
        const has = state.earned.includes(id);
        if (clean >= trophy.count && !has) state.earned.push(id);
        if (clean < trophy.count && has) state.earned = state.earned.filter((x) => x !== id);
      }
      save();
    },
    setSpoilers(on) {
      state.spoilers = Boolean(on);
      save();
    },
    exportJson() {
      return JSON.stringify(
        { app: "leonida-legend", version: 1, earned: state.earned, counters: state.counters, spoilers: state.spoilers },
        null,
        2,
      );
    },
    importJson(text) {
      const parsed = JSON.parse(text);
      if (!parsed || !Array.isArray(parsed.earned)) throw new Error("not a Leonida Legend export");
      state = {
        earned: parsed.earned.filter((x) => Number.isInteger(x)),
        counters: parsed.counters && typeof parsed.counters === "object" ? parsed.counters : {},
        spoilers: Boolean(parsed.spoilers),
      };
      save();
    },
    reset() {
      state = blankState();
      save();
    },
  };
}
