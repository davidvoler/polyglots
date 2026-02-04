import 'package:flutter/material.dart';
import '../services/course_generation_service.dart';

/// Editor flow: 1) Course options  2) Select/reorder words  3) Sentences + question types  4) Group into modules & create
/// Optional [draftId] resumes a saved draft from the database.
/// Optional [onBackToList] when set shows a back button to return to the draft list.
class EditorFlowScreen extends StatefulWidget {
  const EditorFlowScreen({super.key, this.draftId, this.onBackToList});

  final int? draftId;
  final VoidCallback? onBackToList;

  @override
  State<EditorFlowScreen> createState() => _EditorFlowScreenState();
}

class _EditorFlowScreenState extends State<EditorFlowScreen> {
  int _step = 0;
  final PageController _pageController = PageController();

  /// Set when we create or resume a draft; used for update vs create on save.
  int? _draftId;

  // Step 1: Course options
  List<CourseOption> _languages = [];
  List<QuestionTypeOption> _questionTypes = [];
  String? _langCode;
  String? _toLangCode;
  final _titleController = TextEditingController();
  final _descriptionController = TextEditingController();
  final Set<String> _selectedQuestionTypeIds = {};
  bool _loadingOptions = true;
  String? _optionsError;

  // Step 2: Words (all_words = greeting + corpus); reorderable, deletable
  List<WordSelect> _allWords = [];
  bool _loadingWords = false;
  String? _wordsError;

  // Step 3: Sentences per word (automate or per-word wizard)
  bool _automateLesson = false;
  final Map<String, List<int>> _sentencesPerWord = {};
  int _lessonsPerModule = 10;
  // Per-word lesson wizard state
  int _lessonWordIndex = 0;
  List<SentenceForWordItem> _sentencesForCurrentWord = [];
  final Set<String> _selectedSentenceKeys = {};  // "id_toId" for selected sentences
  List<GeneratedExercisePreview> _generatedExercises = [];
  final Set<int> _selectedExerciseIndices = {};
  int _savedCourseId = 0;
  int _savedModuleId = 0;
  bool _loadingSentences = false;
  bool _loadingQuestions = false;
  String? _lessonWizardError;

  // Step 4: Create
  bool _creating = false;
  String? _createResult;

  @override
  void initState() {
    super.initState();
    _draftId = widget.draftId;
    _loadCourseOptions();
  }

  @override
  void dispose() {
    _titleController.dispose();
    _descriptionController.dispose();
    _pageController.dispose();
    super.dispose();
  }

  Future<void> _loadCourseOptions() async {
    setState(() {
      _loadingOptions = true;
      _optionsError = null;
    });
    try {
      final res = await CourseGenerationService.getCourseOptions();
      setState(() {
        _languages = res.languages;
        _questionTypes = res.questionTypes;
        _langCode ??= 'ja';
        _toLangCode ??= 'en';
        _selectedQuestionTypeIds.addAll(_questionTypes.map((qt) => qt.id));
        _loadingOptions = false;
      });
      if (_draftId != null) await _loadDraft();
    } catch (e) {
      setState(() {
        _optionsError = e.toString();
        _loadingOptions = false;
      });
    }
  }

