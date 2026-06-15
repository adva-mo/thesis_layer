# ElevenLabs Pronunciation Dictionary

Entries managed manually in EL Studio. Never add via API.

When a word sounds wrong after VO generation: get IPA from the agent → add alias in EL Studio → update `EL_PRONUNCIATION_DICT_VERSION_ID` in `.env` → regenerate.

Failed attempts are logged here upon user confirmation — so we don't retry broken forms.

---

## Current entries

| Word | Type | Active | Tried & failed |
|------|------|--------|----------------|
| מוכרים | Alias | `/moχʁim/` | `mokhreem` (plain English — didn't sound right), `/moxɣim/` (wrong x variant), `/moχɹim/` (wrong r variant) |
| קהילה | Alias | `kehila` | `/kəhi'la/` (IPA — unpredictable), — |
| דירהאם | Alias | `DIRham` | `/ˈdirhɑm/` (sounded like "dira" + m attached to next word), `/dir.hɑm/` (sounded like "dirhum"), `/dir.hæm/` (æ not supported), `/dirham/` (IPA — slash read literally), `dirham` (short "i" → sounded wrong), `deerham` (caused word to be skipped entirely) |
| הקהילה | Alias | `hake'hila` | `/hakəhiˈla/` (schwa over-pronounced → "hak-hila"), `/hakhiˈla/` (no vowel between k and h), `/ha.ke.hi'la/` (dots caused EL to read only last segment → "hila"), `/hakehila/` (IPA — slash read literally), `hakehila` (internal h voiced as "j" → "hakejila"), `hakeila` (not tested — skipped) |
| לך | Alias | `/leχa/` | `leha` (plain English — EL read slashes literally), `lex` (IPA — x read as English "ks" → "leksa") |

---

## Notes

- EL reads `/` slashes literally — plain English entries must be written without them.
- EL does not support syllable dot `.` or `æ` in IPA.
- `הקהילה` and `קהילה` need separate entries — EL treats prefixed forms as different tokens.
- Plain English is more predictable for standard sounds; IPA kept only where precise phonetics are needed (e.g. מוכרים guttural).
