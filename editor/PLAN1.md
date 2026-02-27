# Plan: editor/PLAN1 — Three Exercise Improvements

## Context

Three targeted improvements to the editor's exercise generation and preview flow:
1. **audio_link persistence**: When saving exercises, the `audio_link` field is never populated because it's not fetched during exercise generation and not included in the INSERT.
2. **Deduplicate identical sentences**: When two sentences share the same text AND translation, both are currently kept. Only one should be saved (randomly chosen).
3. **Suppress spurious duplicate warnings**: The frontend flags any exercises sharing the same `toSentenceId` as duplicates — even across different exercise types (e.g. `sentence_single_choice` + `identify_words_in_speech` generated from the same sentence). Only same-type duplicates should warn.

---

## Files to Modify

| File | Change |
|------|--------|
| `editor/server/src/routers/generate.py` | Fetch audio_link during generation; deduplicate same-text+translation sentences; fix backend `is_duplicate` to be type-aware |
| `editor/server/src/models/generate.py` | Add `audio_link: str = ''` to `GeneratedExercisePreview` |
| `editor/ui/lib/services/course_generation_service.dart` | Add `audioLink` to `GeneratedExercisePreview`; pass it in `saveLesson` JSON body |
| `editor/ui/lib/screens/module_preview_screen.dart` | Fix `_computeDuplicates()` and `_buildExerciseRow` to be type-aware |

---

## Progress

- [x] Step 1: `audio_link` added to `GeneratedExercisePreview` in `editor/server/src/models/generate.py`
- [x] Step 2: `_get_audio_link` helper added to `generate.py`; audio fetched in both `questions_for_sentences` and `module_exercises`
- [x] Step 3: `audio_link` included in `save_lesson` INSERT
- [x] Step 4: Deduplication added to `module_exercises` and `questions_for_sentences`
- [x] Steps 6–7: Flutter `GeneratedExercisePreview` model + `saveLesson` updated with `audioLink`
- [x] Step 8: Flutter duplicate detection made type-aware (`Set<String>` composite key)

---

## Implementation Steps

### 1. Add `audio_link` to `GeneratedExercisePreview` (Backend Model)

**File:** `editor/server/src/models/generate.py`

Add `audio_link: str = ''` to the `GeneratedExercisePreview` class.

---

### 2. Fetch Audio Link During Exercise Generation (Backend)

**File:** `editor/server/src/routers/generate.py`

Add a local async helper at the top of the file (reuse the pattern from `create_course_from_file.py`):

```python
async def _get_audio_link(lang: str, sentence_id: int) -> str:
    sql = "SELECT recording FROM content_raw.audio WHERE lang = %s AND id = %s ORDER BY audio_engine LIMIT 1"
    rows = await get_query_results(sql, (lang, sentence_id))
    return rows[0]['recording'] if rows else ''
```

In both `module_exercises` and `questions_for_sentences`, after building each `GeneratedExercisePreview`, fetch and set `audio_link`:

```python
audio_link = await _get_audio_link(request.lang, s_id)
exercises.append(GeneratedExercisePreview(
    ...,
    audio_link=audio_link,
))
```

---

### 3. Include `audio_link` in the `save_lesson` INSERT

**File:** `editor/server/src/routers/generate.py` — `save_lesson()`

Update the SQL and parameters to include `audio_link`:

```sql
INSERT INTO content.exercise (course_id, module_id, lesson_id, lang, to_lang, exercise_type,
sentence_id, sentence, correct_options, to_sentence_id, wrong_options, audio_link)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
```

Add `ex.audio_link` to the params tuple.

---

### 4. Deduplicate Same-Text+Translation Sentences (Backend)

**File:** `editor/server/src/routers/generate.py` — `module_exercises()`

After fetching `rows` for each word, deduplicate by `(sentence_text, to_text)` before building exercises. When duplicates exist, pick one randomly:

```python
# Deduplicate rows by (sentence_text, to_text), picking one randomly
seen_text_pairs: dict[tuple[str, str], dict] = {}
for r in rows:
    key = (r.get("sentence") or "", r.get("translation") or "")
    if key not in seen_text_pairs or random.random() < 0.5:
        seen_text_pairs[key] = r
deduped_rows = list(seen_text_pairs.values())
```

Then iterate over `deduped_rows` instead of `rows`.

In `questions_for_sentences`, track `seen_text_pairs: set[tuple[str, str]]` and skip any pair already seen.

---

### 5. Fix Backend `is_duplicate` to Be Type-Aware (Backend)

**File:** `editor/server/src/routers/generate.py` — `module_exercises()`

The `to_id_counts` already only counts `sentence_single_choice` exercises, so the existing logic is already type-aware. No change needed here.

---

### 6. Update Flutter `GeneratedExercisePreview` Model

**File:** `editor/ui/lib/services/course_generation_service.dart`

Add `audioLink` field:
```dart
final String audioLink;
// in constructor: this.audioLink = '',
// in fromJson: audioLink: json['audio_link'] ?? '',
```

---

### 7. Pass `audio_link` in `saveLesson` Request Body

**File:** `editor/ui/lib/services/course_generation_service.dart` — `saveLesson()`

Add to the exercises map:
```dart
'audio_link': e.audioLink,
```

---

### 8. Fix Duplicate Detection to Be Type-Aware (Flutter)

**File:** `editor/ui/lib/screens/module_preview_screen.dart`

Change `_duplicateToIds` from `Set<int>` to `Set<String>` (composite key `"$toSentenceId|$exerciseType"`).

Update `_computeDuplicates()`:
```dart
Set<String> _computeDuplicates() {
  final counts = <String, int>{};
  for (final we in widget.wordExercises) {
    for (final ex in we.exercises) {
      if (ex.toSentenceId > 0) {
        final key = '${ex.toSentenceId}|${ex.exerciseType}';
        counts[key] = (counts[key] ?? 0) + 1;
      }
    }
  }
  return counts.entries.where((e) => e.value > 1).map((e) => e.key).toSet();
}
```

Update `_duplicateCount` getter and `_buildExerciseRow` isDup check to use the composite key.

---

## Verification

1. **audio_link**: Generate exercises via the editor, save a module, then query `SELECT audio_link FROM content.exercise LIMIT 10` — should show non-empty values for sentences that have audio.
2. **Deduplication**: Use a word that has multiple sentences with identical text+translation in the DB; confirm only one appears in the preview.
3. **Duplicate warning**: Generate a module with words that share the same sentence — verify the orange warning only appears when the same exercise TYPE is duplicated, not when `sentence_single_choice` and `identify_words_in_speech` share a translation.