  /// Load draft from server and restore wizard state (call after options loaded).
  Future<void> _loadDraft() async {
    if (_draftId == null) return;
    try {
      final draft = await CourseGenerationService.getDraft(_draftId!);
      if (!mounted) return;
      _titleController.text = draft.title;
      _descriptionController.text = draft.description;
      setState(() {
        _langCode = draft.lang;
        _toLangCode = draft.toLang;
        _selectedQuestionTypeIds.clear();
        _selectedQuestionTypeIds.addAll(draft.selectedQuestionTypeIds);
        _allWords = draft.wordsWithWeight
            .map((w) => WordSelect(
                  lang: draft.lang,
                  word: w.word,
                  pos: '',
                  minWcount: 0,
                  maxWcount: 0,
                  sentencesCount: 0,
                  rootCount: 0,
                  greeting: false,
                ))
            .toList();
        _step = draft.step.clamp(0, 3);
        _automateLesson = draft.automateLesson;
        _lessonsPerModule = draft.lessonsPerModule;
        _sentencesPerWord.clear();
        _sentencesPerWord.addAll(draft.sentencesPerWord);
      });
      _pageController.jumpToPage(_step);
    } catch (e) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Failed to load draft: $e')));
    }
  }

  Future<void> _loadWords() async {
    if (_langCode == null) return;
    setState(() {
      _loadingWords = true;
      _wordsError = null;
    });
    try {
      final all = await CourseGenerationService.getAllWords(lang: _langCode!);
      setState(() {
        _allWords = all;
        _loadingWords = false;
      });
    } catch (e) {
      setState(() {
        _wordsError = e.toString();
        _loadingWords = false;
      });
    }
  }

  void _removeWord(int index) {
    setState(() {
      if (index >= 0 && index < _allWords.length) _allWords.removeAt(index);
    });
  }

  void _onReorder(int oldIndex, int newIndex) {
    setState(() {
      if (newIndex > oldIndex) newIndex--;
      final item = _allWords.removeAt(oldIndex);
      _allWords.insert(newIndex, item);
    });
  }

  Future<void> _submitWords() async {
    if (_langCode == null) return;
    try {
      final wordsWithWeight = _allWords.asMap().entries.map((e) => WordWithWeight(word: e.value.word, weight: e.key)).toList();
      await CourseGenerationService.submitWords(lang: _langCode!, toLang: _toLangCode ?? '', words: wordsWithWeight);
    } catch (e) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Submit words: $e')));
    }
  }

  /// Persist wizard state to DB (create or update draft).
  Future<void> _saveDraft() async {
    if (_langCode == null || _toLangCode == null) return;
    final wordsWithWeight = _allWords.asMap().entries.map((e) => WordWithWeight(word: e.value.word, weight: e.key)).toList();
    try {
      if (_draftId != null) {
        await CourseGenerationService.updateDraft(
          _draftId!,
          title: _titleController.text.trim().isEmpty ? 'New course' : _titleController.text.trim(),
          description: _descriptionController.text.trim(),
          lang: _langCode!,
          toLang: _toLangCode!,
          selectedQuestionTypeIds: _selectedQuestionTypeIds.toList(),
          wordsWithWeight: wordsWithWeight,
          step: _step,
          automateLesson: _automateLesson,
          lessonsPerModule: _lessonsPerModule,
          sentencesPerWord: Map.from(_sentencesPerWord),
        );
      } else {
        final draft = await CourseGenerationService.saveDraft(
          title: _titleController.text.trim().isEmpty ? 'New course' : _titleController.text.trim(),
          description: _descriptionController.text.trim(),
          lang: _langCode!,
          toLang: _toLangCode!,
          selectedQuestionTypeIds: _selectedQuestionTypeIds.toList(),
          wordsWithWeight: wordsWithWeight,
          step: _step,
          automateLesson: _automateLesson,
          lessonsPerModule: _lessonsPerModule,
          sentencesPerWord: Map.from(_sentencesPerWord),
        );
        setState(() => _draftId = draft.id);
      }
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Draft saved. You can resume later.')));
    } catch (e) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Failed to save draft: $e')));
    }
  }

  void _toggleQuestionType(String id) {
    setState(() {
      if (_selectedQuestionTypeIds.contains(id)) {
        _selectedQuestionTypeIds.remove(id);
      } else {
        _selectedQuestionTypeIds.add(id);
      }
    });
  }

  Future<void> _createCourse() async {
    if (_langCode == null || _toLangCode == null || _allWords.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Set languages and load at least one word.')),
      );
      return;
    }
    setState(() {
      _creating = true;
      _createResult = null;
    });
    try {
      final selectedWords = _allWords.map((w) => w.word).toList();
      final result = await CourseGenerationService.createCourseFromEditor(
        lang: _langCode!,
        toLang: _toLangCode!,
        title: _titleController.text.trim().isEmpty ? 'New course' : _titleController.text.trim(),
        description: _descriptionController.text.trim(),
        selectedWords: selectedWords,
        sentencesPerWord: _sentencesPerWord,
        enabledQuestionTypes: _selectedQuestionTypeIds.toList(),
        automateLesson: _automateLesson,
        lessonsPerModule: _lessonsPerModule,
      );
      setState(() {
        _creating = false;
        _createResult = 'Course created: id=${result['course_id']}';
      });
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Course created: ${result['course_id']}')),
        );
      }
    } catch (e) {
      setState(() {
        _creating = false;
        _createResult = 'Error: $e';
      });
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Failed: $e')));
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        leading: widget.onBackToList != null
            ? IconButton(icon: const Icon(Icons.arrow_back), onPressed: widget.onBackToList)
            : null,
        title: const Text('Create course (4 steps)'),
        elevation: 0,
        actions: [
          TextButton.icon(
            onPressed: (_langCode == null || _toLangCode == null) ? null : () async => await _saveDraft(),
            icon: const Icon(Icons.save_outlined, size: 20),
            label: const Text('Save draft'),
          ),
        ],
      ),
      body: Column(
        children: [
          _buildStepIndicator(),
          Expanded(
            child: PageView(
              controller: _pageController,
              physics: const NeverScrollableScrollPhysics(),
              onPageChanged: (i) => setState(() => _step = i),
              children: [
                _buildStep1(),
                _buildStep2(),
                _buildStep3(),
                _buildStep4(),
              ],
            ),
          ),
          _buildNavButtons(),
        ],
      ),
    );
  }

  Widget _buildStepIndicator() {
    const steps = ['1. Options', '2. Words', '3. Sentences & types', '4. Create'];
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 12),
      child: Row(
        children: List.generate(4, (i) {
          final active = _step == i;
          return Expanded(
            child: GestureDetector(
              onTap: () {
                _pageController.jumpToPage(i);
                setState(() => _step = i);
              },
              child: Center(
                child: Text(
                  steps[i],
                  style: TextStyle(
                    fontWeight: active ? FontWeight.bold : FontWeight.normal,
                    color: active ? Theme.of(context).colorScheme.primary : Colors.grey,
                  ),
                ),
              ),
            ),
          );
        }),
      ),
    );
  }

  Widget _buildStep1() {
    if (_loadingOptions) {
      return const Center(child: CircularProgressIndicator());
    }
    if (_optionsError != null) {
      return Center(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(_optionsError!, textAlign: TextAlign.center),
              const SizedBox(height: 16),
              ElevatedButton(onPressed: _loadCourseOptions, child: const Text('Retry')),
            ],
          ),
        ),
      );
    }
    return SingleChildScrollView(
      padding: const EdgeInsets.all(24),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Languages', style: TextStyle(fontWeight: FontWeight.bold)),
          const SizedBox(height: 8),
          Row(
            children: [
              const Text('Learn: '),
              DropdownButton<String>(
                value: _langCode,
                items: _languages.map((l) => DropdownMenuItem(value: l.code, child: Text(l.name))).toList(),
                onChanged: (v) => setState(() => _langCode = v),
              ),
              const SizedBox(width: 24),
              const Text('Native: '),
              DropdownButton<String>(
                value: _toLangCode,
                items: _languages.map((l) => DropdownMenuItem(value: l.code, child: Text(l.name))).toList(),
                onChanged: (v) => setState(() => _toLangCode = v),
              ),
            ],
          ),
          const SizedBox(height: 16),
          const Text('Title', style: TextStyle(fontWeight: FontWeight.bold)),
          TextField(
            controller: _titleController,
            decoration: const InputDecoration(hintText: 'Course title'),
          ),
          const SizedBox(height: 8),
          const Text('Description', style: TextStyle(fontWeight: FontWeight.bold)),
          TextField(
            controller: _descriptionController,
            maxLines: 2,
            decoration: const InputDecoration(hintText: 'Optional description'),
          ),
          const SizedBox(height: 16),
          const Text('Question types (select applicable)', style: TextStyle(fontWeight: FontWeight.bold)),
          ..._questionTypes.map((qt) => CheckboxListTile(
                title: Text(qt.name),
                subtitle: Text(qt.description),
                value: _selectedQuestionTypeIds.contains(qt.id),
                onChanged: (_) => _toggleQuestionType(qt.id),
              )),
        ],
      ),
    );
  }

  Widget _buildStep2() {
    return Column(
      children: [
        // Fixed header section
        Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  ElevatedButton(
                    onPressed: _loadingWords ? null : () => _loadWords(),
                    child: Text(_loadingWords ? 'Loading...' : 'Load words (all_words: greeting + corpus)'),
                  ),
                ],
              ),
              if (_wordsError != null) Padding(padding: const EdgeInsets.only(top: 8), child: Text(_wordsError!, style: const TextStyle(color: Colors.red))),
              const SizedBox(height: 16),
              Text('Words: ${_allWords.length}. Drag to reorder, delete to exclude.', style: TextStyle(color: Colors.grey[600])),
            ],
          ),
        ),
        // Scrollable list section
        Expanded(
          child: _allWords.isEmpty
              ? const Center(child: Text('Load words to see list.'))
              : ReorderableListView.builder(
                  padding: const EdgeInsets.symmetric(horizontal: 24),
                  itemCount: _allWords.length,
                  onReorder: _onReorder,
                  itemBuilder: (context, index) {
                    final w = _allWords[index];
                    return Card(
                      key: ValueKey(w.word),
                      margin: const EdgeInsets.symmetric(vertical: 4),
                      child: ListTile(
                        leading: const Icon(Icons.drag_handle),
                        title: Text(w.word, style: const TextStyle(fontWeight: FontWeight.bold)),
                        subtitle: Text(
                          'pos: ${w.pos} | min/max wcount: ${w.minWcount}-${w.maxWcount} | sentences: ${w.sentencesCount} | root_count: ${w.rootCount}${w.greeting ? ' | greeting' : ''}',
                          style: TextStyle(fontSize: 12, color: Colors.grey[600]),
                        ),
                        trailing: IconButton(
                          icon: const Icon(Icons.delete_outline),
                          onPressed: () => _removeWord(index),
                        ),
                      ),
                    );
                  },
                ),
        ),
      ],
    );
  }

  Widget _buildStep3() {
    if (_automateLesson) {
      return SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('3. For each word: select sentences & question types', style: TextStyle(fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            CheckboxListTile(
              title: const Text('Automate lesson creation'),
              subtitle: const Text('Use shortest 15 sentences, 15 single choice + 5 identify words'),
              value: _automateLesson,
              onChanged: (v) => setState(() => _automateLesson = v ?? false),
            ),
            const SizedBox(height: 16),
            Text('Words: ${_allWords.length}. Sentence selection per word can be added in a follow-up (open each word → load sentences → pick ~10).', style: TextStyle(color: Colors.grey[600])),
            const SizedBox(height: 16),
            const Text('Lessons per module (step 4)', style: TextStyle(fontWeight: FontWeight.bold)),
            TextField(
              keyboardType: TextInputType.number,
              onChanged: (s) => setState(() => _lessonsPerModule = int.tryParse(s) ?? 10),
              decoration: InputDecoration(
                hintText: '$_lessonsPerModule',
                suffixText: 'lessons per module',
              ),
            ),
          ],
        ),
      );
    }
    // Per-word wizard: sentences → generate questions → choose → save lesson → next word
    if (_allWords.isEmpty) {
      return const Center(child: Text('Load words in step 2 first.'));
    }
    final wordIndex = _lessonWordIndex.clamp(0, _allWords.length - 1);
    final currentWord = _allWords[wordIndex];
    final totalWords = _allWords.length;
    return SingleChildScrollView(
      padding: const EdgeInsets.all(24),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('3. Lesson for word ${wordIndex + 1} of $totalWords: ${currentWord.word}', style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
          const SizedBox(height: 16),
          CheckboxListTile(
            title: const Text('Automate lesson creation'),
            subtitle: const Text('Use shortest 15 sentences, 15 single choice + 5 identify words'),
            value: _automateLesson,
            onChanged: (v) => setState(() => _automateLesson = v ?? false),
          ),
          const SizedBox(height: 16),
          const Text('1. Select the sentences and translations', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
          const SizedBox(height: 4),
          Text('Load sentences for this word, then select which ones (with translation) to include.', style: TextStyle(color: Colors.grey[700], fontSize: 13)),
          const SizedBox(height: 8),
          ElevatedButton(
            onPressed: _loadingSentences ? null : () => _loadSentencesForCurrentWord(),
            child: Text(_loadingSentences ? 'Loading...' : 'Load sentences for "${currentWord.word}"'),
          ),
          if (_lessonWizardError != null) Padding(padding: const EdgeInsets.only(top: 8), child: Text(_lessonWizardError!, style: const TextStyle(color: Colors.red))),
          if (_sentencesForCurrentWord.isNotEmpty) ...[
            const SizedBox(height: 8),
            Text('Sentences and translations (${_selectedSentenceKeys.length} selected):', style: TextStyle(color: Colors.grey[700])),
            const SizedBox(height: 4),
            ...List.generate(_sentencesForCurrentWord.length, (i) {
              final s = _sentencesForCurrentWord[i];
              final key = '${s.id}_${s.toId}';
              return CheckboxListTile(
                value: _selectedSentenceKeys.contains(key),
                onChanged: (v) {
                  setState(() {
                    if (v == true) {
                      _selectedSentenceKeys.add(key);
                    } else {
                      _selectedSentenceKeys.remove(key);
                    }
                  });
                },
                title: Text(s.sentence, style: const TextStyle(fontSize: 14)),
                subtitle: Text(s.translation, style: TextStyle(fontSize: 12, color: Colors.grey[600])),
              );
            }),
          ],
          const SizedBox(height: 24),
          const Text('2. Show the lessons created from the sentences', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
          const SizedBox(height: 4),
          Text('Generate exercises from your selected sentences. Then review and deselect any you do not want.', style: TextStyle(color: Colors.grey[700], fontSize: 13)),
          const SizedBox(height: 8),
          ElevatedButton(
            onPressed: (_loadingQuestions || _selectedSentenceKeys.isEmpty) ? null : () => _generateQuestionsForCurrentWord(),
            child: Text(_loadingQuestions ? 'Generating...' : 'Create lessons from ${_selectedSentenceKeys.length} sentences'),
          ),
          if (_generatedExercises.isNotEmpty) ...[
            const SizedBox(height: 12),
            Text('Lessons created from the selected sentences. All included by default; deselect the questions you do not want to include (${_selectedExerciseIndices.length} selected).', style: TextStyle(color: Colors.grey[700], fontSize: 13)),
            const SizedBox(height: 4),
            ...List.generate(_generatedExercises.length, (i) {
              final ex = _generatedExercises[i];
              return CheckboxListTile(
                value: _selectedExerciseIndices.contains(i),
                onChanged: (v) {
                  setState(() {
                    if (v == true) {
                      _selectedExerciseIndices.add(i);
                    } else {
                      _selectedExerciseIndices.remove(i);
                    }
                  });
                },
                title: Text('${ex.exerciseType}: ${ex.sentence}', style: const TextStyle(fontSize: 13), maxLines: 2, overflow: TextOverflow.ellipsis),
                subtitle: Text(ex.toSentence, style: TextStyle(fontSize: 12, color: Colors.grey[600]), maxLines: 1, overflow: TextOverflow.ellipsis),
              );
            }),
          ],
          const SizedBox(height: 24),
          const Text('3. Save lesson and move to next word', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
          const SizedBox(height: 8),
          Row(
            children: [
              ElevatedButton(
                onPressed: _selectedExerciseIndices.isEmpty ? null : () => _saveLessonForCurrentWord(),
                child: const Text('Save lesson'),
              ),
              const SizedBox(width: 16),
              if (wordIndex < totalWords - 1)
                ElevatedButton(
                  onPressed: () => _nextLessonWord(),
                  child: const Text('Next word'),
                )
              else
                Text('No more words.', style: TextStyle(color: Colors.grey[600])),
            ],
          ),
          const SizedBox(height: 16),
          const Text('Lessons per module (for step 4)', style: TextStyle(fontWeight: FontWeight.bold)),
          TextField(
            keyboardType: TextInputType.number,
            onChanged: (s) => setState(() => _lessonsPerModule = int.tryParse(s) ?? 10),
            decoration: InputDecoration(
              hintText: '$_lessonsPerModule',
              suffixText: 'lessons per module',
            ),
          ),
        ],
      ),
    );
  }

  Future<void> _loadSentencesForCurrentWord() async {
    if (_langCode == null || _toLangCode == null || _allWords.isEmpty) return;
    final word = _allWords[_lessonWordIndex.clamp(0, _allWords.length - 1)].word;
    setState(() {
      _loadingSentences = true;
      _lessonWizardError = null;
    });
    try {
      final res = await CourseGenerationService.getSentencesForWord(lang: _langCode!, toLang: _toLangCode!, word: word, limit: 30);
      if (mounted) setState(() {
        _sentencesForCurrentWord = res.sentences;
        _loadingSentences = false;
        _selectedSentenceKeys.clear();
      });
    } catch (e) {
      if (mounted) setState(() {
        _lessonWizardError = e.toString();
        _loadingSentences = false;
      });
    }
  }

  Future<void> _generateQuestionsForCurrentWord() async {
    if (_langCode == null || _toLangCode == null || _selectedSentenceKeys.isEmpty) return;
    final word = _allWords[_lessonWordIndex.clamp(0, _allWords.length - 1)].word;
    final pairs = <SentenceIdPair>[];
    for (final s in _sentencesForCurrentWord) {
      final key = '${s.id}_${s.toId}';
      if (_selectedSentenceKeys.contains(key)) pairs.add(SentenceIdPair(sentenceId: s.id, toId: s.toId));
    }
    setState(() {
      _loadingQuestions = true;
      _lessonWizardError = null;
    });
    try {
      final res = await CourseGenerationService.generateQuestionsForSentences(
        lang: _langCode!,
        toLang: _toLangCode!,
        word: word,
        sentences: pairs,
      );
      if (mounted) setState(() {
        _generatedExercises = res.exercises;
        _loadingQuestions = false;
        _selectedExerciseIndices.clear();
        for (int i = 0; i < res.exercises.length; i++) _selectedExerciseIndices.add(i);
      });
    } catch (e) {
      if (mounted) setState(() {
        _lessonWizardError = e.toString();
        _loadingQuestions = false;
      });
    }
  }

  Future<void> _saveLessonForCurrentWord() async {
    if (_langCode == null || _toLangCode == null || _selectedExerciseIndices.isEmpty) return;
    final word = _allWords[_lessonWordIndex.clamp(0, _allWords.length - 1)].word;
    final exercises = _selectedExerciseIndices.map((i) => _generatedExercises[i]).toList();
    setState(() => _lessonWizardError = null);
    try {
      final res = await CourseGenerationService.saveLesson(
        courseId: _savedCourseId,
        moduleId: _savedModuleId,
        lang: _langCode!,
        toLang: _toLangCode!,
        word: word,
        title: word,
        courseTitle: _titleController.text.trim().isEmpty ? 'New course' : _titleController.text.trim(),
        courseDescription: _descriptionController.text.trim(),
        lessonsPerModule: _lessonsPerModule,
        wordIndex: _lessonWordIndex,
        exercises: exercises,
      );
      if (mounted) {
        setState(() {
          _savedCourseId = res.courseId;
          _savedModuleId = res.moduleId;
        });
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Lesson saved: ${res.lessonId}')));
      }
    } catch (e) {
      if (mounted) setState(() => _lessonWizardError = e.toString());
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Save failed: $e')));
    }
  }

  void _nextLessonWord() {
    if (_lessonWordIndex < _allWords.length - 1) {
      setState(() {
        _lessonWordIndex++;
        _sentencesForCurrentWord = [];
        _selectedSentenceKeys.clear();
        _generatedExercises = [];
        _selectedExerciseIndices.clear();
        _lessonWizardError = null;
      });
    }
  }

  Widget _buildStep4() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(24),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('4. Group lessons into modules and create course', style: TextStyle(fontWeight: FontWeight.bold)),
          const SizedBox(height: 16),
          Text('Words: ${_allWords.length}. Modules: ${(_allWords.length / _lessonsPerModule).ceil()} ($_lessonsPerModule lessons per module).'),
          const SizedBox(height: 24),
          if (_createResult != null) Padding(padding: const EdgeInsets.only(bottom: 16), child: Text(_createResult!)),
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: _creating ? null : _createCourse,
              child: Text(_creating ? 'Creating...' : 'Create course'),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildNavButtons() {
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          if (_step > 0)
            TextButton(
              onPressed: () async {
                _pageController.previousPage(duration: const Duration(milliseconds: 200), curve: Curves.easeInOut);
                setState(() => _step--);
                await _saveDraft();
              },
              child: const Text('Back'),
            )
          else
            const SizedBox(),
          if (_step < 3)
            ElevatedButton(
              onPressed: () async {
                if (_step == 0 && _langCode != null) _loadWords();
                if (_step == 1 && _allWords.isNotEmpty) await _submitWords();
                _pageController.nextPage(duration: const Duration(milliseconds: 200), curve: Curves.easeInOut);
                setState(() => _step++);
                await _saveDraft();
              },
              child: const Text('Next'),
            )
          else
            const SizedBox(),
        ],
      ),
    );
  }
}

