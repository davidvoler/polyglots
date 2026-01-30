# Editor plan: interactive course authoring flow

**Goal:** The Editor is an app for course creation and editing - we want it to be ready to use 


**Existing Editor Code:**

We have a server and UI
Server in python 
UI if flutter 




**Your process (5 parts):**

1. **Select and order words** — Server returns words ordered by how common they are in the content (most common first).
2. **User selects words and reorders them** — The course editor chooses which words to include and in what order.
3. **For each word, offer sentences and translations** — User sees candidate sentences (with translation) for that word and chooses which to use.
4. **Show the user all sentences for the word ordered by sentences length with translation and option** — Let the user choose the best sentences for the current lesson 
5. **Generate question types automatically; user chooses what is applicable** — System generates the possible question types (single choice, multiple choice, identify words, letter-in-words, memory game, etc.); user enables/disables per lesson or globally.
6. **For each lesson show words so far** - For each lesson show words that were used in previous lessons - this will help the user to choose the sentences that contain them
7. **If the course is teaching alphabet - show letters so far** - show the letters used so far and how many times for each lesson
8. **In the case of Japanese - Choose also the letter type Hirgana, Katakana or Kanji** - add ab_type for the letters 
---

## Current state (summary)

- **Words by frequency:** [editor/server/src/routers/generate.py](editor/server/src/routers/generate.py) — `common_words`, `common_root`, `common_elements` query `content_raw.sentence_elements`, return words with counts, ordered by count desc. So “most common first” is already available. [words_select](editor/server/src/routers/words_select.py) uses [module_words.py](editor/server/src/generators/module_words.py) and `content_raw.words_pos1` with a different ordering (sentence-length buckets, root_count, sentences_count) for pre-built modules.
- **Select/reorder in UI:** [generate_course_wizard_screen.dart](editor/ui/lib/screens/generate_course_wizard_screen.dart) has a word-selection step and calls the words_select API; there is no clear “get common words then reorder” flow or drag-and-drop reorder.
- **Sentences per word:** [lessons_from_words.py](editor/server/src/generators/lessons_from_words.py) has `create_question(word, lang, to_lang)` which loads sentences + translation + options from `content_raw.sentence_elements` + `translation_links` + `sentences`. This is used in scripts, not exposed as an API for the editor. So there is no “get sentences for this word so the user can pick” endpoint.
- **~10 sentences:** Logic in `create_question` uses `limit 30`; no parameter or UI to target ~10 or let the user pick which 10.
- **Question types:** [editor/server/src/question_types/](editor/server/src/question_types/) implements: sentence_single_choice, sentence_multiple_choice, letter_in_words, memory_game, identify_words_in_speech, type_question, words_in_grid, description. [gen_from_course.py](editor/server/src/question_types/gen_from_course.py) augments lessons (e.g. alphabet with memory game, letter_in_words). There is no API or UI to “choose which question types are applicable” per lesson or per course.

---

## 1. Words: server returns common words, user selects and reorders

**Backend**

- **Unify or expose “common words” for the editor:** Either reuse existing `POST /api/v1/generate/common_words` (and optionally `common_root` / `common_elements`) so the editor UI can call it with `lang`, `to_lang`, `limit`, `offset`, and optionally `word_type` / `words_count`. Or add a single endpoint, e.g. `POST /api/v1/generate/words` that returns words ordered by frequency (from `content_raw.sentence_elements` or `words_pos1`, depending on desired metric: raw count vs. sentence_count/root_count). Response should include at least: `word`, `count` (or `sentences_count`), and optionally `pos` so the UI can show and sort.
- **Optional: persist selected/reordered list:** If you want to save “selected word list” or “module/lesson plan” before generating lessons, add an endpoint that accepts an ordered list of words (e.g. `word_ids` or `words[]`) and stores it (e.g. in a draft course or a “word list” resource). Otherwise the UI can keep the selected order in memory and send it when requesting sentences (step 2).

**UI**

