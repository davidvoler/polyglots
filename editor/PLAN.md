# Editor Development Plan

**Status:** Backend mostly complete. Service layer (Flutter) mostly complete. UI gap is the main blocker.

**Goal:** A working end-to-end course creation flow — from language selection to a saved, reviewable course.

---

## Current State Summary

### ✅ Backend (Python/FastAPI) — Ready
| Endpoint | Purpose |
|----------|---------|
| `GET /generate/course_options` | Languages + question types list |
| `GET /generate/question_types` | Question types list |
| `POST /words_select/all_words` | Words ordered by frequency (greeting + corpus) |
| `POST /words_select/submit_words` | Save selected/ordered word list |
| `POST /generate/sentences_for_word` | Candidate sentences for a word (sorted by length) |
| `POST /generate/questions_for_sentences` | Generate exercise previews from selected sentences |
| `POST /generate/save_lesson` | Save a lesson (word + exercises) to DB |
| `POST /generate/create_course_from_editor` | Bulk create course from word list |
| `POST/GET/PUT /generate/draft` | Save and resume wizard state |

### ✅ Service Layer (Dart) — Ready
All methods in `course_generation_service.dart`:
- `getAllWords()`, `submitWords()`, `getSentencesForWord()`
- `getQuestionTypes()`, `generateQuestionsForSentences()`
- `saveLesson()`, `createCourseFromEditor()`
- `saveDraft()`, `updateDraft()`, `getDraft()`, `listDrafts()`

### ❌ UI (Flutter) — Main Gap
The existing `generate_course_wizard_screen.dart` uses the **old** auto-generate flow
(CourseTemplate-based). It needs to be replaced with a new wizard.

---

## Core Concepts

### Module-first generation
The unit of work is a **module**, not a single lesson. Each module contains several lessons
(one lesson per word). The user works through the course module by module:
generate → preview module → accept or adjust → move to next module.

### Auto-generate exercises (no sentence selection)
No manual sentence selection step. For each word, the server automatically generates
**20 exercises** using the best available sentences (shortest first, most sentences covered).

### Duplicate handling
When multiple sentences share the same translation (duplicates), surface them to the user
in the module preview so they can choose to keep one, keep all, or discard.
All exercises are **selected by default** — the user only acts if they want to remove something.

---

## Target Flow

```
[New Course]
     │
     ▼
Step 1: Course Setup
  - Target language (default: Japanese)
  - Native language (default: Hebrew)
  - Title + Description (title auto-suggested from languages)
     │
     ▼
Step 2: Word Selection
  - Load words via getAllWords()
  - Greeting words at top (starred)
  - Select / deselect words (checkbox per row)
  - Drag-and-drop reorder of selected words
  - "Load more" pagination
  - Words grouped into modules (visual dividers: Module 1 | Module 2 | ...)
  - "Words per module" setting (default: 5)
     │
     ▼
Step 3: Question Types
  - All selected by default
  - Two groups: "Sentence exercises" and "Alphabet exercises"
  - Toggle per type
     │
     ▼
Step 4: Generate Module
  - Server generates 20 exercises per word in the current module
  - Progress indicator per word: "Generating 食べる... (2/5)"
  - On complete: navigate to Module Preview
     │
     ▼
Step 5: Module Preview  ← key interactive step
  - Shows the full module: all lessons, all exercises
  - All exercises selected by default
  - Duplicate sentence/translation pairs highlighted — user can keep all or pick one
  - User deselects any exercises they don't want
  - [Save Module] → saves to DB, moves to next module
  - [← Back] → return to word selection to adjust
     │
     ▼
  Repeat Steps 4–5 for each module
     │
     ▼
Step 6: Course Summary
  - N modules saved, N lessons, N exercises
  - [View Course] → opens Review Screen
  - [Back to Courses]
     │
     ▼
Review Screen (accessible anytime from courses list)
  - Full course tree: Module > Lesson > Exercises
  - Edit/remove exercises
  - [Save Changes]
```

---

## Implementation Phases

---

### Phase 1 — New Wizard (Steps 1–3)

**File:** `editor/ui/lib/screens/editor_flow_screen.dart`

Replace or re-route `generate_course_wizard_screen.dart`. Keep old file for reference.

#### Step 1: Course Setup
- `DropdownButtonFormField` for target and native language
- Default: Japanese → Hebrew
- `TextField` for title (auto-fill: "[Target] for [Native] speakers")
- Optional description field
- Validate: both languages required

#### Step 2: Word Selection
- Call `CourseGenerationService.getAllWords(lang: langCode)`
- List rows: `[checkbox]  word  [POS badge]  [N sentences]  [⭐ greeting]`
- `ReorderableListView` so user can drag to reorder selected words
- Visual module dividers — show "── Module 1 ──", "── Module 2 ──" etc. based on "words per module" setting
- "Words per module" number input (default: 5) — updates dividers live
- "Load more" for pagination
- Header: "42 words selected · 9 modules"
- Validate: at least 3 words selected

#### Step 3: Question Types
- Fetch from `getCourseOptions()` or use static list
- Two sections: "Sentence exercises" / "Alphabet exercises"
- `SwitchListTile` per type, all on by default
- Short description per type

---

### Phase 2 — Generate Module (Step 4)

**Widget:** `GenerateModuleWidget` (can live inside `editor_flow_screen.dart` or extracted)

#### Behavior
- Takes current module's word list
- For each word: call `getSentencesForWord()` → take up to 20 sentences → call `generateQuestionsForSentences()`
- Accumulate all exercises across words in the module
- Detect duplicates: same `sentence_id` + `to_id` appearing more than once → flag as duplicate
- Show progress:

```
Generating Module 1...

  ✓ 食べる     20 exercises
  ✓ 飲む       18 exercises
  ⟳ 見る       generating...
  ○ 行く
  ○ 来る

  ███████░░░░  3 / 5 words
```

- On complete → navigate to Module Preview (Step 5)

#### Backend note
- `generateQuestionsForSentences()` currently generates `sentence_single_choice` + ~10% `identify_words`
- May need to extend to generate all enabled question types per sentence
- **New backend endpoint needed:** `POST /generate/module_exercises`
  - Input: `{ lang, to_lang, words: [str], question_types: [str] }`
  - For each word: fetch up to 20 sentences, generate exercises of each enabled type
  - Return: `{ modules: [ { word, lessons: [ { exercises: [...] } ] } ] }`
  - Flag duplicates in the response

---

### Phase 3 — Module Preview (Step 5)

**File:** `editor/ui/lib/screens/module_preview_screen.dart`

This is the key interactive step. The user sees everything and decides what to keep.

#### Layout
```
Module 1  ·  5 lessons  ·  87 exercises

⚠ 3 duplicate translations found — review below

▼ Lesson: 食べる  (20 exercises)
  ☑ [single_choice]   食べる。          →  "To eat."
  ☑ [single_choice]   私は食べる。      →  "I eat."
  ⚠ [single_choice]   りんごを食べる。  →  "I eat."   ← duplicate translation
     Keep both  |  Keep this  |  Remove this
  ☑ [identify_words]  私はりんごを食べる。  →  words: [食べる, りんご]
  ...

▼ Lesson: 飲む  (18 exercises)
  ...

────────────────────────────────
[← Back to words]    [Save Module →]
```

#### Behavior
- All exercises `☑` by default
- Duplicates (same `to_sentence_id`) shown with ⚠ badge and inline choice:
  - **Keep all** (default — just leave both checked)
  - **Keep this one** (uncheck the other duplicate)
  - **Remove this** (uncheck current)
- Exercise rows show: type badge · sentence text · translation
- "Save Module" button:
  - Calls `saveLesson()` per lesson (word), passing only the checked exercises
  - Returns `courseId` + `moduleId` + `lessonId`
  - On last module: go to Course Summary (Step 6)
  - Otherwise: return to word list, advance to next module group

---

### Phase 4 — Course Summary & Review Screen

**File:** `editor/ui/lib/screens/course_review_screen.dart`

#### Course Summary (Step 6)
Simple screen shown after all modules are saved:
```
✓ Course created!
  Japanese for Hebrew speakers
  4 modules · 20 lessons · 312 exercises

[View Full Course]    [Back to Courses]
```

#### Review Screen (accessible anytime)
Full course tree for post-generation editing:
```
▼ Module 1  (5 lessons · 87 exercises)
  ▶ Lesson: 食べる
  ▼ Lesson: 飲む  (expanded)
      ☑ [single_choice]   飲む。  →  "To drink."
      ☑ [single_choice]   水を飲む。  →  "Drink water."
      ☐ [identify_words]  (deselected)

[Save Changes]
```

- Load via `GET /course/{id}` + `GET /course/{id}/modules` + lessons + exercises
- Checkbox toggles, collected changes sent on "Save Changes"
- **New backend endpoint needed:** `DELETE /course/exercises` — accepts list of exercise IDs to remove

---

### Phase 5 — Draft Save/Resume

**Already in service layer — just needs UI wiring.**

#### Save on each step advance
- Call `saveDraft()` on first advance, `updateDraft()` on subsequent steps
- Store `draftId` in wizard state
- Draft payload: lang, to_lang, word list + weights, question types, current step, current module index

#### Resume
- On "New Course" from courses screen, check for existing drafts
- If found: show dialog "Resume [title] (last edited X days ago)?" or "Start fresh"
- Load via `getDraft(id)` and restore wizard state to last saved step

---

## Files to Create / Modify

| File | Action | Notes |
|------|--------|-------|
| `editor/ui/lib/screens/editor_flow_screen.dart` | Create | New wizard Steps 1–3 + 6 |
| `editor/ui/lib/screens/module_preview_screen.dart` | Create | Step 5 — module preview + exercise selection |
| `editor/ui/lib/screens/course_review_screen.dart` | Create | Full course review after generation |
| `editor/ui/lib/screens/generate_course_wizard_screen.dart` | Archive | Keep old flow for reference |
| `editor/ui/lib/screens/courses_screen.dart` | Modify | Route to new wizard, show resume option |
| `editor/ui/lib/main.dart` | Modify | Add routes for new screens |
| `editor/server/src/routers/generate.py` | Modify | Add `POST /generate/module_exercises` |
| `editor/server/src/routers/course.py` | Modify | Add `DELETE /course/exercises` |

---

## Order of Work (Recommended)

1. **Phase 1** — Wizard Steps 1–3 (course setup, word selection with module dividers, question types)
2. **Phase 2** — Generate module step with progress bar + new backend endpoint
3. **Phase 3** — Module preview with duplicate handling and exercise selection
4. **Phase 4** — Course summary + review screen + delete exercises endpoint
5. **Phase 5** — Draft save/resume wired into wizard

---

## Open Questions

- **Duplicate policy:** Default is "keep all". Is that right, or should the default be "keep only the first occurrence"?
- **Module boundary:** Dividers in word list are visual. Should the user be able to drag words across module boundaries freely, or should modules be strict groups?
- **20 exercises per word:** Is 20 the right cap, or should it be configurable per course/module?
- **Course title:** Auto-generate from languages or always ask?

---

*Last updated: 2026-02-25*