/// Wrapper: show "Start new" + list of drafts, or EditorFlowScreen when user chooses.
class EditorCreateCourseScreen extends StatefulWidget {
  const EditorCreateCourseScreen({super.key});

  @override
  State<EditorCreateCourseScreen> createState() => _EditorCreateCourseScreenState();
}

class _EditorCreateCourseScreenState extends State<EditorCreateCourseScreen> {
  bool _showFlow = false;
  int? _draftId;

  void _startNew() => setState(() {
    _showFlow = true;
    _draftId = null;
  });

  void _resumeDraft(int id) => setState(() {
    _showFlow = true;
    _draftId = id;
  });

  void _backToList() => setState(() {
    _showFlow = false;
    _draftId = null;
  });

  @override
  Widget build(BuildContext context) {
    if (_showFlow) {
      return EditorFlowScreen(draftId: _draftId, onBackToList: _backToList);
    }
    return _EditorDraftListContent(onStartNew: _startNew, onResumeDraft: _resumeDraft);
  }
}

class _EditorDraftListContent extends StatefulWidget {
  const _EditorDraftListContent({required this.onStartNew, required this.onResumeDraft});

  final VoidCallback onStartNew;
  final void Function(int draftId) onResumeDraft;

  @override
  State<_EditorDraftListContent> createState() => _EditorDraftListContentState();
}