- **Step “Select and order words”:**  
  - Call the common-words API (e.g. `common_words` or the new `words`) with `lang`, `to_lang`, and a sensible default limit (e.g. 100–200).  
  - Show the list (e.g. “word – count”) so the user sees “most common first”.  
  - Let the user **select** which words to include (e.g. checkboxes or “Add to course”) and **reorder** the selected list (e.g. drag-and-drop or up/down).  
  - Result: an ordered list of words that will drive lesson generation (one lesson per word, or grouped by module as you prefer).

---

## 2. For each word: offer sentences and translations (user selects ~10)

**Backend**

- **Endpoint “sentences for word”:** Add an API used by the editor to fetch candidate sentences for a given word, e.g.  
  `POST /api/v1/generate/sentences_for_word`  
  Body: `{ "lang", "to_lang", "word" }`  
  Logic: same as in [lessons_from_words.create_question](editor/server/src/generators/lessons_from_words.py) (query `content_raw.sentence_elements` + translation_links + sentences where the word appears in root/word1/word2/word3), return a list of items with at least: sentence id, sentence text, translation text, options (for multiple choice). Optionally order by `len_elm` and cap at 20–30 so the user has a manageable list to choose from.
- **Optional: “save selected sentences for word”:** If you want to persist the user’s choices before generating exercises, add an endpoint that accepts `word` + list of `sentence_id` (and optionally `to_id`) and stores them (e.g. in a draft lesson or in the same “word list” resource). Otherwise the UI can pass the selected sentence IDs when triggering “generate lesson” or “generate exercises”.

**UI**

- **Step “Sentences for word” (per word or in a list view):**  
  - For each word in the selected/reordered list, call `sentences_for_word` and show the results (sentence + translation; optionally options).  
  - Let the user **select** which sentences to keep (e.g. checkboxes; default or hint: “aim for ~10”).  
  - Optional: allow reordering the selected sentences (order will define lesson order).  
  - If you have “save selected sentences”, call it when the user confirms; otherwise keep the selection in memory and pass it to the “generate lesson / exercises” step.

---

## 3. Each word has around 10 sentences

- **Backend:** The “sentences for word” response can be capped (e.g. 20–30); the UI enforces “around 10” by design (e.g. “Select up to 10” or “Recommend 10”). If you add validation, an optional check: when generating a lesson for a word, require at least 1 and at most N (e.g. 15) selected sentences.
- **UI:** Show a counter (“X / 10 sentences”) and optionally a warning if the user selects far from 10 (e.g. &lt; 5 or &gt; 15). You can pre-select the first 10 by default so the user only deselects/adds as needed.

---

## 4. Generate question types automatically; user chooses what is applicable

**Backend**

- **List available question types:** Add an endpoint, e.g. `GET /api/v1/generate/question_types`, that returns the list of question types the system can generate (e.g. `sentence_single_choice`, `sentence_multiple_choice`, `letter_in_words`, `memory_game`, `identify_words_in_speech`, `type_question`, `words_in_grid`, `explanation`/description). Optionally include a short label and “applicable to” (e.g. “sentence lessons only”, “alphabet lessons only”) so the UI can show them in a sensible way.
- **Generate exercises with selection:** The existing flow (e.g. [gen_from_course](editor/server/src/question_types/gen_from_course.py), [course_from_file_question_types](editor/server/src/generators/course_from_file_question_types.py), or [create_course_from_file](editor/server/src/generators/create_course_from_file.py)) creates exercises in `course.exercise`. Add a parameter (e.g. `question_types: list[str]` or `enabled_question_types: list[str]`) to the “generate course/lesson/exercises” API so that only the selected types are generated. For each type, call the existing generator (e.g. sentences_single_choice, sentences_multiple_choice, letter_in_words, memory_game, etc.) only if that type is in the list.
- **Where to apply:** Decide whether the choice is per course, per module, or per lesson. Simplest: per course (“for this course, generate these question types”). Then when generating exercises for each lesson, only create exercises whose `exercise_type` is in the user’s list.

**UI**

- **Step “Question types”:**  
  - Call `GET /api/v1/generate/question_types` (or use a static list if you prefer).  
  - Show checkboxes (or toggles) for each type, with a short description (e.g. “Single choice: pick the correct translation”, “Memory game: match pairs”).  
  - Optionally show “applicable to” (e.g. “Sentence lessons”, “Alphabet lessons”) so the user understands when each type is used.  
  - Save the selected list and pass it when calling “generate course” or “generate exercises”.

---

## 5. End-to-end flow (suggested)

```mermaid
sequenceDiagram
  participant User
  participant EditorUI
  participant EditorServer
  participant DB

  User->>EditorUI: New course (lang, to_lang)
  EditorUI->>EditorServer: GET/POST words (common words)
  EditorServer->>DB: content_raw.sentence_elements / words_pos1
  DB-->>EditorServer: words ordered by frequency
  EditorServer-->>EditorUI: word list (word, count)
  User->>EditorUI: Select words, reorder
  loop For each word
    EditorUI->>EditorServer: sentences_for_word(word)
    EditorServer->>DB: sentence_elements + translations
    DB-->>EditorServer: candidates
    EditorServer-->>EditorUI: sentences + translation (+ options)
    User->>EditorUI: Select ~10 sentences
  end
  User->>EditorUI: Choose question types (checkboxes)
  EditorUI->>EditorServer: generate course/lessons/exercises(ordered words, selected sentences per word, enabled_question_types)
  EditorServer->>EditorServer: create course, modules, lessons; for each lesson create exercises by type
  EditorServer->>DB: course.exercise, course.lesson, etc.
  EditorServer-->>EditorUI: course id / summary
```

---

## 6. Order of work (suggested)

1. **Backend: sentences for word** — Add `POST /api/v1/generate/sentences_for_word` (or under a different router) that returns candidate sentences + translation + options for a given word, reusing logic from `lessons_from_words.create_question`.
2. **Backend: question types list and filter** — Add `GET /api/v1/generate/question_types` and extend the generate-course/lesson/exercises path with an `enabled_question_types` (or similar) parameter so only selected types are generated.
3. **UI: words step** — Use existing `common_words` (or new `words`) API; add selection and reorder (e.g. drag-and-drop) and persist the ordered word list in state or via a new “draft” API.
4. **UI: sentences-per-word step** — For each selected word, call `sentences_for_word`, show list with checkboxes, let user select ~10 and optionally reorder; store selected sentence IDs.
5. **UI: question types step** — List question types with checkboxes; pass selected types into the generate API.
6. **Wire “Generate”** — When user clicks Generate, call the course/lesson/exercise generator with: ordered words, selected sentences per word (~10), and enabled question types. Ensure the generator writes to `course.exercise` (and course/module/lesson tables) so the Student app can consume the course.

---

## 7. Files to touch (summary)

| Area | Backend | UI |
|------|--------|-----|
| Words (order, select, reorder) | [generate.py](editor/server/src/routers/generate.py) (existing common_words); optional draft API | [generate_course_wizard_screen.dart](editor/ui/lib/screens/generate_course_wizard_screen.dart) (or new screen): list, select, reorder |
| Sentences per word | New: sentences_for_word in generate router or new router; reuse [lessons_from_words](editor/server/src/generators/lessons_from_words.py) | New step: per-word sentence picker (~10), call API, show sentence + translation, checkboxes |
| Question types | New: question_types endpoint; extend [gen_from_course](editor/server/src/question_types/gen_from_course.py) / course_from_file_question_types with enabled_question_types | New step: list types, checkboxes, pass to generate |
| Generate course | Extend [generate.py](editor/server/src/routers/generate.py) or [course_from_file_question_types](editor/server/src/generators/course_from_file_question_types.py) to accept word list + sentences per word + question types and write to course.* | “Generate” button that sends full payload |

---

## 8. Optional later

- **Draft / save progress:** Save “selected words + order” and “selected sentences per word” as a draft so the user can leave and come back.
- **Edit after generate:** Allow editing the generated course (add/remove/reorder lessons or exercises) in the Editor UI.
- **AI assist:** Use an AI agent to suggest words, suggest sentences for a word, or suggest which question types to enable (as in [common/DOC/authoring_tool.md](common/DOC/authoring_tool.md)).

This plan keeps your existing Python-based course generation and content tables, and adds the minimal APIs and UI steps so the process is interactive: words (select & reorder) → sentences per word (~10) → question types (choose applicable) → generate.