class _EditorDraftListContentState extends State<_EditorDraftListContent> {
  List<EditorDraftListItem> _drafts = [];
  bool _loading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _loadDrafts();
  }

  Future<void> _loadDrafts() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final list = await CourseGenerationService.listDrafts();
      if (mounted) setState(() {
        _drafts = list;
        _loading = false;
      });
    } catch (e) {
      if (mounted) setState(() {
        _error = e.toString();
        _loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Create course'),
        elevation: 0,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Start a new course or resume a saved draft.', style: TextStyle(fontSize: 16)),
            const SizedBox(height: 24),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                onPressed: widget.onStartNew,
                icon: const Icon(Icons.add_circle_outline),
                label: const Text('Start new course'),
                style: ElevatedButton.styleFrom(padding: const EdgeInsets.symmetric(vertical: 16)),
              ),
            ),
            const SizedBox(height: 32),
            const Text('Resume draft', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
            const SizedBox(height: 8),
            if (_loading)
              const Center(child: Padding(padding: EdgeInsets.all(24), child: CircularProgressIndicator()))
            else if (_error != null)
              Padding(
                padding: const EdgeInsets.only(top: 8),
                child: Text(_error!, style: const TextStyle(color: Colors.red)),
              )
            else if (_drafts.isEmpty)
              Text('No drafts yet. Start a new course and use "Save draft" to resume later.', style: TextStyle(color: Colors.grey[600]))
            else
              ListView.separated(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                itemCount: _drafts.length,
                separatorBuilder: (_, __) => const SizedBox(height: 8),
                itemBuilder: (context, index) {
                  final d = _drafts[index];
                  return Card(
                    child: ListTile(
                      title: Text(d.title.isEmpty ? 'Untitled' : d.title),
                      subtitle: Text('Step ${d.step + 1} · ${d.lang} → ${d.toLang} · ${d.updatedAt}'),
                      trailing: const Icon(Icons.arrow_forward),
                      onTap: () => widget.onResumeDraft(d.id),
                    ),
                  );
                },
              ),
          ],
        ),
      ),
    );
  }
}
