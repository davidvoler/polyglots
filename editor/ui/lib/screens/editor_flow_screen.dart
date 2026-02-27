import 'dart:math';
import 'package:flutter/material.dart';
import '../services/course_generation_service.dart';
import 'module_preview_screen.dart';
import 'course_review_screen.dart';

enum _Phase { setup, wordSelect, questionTypes, generating, summary }

/// New wizard: Course Setup → Word Selection → Question Types →
/// [for each module: Generate → Module Preview] → Course Summary.
/// Optional [draftId] resumes a saved draft.
class EditorFlowScreen extends StatefulWidget {
  const EditorFlowScreen({super.key, this.draftId, this.onBackToList});
  final int? draftId;
  final VoidCallback? onBackToList;

  @override
  State<EditorFlowScreen> createState() => _EditorFlowScreenState();
}

class _EditorFlowScreenState extends State<EditorFlowScreen> {
  _Phase _phase = _Phase.setup;
  int? _draftId;

  // Step 1: Course setup
  List<CourseOption> _languages = [];
  List<QuestionTypeOption> _questionTypes = [];
  String _langCode = 'ja';
  String _toLangCode = 'he';
  final _titleController = TextEditingController();
  final _descController = TextEditingController();
  bool _loadingOptions = true;
  String? _optionsError;

  // Step 2: Word selection
  List<WordSelect> _selectedWords = [];
  List<WordSelect> _availableWords = [];
  int _wordsPerModule = 5;
  bool _loadingWords = false;
  String? _wordsError;
  bool _hasMoreWords = true;
  int _skipCount = 0;

  // Step 3: Question types
  final Set<String> _selectedQTypeIds = {};

  // Module generation state
  int _moduleIndex = 0;
  int _savedCourseId = 0;
  // Progress tracking
  final Map<String, String> _wordStatus = {}; // 'pending' | 'generating' | 'done(N)' | 'error'
  final Map<String, List<GeneratedExercisePreview>> _wordExercises = {};
  bool _generating = false;
  // Accumulated vocabulary from saved modules, used as distractors for identify exercises
  final List<String> _allWordsSoFar = [];

  // Course summary
  int _savedModulesCount = 0;
  int _totalLessons = 0;
  int _totalExercises = 0;

  int get _moduleCount => _selectedWords.isEmpty ? 0 : (_selectedWords.length / _wordsPerModule).ceil();

  @override
  void initState() {
    super.initState();
    _draftId = widget.draftId;
    _loadCourseOptions();
  }

  @override
  void dispose() {
    _titleController.dispose();
    _descController.dispose();
    super.dispose();
  }

  // ───────────── data loading ─────────────

  Future<void> _loadCourseOptions() async {
    setState(() { _loadingOptions = true; _optionsError = null; });
    try {
      final res = await CourseGenerationService.getCourseOptions();
      setState(() {
        _languages = res.languages;
        _questionTypes = res.questionTypes;
        _selectedQTypeIds.addAll(res.questionTypes.map((qt) => qt.id));
        _loadingOptions = false;
      });
      if (_draftId != null) await _loadDraft();
    } catch (e) {
      setState(() { _optionsError = e.toString(); _loadingOptions = false; });
    }
  }

  Future<void> _loadDraft() async {
    if (_draftId == null) return;
    try {
      final draft = await CourseGenerationService.getDraft(_draftId!);
      if (!mounted) return;
      _titleController.text = draft.title;
      _descController.text = draft.description;
      setState(() {
        _langCode = draft.lang;
        _toLangCode = draft.toLang;
        _selectedQTypeIds
          ..clear()
          ..addAll(draft.selectedQuestionTypeIds);
        _selectedWords = draft.wordsWithWeight
            .map((w) => WordSelect(lang: draft.lang, word: w.word, pos: '', minWcount: 0, maxWcount: 0, sentencesCount: 0, rootCount: 0))
            .toList();
        _wordsPerModule = draft.lessonsPerModule;
        _phase = _Phase.values[draft.step.clamp(0, _Phase.values.length - 1)];
      });
    } catch (e) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Failed to load draft: $e')));
    }
  }

  Future<void> _loadWords({bool loadMore = false}) async {
    setState(() { _loadingWords = true; _wordsError = null; });
    try {
      final all = await CourseGenerationService.getAllWords(lang: _langCode, skipCount: loadMore ? _skipCount : 0);
      setState(() {
        if (!loadMore) {
          _skipCount = 0;
          // Greeting words pre-selected, rest in available
          final greeting = all.where((w) => w.greeting).toList();
          final rest = all.where((w) => !w.greeting).toList();
          _selectedWords = greeting;
          _availableWords = rest;
        } else {
          _availableWords.addAll(all);
        }
        _skipCount += all.length;
        _hasMoreWords = all.length >= 50;
        _loadingWords = false;
      });
    } catch (e) {
      setState(() { _wordsError = e.toString(); _loadingWords = false; });
    }
  }

  void _selectWord(WordSelect w) {
    setState(() {
      _availableWords.remove(w);
      _selectedWords.add(w);
    });
  }

  void _deselectWord(int index) {
    setState(() {
      final w = _selectedWords.removeAt(index);
      _availableWords.insert(0, w);
    });
  }

  void _onReorderSelected(int oldIndex, int newIndex) {
    setState(() {
      if (newIndex > oldIndex) newIndex--;
      final item = _selectedWords.removeAt(oldIndex);
      _selectedWords.insert(newIndex, item);
    });
  }

  Future<void> _saveDraft() async {
    if (_langCode.isEmpty || _toLangCode.isEmpty) return;
    final wordsWithWeight = _selectedWords.asMap().entries
        .map((e) => WordWithWeight(word: e.value.word, weight: e.key))
        .toList();
    try {
      final phaseIndex = _Phase.values.indexOf(_phase);
      if (_draftId != null) {
        await CourseGenerationService.updateDraft(_draftId!,
          title: _titleController.text.trim().isEmpty ? 'New course' : _titleController.text.trim(),
          description: _descController.text.trim(),
          lang: _langCode, toLang: _toLangCode,
          selectedQuestionTypeIds: _selectedQTypeIds.toList(),
          wordsWithWeight: wordsWithWeight, step: phaseIndex,
          lessonsPerModule: _wordsPerModule,
        );
      } else {
        final draft = await CourseGenerationService.saveDraft(
          title: _titleController.text.trim().isEmpty ? 'New course' : _titleController.text.trim(),
          description: _descController.text.trim(),
          lang: _langCode, toLang: _toLangCode,
          selectedQuestionTypeIds: _selectedQTypeIds.toList(),
          wordsWithWeight: wordsWithWeight, step: phaseIndex,
          lessonsPerModule: _wordsPerModule,
        );
        setState(() => _draftId = draft.id);
      }
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Draft saved.')));
    } catch (e) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Save draft failed: $e')));
    }
  }

  // ───────────── navigation ─────────────

  void _goToWordSelect() {
    if (_langCode.isEmpty || _toLangCode.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Select both languages.')));
      return;
    }
    if (_titleController.text.trim().isEmpty) {
      _titleController.text = '${_languageName(_langCode)} for ${_languageName(_toLangCode)} speakers';
    }
    setState(() => _phase = _Phase.wordSelect);
    if (_availableWords.isEmpty && _selectedWords.isEmpty) _loadWords();
  }

  void _goToQuestionTypes() {
    if (_selectedWords.length < 3) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Select at least 3 words.')));
      return;
    }
    setState(() => _phase = _Phase.questionTypes);
  }

  void _startGeneration() {
    if (_selectedWords.isEmpty) return;
    setState(() {
      _phase = _Phase.generating;
      _wordStatus.clear();
      _wordExercises.clear();
      _generating = true;
    });
    _runModuleGeneration();
  }

  Future<void> _runModuleGeneration() async {
    final start = _moduleIndex * _wordsPerModule;
    final end = min(start + _wordsPerModule, _selectedWords.length);
    final moduleWords = _selectedWords.sublist(start, end);

    setState(() {
      for (final w in moduleWords) { _wordStatus[w.word] = 'generating'; }
    });

    try {
      final response = await CourseGenerationService.generateModuleExercises(
        lang: _langCode,
        toLang: _toLangCode,
        words: moduleWords.map((w) => w.word).toList(),
        questionTypes: _selectedQTypeIds.toList(),
        wordsSoFar: List.unmodifiable(_allWordsSoFar),
      );
      setState(() {
        for (final result in response.results) {
          _wordExercises[result.word] = result.exercises;
          _wordStatus[result.word] = 'done(${result.exercises.length})';
        }
        for (final w in moduleWords) {
          _wordExercises.putIfAbsent(w.word, () => []);
          _wordStatus.putIfAbsent(w.word, () => 'done(0)');
        }
      });
    } catch (e) {
      setState(() {
        for (final w in moduleWords) { _wordStatus[w.word] = 'error'; }
      });
    }

    // Detect duplicates across module
    _markDuplicates(moduleWords.map((w) => w.word).toList());
    setState(() => _generating = false);

    // Navigate to module preview
    if (!mounted) return;
    final wordExercisesForModule = moduleWords
        .map((w) => WordExercisesForModule(
              word: w.word,
              exercises: _wordExercises[w.word] ?? [],
            ))
        .toList();

    final result = await Navigator.push<ModuleSaveResult>(
      context,
      MaterialPageRoute(
        builder: (_) => ModulePreviewScreen(
          lang: _langCode,
          toLang: _toLangCode,
          courseTitle: _titleController.text.trim().isEmpty ? 'New course' : _titleController.text.trim(),
          courseDescription: _descController.text.trim(),
          moduleNumber: _moduleIndex + 1,
          initialCourseId: _savedCourseId,
          wordsPerModule: _wordsPerModule,
          wordExercises: wordExercisesForModule,
        ),
      ),
    );

    if (!mounted) return;

    if (result != null) {
      // Collect identify-exercise words into the pool for future modules' distractors
      for (final we in wordExercisesForModule) {
        for (final ex in we.exercises) {
          if (ex.exerciseType == 'identify_words_in_speech') {
            _allWordsSoFar.addAll(ex.correctOptions);
          }
        }
      }
      setState(() {
        _savedCourseId = result.courseId;
        _savedModulesCount++;
        _totalLessons += result.lessonCount;
        _totalExercises += result.exerciseCount;
        _moduleIndex++;
      });
      if (_moduleIndex >= _moduleCount) {
        setState(() => _phase = _Phase.summary);
      } else {
        // Auto-start next module generation
        setState(() {
          _wordStatus.clear();
          _wordExercises.clear();
          _generating = true;
        });
        _runModuleGeneration();
      }
    } else {
      // Back was pressed in preview — return to word selection
      setState(() => _phase = _Phase.wordSelect);
    }
  }

  Set<int> _markDuplicates(List<String> wordList) {
    final toIdCount = <int, int>{};
    for (final word in wordList) {
      for (final ex in _wordExercises[word] ?? []) {
        if (ex.toSentenceId > 0) {
          toIdCount[ex.toSentenceId] = (toIdCount[ex.toSentenceId] ?? 0) + 1;
        }
      }
    }
    return toIdCount.entries.where((e) => e.value > 1).map((e) => e.key).toSet();
  }

  String _languageName(String code) {
    return _languages.firstWhere((l) => l.code == code, orElse: () => CourseOption(code: code, name: code)).name;
  }

  // ───────────── build ─────────────

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        leading: widget.onBackToList != null
            ? IconButton(icon: const Icon(Icons.arrow_back), onPressed: widget.onBackToList)
            : null,
        title: Text(_appBarTitle),
        elevation: 0,
        actions: [
          if (_phase != _Phase.generating && _phase != _Phase.summary)
            TextButton.icon(
              onPressed: _saveDraft,
              icon: const Icon(Icons.save_outlined, size: 18),
              label: const Text('Save draft'),
            ),
        ],
      ),
      body: Column(
        children: [
          if (_phase != _Phase.generating && _phase != _Phase.summary)
            _buildStepIndicator(),
          Expanded(child: _buildBody()),
          _buildNavBar(),
        ],
      ),
    );
  }

  String get _appBarTitle {
    switch (_phase) {
      case _Phase.setup: return 'Step 1: Course setup';
      case _Phase.wordSelect: return 'Step 2: Select words';
      case _Phase.questionTypes: return 'Step 3: Question types';
      case _Phase.generating: return 'Generating Module ${_moduleIndex + 1}...';
      case _Phase.summary: return 'Course created!';
    }
  }

  Widget _buildStepIndicator() {
    const labels = ['1. Setup', '2. Words', '3. Types'];
    final stepIndex = [_Phase.setup, _Phase.wordSelect, _Phase.questionTypes].indexOf(_phase);
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 8),
      color: Theme.of(context).colorScheme.surface,
      child: Row(
        children: List.generate(3, (i) {
          final active = stepIndex == i;
          final done = stepIndex > i;
          return Expanded(
            child: Row(
              children: [
                Expanded(
                  child: Center(
                    child: Text(
                      labels[i],
                      style: TextStyle(
                        fontWeight: active ? FontWeight.bold : FontWeight.normal,
                        color: done
                            ? Colors.green
                            : active
                                ? Theme.of(context).colorScheme.primary
                                : Colors.grey,
                      ),
                    ),
                  ),
                ),
                if (i < 2)
                  Icon(Icons.chevron_right, size: 16, color: Colors.grey[400]),
              ],
            ),
          );
        }),
      ),
    );
  }

  Widget _buildBody() {
    switch (_phase) {
      case _Phase.setup: return _buildSetup();
      case _Phase.wordSelect: return _buildWordSelect();
      case _Phase.questionTypes: return _buildQuestionTypes();
      case _Phase.generating: return _buildGenerating();
      case _Phase.summary: return _buildSummary();
    }
  }

  Widget _buildNavBar() {
    switch (_phase) {
      case _Phase.setup:
        return _navRow(
          right: ElevatedButton(
            onPressed: _loadingOptions ? null : _goToWordSelect,
            child: const Text('Next: Select words →'),
          ),
        );
      case _Phase.wordSelect:
        return _navRow(
          left: TextButton(onPressed: () => setState(() => _phase = _Phase.setup), child: const Text('← Back')),
          right: ElevatedButton(
            onPressed: _loadingWords ? null : _goToQuestionTypes,
            child: const Text('Next: Question types →'),
          ),
        );
      case _Phase.questionTypes:
        return _navRow(
          left: TextButton(onPressed: () => setState(() => _phase = _Phase.wordSelect), child: const Text('← Back')),
          right: ElevatedButton(
            onPressed: _startGeneration,
            child: Text('Generate Module ${_moduleIndex + 1} →'),
          ),
        );
      case _Phase.generating:
        return const SizedBox.shrink();
      case _Phase.summary:
        return _navRow(
          right: ElevatedButton(
            onPressed: () {
              if (_savedCourseId > 0) {
                Navigator.push(context, MaterialPageRoute(
                  builder: (_) => CourseReviewScreen(courseId: _savedCourseId),
                ));
              }
            },
            child: const Text('View Full Course →'),
          ),
        );
    }
  }

  Widget _navRow({Widget? left, Widget? right}) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [left ?? const SizedBox(), right ?? const SizedBox()],
      ),
    );
  }

  // ───────────── Step 1: Setup ─────────────

  Widget _buildSetup() {
    if (_loadingOptions) return const Center(child: CircularProgressIndicator());
    if (_optionsError != null) {
      return Center(
        child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
          Text(_optionsError!, textAlign: TextAlign.center),
          const SizedBox(height: 16),
          ElevatedButton(onPressed: _loadCourseOptions, child: const Text('Retry')),
        ]),
      );
    }
    return SingleChildScrollView(
      padding: const EdgeInsets.all(24),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        const Text('Languages', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
        const SizedBox(height: 8),
        Row(children: [
          const Text('Target language: '),
          DropdownButton<String>(
            value: _langCode,
            items: _languages.map((l) => DropdownMenuItem(value: l.code, child: Text(l.name))).toList(),
            onChanged: (v) { if (v != null) setState(() { _langCode = v; _titleController.clear(); }); },
          ),
          const SizedBox(width: 24),
          const Text('Native language: '),
          DropdownButton<String>(
            value: _toLangCode,
            items: _languages.map((l) => DropdownMenuItem(value: l.code, child: Text(l.name))).toList(),
            onChanged: (v) { if (v != null) setState(() { _toLangCode = v; _titleController.clear(); }); },
          ),
        ]),
        const SizedBox(height: 16),
        const Text('Course title', style: TextStyle(fontWeight: FontWeight.bold)),
        const SizedBox(height: 4),
        TextField(
          controller: _titleController,
          decoration: InputDecoration(
            hintText: '${_languageName(_langCode)} for ${_languageName(_toLangCode)} speakers',
            border: const OutlineInputBorder(),
          ),
        ),
        const SizedBox(height: 12),
        const Text('Description (optional)', style: TextStyle(fontWeight: FontWeight.bold)),
        const SizedBox(height: 4),
        TextField(
          controller: _descController,
          maxLines: 2,
          decoration: const InputDecoration(hintText: 'Course description...', border: OutlineInputBorder()),
        ),
      ]),
    );
  }

  // ───────────── Step 2: Word selection ─────────────

  Widget _buildWordSelect() {
    final count = _selectedWords.length;
    final modules = _moduleCount;
    return Column(children: [
      // Header bar
      Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        color: Colors.grey[100],
        child: Row(children: [
          Text(
            '$count word${count == 1 ? '' : 's'} selected · $modules module${modules == 1 ? '' : 's'}',
            style: const TextStyle(fontWeight: FontWeight.bold),
          ),
          const Spacer(),
          const Text('Per module: '),
          SizedBox(
            width: 56,
            child: TextField(
              keyboardType: TextInputType.number,
              controller: TextEditingController(text: '$_wordsPerModule')
                ..selection = TextSelection.collapsed(offset: '$_wordsPerModule'.length),
              onChanged: (s) { final v = int.tryParse(s); if (v != null && v > 0) setState(() => _wordsPerModule = v); },
              decoration: const InputDecoration(isDense: true, contentPadding: EdgeInsets.symmetric(horizontal: 8, vertical: 8)),
            ),
          ),
        ]),
      ),
      if (_wordsError != null)
        Padding(
          padding: const EdgeInsets.all(8),
          child: Text(_wordsError!, style: const TextStyle(color: Colors.red)),
        ),
      Expanded(
        child: _loadingWords && _selectedWords.isEmpty && _availableWords.isEmpty
            ? const Center(child: CircularProgressIndicator())
            : Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
                // Left panel: selected words (reorderable)
                Expanded(child: _buildSelectedWordsPanel()),
                const VerticalDivider(width: 1),
                // Right panel: available words
                Expanded(child: _buildAvailableWordsPanel()),
              ]),
      ),
    ]);
  }

  Widget _buildSelectedWordsPanel() {
    return Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Padding(
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
        child: Text(
          'Selected (${_selectedWords.length})',
          style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.green),
        ),
      ),
      Expanded(
        child: _selectedWords.isEmpty
            ? Center(
                child: Text('No words selected.\nClick + in the right panel.',
                    textAlign: TextAlign.center, style: TextStyle(color: Colors.grey[500])))
            : ReorderableListView.builder(
                padding: const EdgeInsets.only(bottom: 8),
                itemCount: _selectedWords.length,
                onReorder: _onReorderSelected,
                itemBuilder: (ctx, index) {
                  final word = _selectedWords[index];
                  final isModuleStart = index % _wordsPerModule == 0;
                  final moduleNum = index ~/ _wordsPerModule + 1;
                  return _buildSelectedTile(
                    key: ValueKey(word.word),
                    index: index,
                    word: word,
                    isModuleStart: isModuleStart,
                    moduleNum: moduleNum,
                  );
                },
              ),
      ),
    ]);
  }

  Widget _buildSelectedTile({
    required Key key,
    required int index,
    required WordSelect word,
    required bool isModuleStart,
    required int moduleNum,
  }) {
    return Column(
      key: key,
      crossAxisAlignment: CrossAxisAlignment.stretch,
      mainAxisSize: MainAxisSize.min,
      children: [
        if (isModuleStart)
          Container(
            padding: const EdgeInsets.symmetric(vertical: 3, horizontal: 12),
            color: Colors.deepPurple[50],
            child: Text(
              '── Module $moduleNum ──',
              style: TextStyle(fontSize: 11, color: Colors.deepPurple[400], fontWeight: FontWeight.w600),
            ),
          ),
        ListTile(
          dense: true,
          leading: ReorderableDragStartListener(
            index: index,
            child: const Icon(Icons.drag_handle, size: 20, color: Colors.grey),
          ),
          title: _wordTitle(word),
          subtitle: Text('${word.sentencesCount} sentences', style: const TextStyle(fontSize: 11)),
          trailing: IconButton(
            icon: const Icon(Icons.remove_circle_outline, size: 18, color: Colors.red),
            onPressed: () => _deselectWord(index),
          ),
        ),
      ],
    );
  }

  Widget _buildAvailableWordsPanel() {
    return Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Padding(
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
        child: Row(children: [
          Text('Available (${_availableWords.length})', style: const TextStyle(fontWeight: FontWeight.bold)),
          const Spacer(),
          if (_loadingWords) const SizedBox(width: 16, height: 16, child: CircularProgressIndicator(strokeWidth: 2)),
          if (!_loadingWords && _availableWords.isEmpty)
            TextButton.icon(
              onPressed: () => _loadWords(),
              icon: const Icon(Icons.download, size: 16),
              label: const Text('Load'),
            ),
        ]),
      ),
      Expanded(
        child: ListView.builder(
          itemCount: _availableWords.length + (_hasMoreWords && _availableWords.isNotEmpty ? 1 : 0),
          itemBuilder: (ctx, index) {
            if (index == _availableWords.length) {
              return TextButton.icon(
                onPressed: _loadingWords ? null : () => _loadWords(loadMore: true),
                icon: const Icon(Icons.expand_more, size: 16),
                label: const Text('Load more'),
              );
            }
            final word = _availableWords[index];
            return ListTile(
              dense: true,
              leading: IconButton(
                icon: const Icon(Icons.add_circle_outline, size: 20, color: Colors.green),
                onPressed: () => _selectWord(word),
              ),
              title: _wordTitle(word),
              subtitle: Text('${word.sentencesCount} sentences', style: const TextStyle(fontSize: 11)),
            );
          },
        ),
      ),
    ]);
  }

  Widget _wordTitle(WordSelect word) {
    return Row(children: [
      Text(word.word, style: const TextStyle(fontWeight: FontWeight.bold)),
      if (word.pos.isNotEmpty) ...[
        const SizedBox(width: 6),
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 5, vertical: 1),
          decoration: BoxDecoration(color: Colors.blue[50], borderRadius: BorderRadius.circular(3)),
          child: Text(word.pos, style: const TextStyle(fontSize: 10)),
        ),
      ],
      if (word.greeting) ...[
        const SizedBox(width: 4),
        const Icon(Icons.star, size: 13, color: Colors.amber),
      ],
    ]);
  }

  // ───────────── Step 3: Question types ─────────────

  Widget _buildQuestionTypes() {
    final sentence = _questionTypes.where((qt) => qt.applicableTo == 'sentence').toList();
    final alphabet = _questionTypes.where((qt) => qt.applicableTo == 'alphabet').toList();
    return SingleChildScrollView(
      padding: const EdgeInsets.all(24),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text(
          '${_moduleCount} module${_moduleCount == 1 ? '' : 's'} · '
          '${_selectedWords.length} word${_selectedWords.length == 1 ? '' : 's'}',
          style: TextStyle(color: Colors.grey[600]),
        ),
        const SizedBox(height: 20),
        _buildQTypesSection('Sentence exercises', sentence),
        const SizedBox(height: 16),
        _buildQTypesSection('Alphabet exercises', alphabet),
      ]),
    );
  }

  Widget _buildQTypesSection(String title, List<QuestionTypeOption> types) {
    if (types.isEmpty) return const SizedBox.shrink();
    return Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Text(title, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
      const SizedBox(height: 4),
      ...types.map((qt) => SwitchListTile(
            title: Text(qt.name),
            subtitle: qt.description.isNotEmpty ? Text(qt.description) : null,
            value: _selectedQTypeIds.contains(qt.id),
            onChanged: (v) => setState(() => v ? _selectedQTypeIds.add(qt.id) : _selectedQTypeIds.remove(qt.id)),
          )),
    ]);
  }

  // ───────────── Generation progress ─────────────

  Widget _buildGenerating() {
    final start = _moduleIndex * _wordsPerModule;
    final end = min(start + _wordsPerModule, _selectedWords.length);
    final moduleWords = _selectedWords.sublist(start, end);
    final doneCount = moduleWords.where((w) => _wordStatus[w.word]?.startsWith('done') == true).length;

    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(mainAxisSize: MainAxisSize.min, crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text(
            'Generating Module ${_moduleIndex + 1} of $_moduleCount',
            style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 24),
          ...moduleWords.map((word) {
            final status = _wordStatus[word.word] ?? 'pending';
            return Padding(
              padding: const EdgeInsets.symmetric(vertical: 4),
              child: Row(children: [
                _statusIcon(status),
                const SizedBox(width: 12),
                Expanded(child: Text(word.word, style: const TextStyle(fontWeight: FontWeight.bold))),
                Text(_statusLabel(status), style: TextStyle(color: Colors.grey[600], fontSize: 12)),
              ]),
            );
          }),
          const SizedBox(height: 24),
          LinearProgressIndicator(value: moduleWords.isEmpty ? 0 : doneCount / moduleWords.length),
          const SizedBox(height: 8),
          Text('$doneCount / ${moduleWords.length} words', style: TextStyle(color: Colors.grey[600])),
        ]),
      ),
    );
  }

  Widget _statusIcon(String status) {
    if (status == 'pending') return const Icon(Icons.circle_outlined, size: 18, color: Colors.grey);
    if (status == 'generating') return const SizedBox(width: 18, height: 18, child: CircularProgressIndicator(strokeWidth: 2));
    if (status.startsWith('done')) return const Icon(Icons.check_circle, size: 18, color: Colors.green);
    return const Icon(Icons.error_outline, size: 18, color: Colors.red);
  }

  String _statusLabel(String status) {
    if (status == 'pending') return 'waiting...';
    if (status == 'generating') return 'generating...';
    if (status.startsWith('done')) {
      final n = status.replaceAll(RegExp(r'done\(|\)'), '');
      return '$n exercises';
    }
    return 'error';
  }

  // ───────────── Summary ─────────────

  Widget _buildSummary() {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(mainAxisSize: MainAxisSize.min, children: [
          const Icon(Icons.check_circle, size: 72, color: Colors.green),
          const SizedBox(height: 16),
          Text(
            _titleController.text.isEmpty ? 'Course created!' : _titleController.text,
            style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 8),
          Text(
            '$_savedModulesCount module${_savedModulesCount == 1 ? '' : 's'} · '
            '$_totalLessons lesson${_totalLessons == 1 ? '' : 's'} · '
            '$_totalExercises exercise${_totalExercises == 1 ? '' : 's'}',
            style: TextStyle(fontSize: 16, color: Colors.grey[600]),
          ),
          const SizedBox(height: 32),
          if (widget.onBackToList != null)
            TextButton(onPressed: widget.onBackToList, child: const Text('Back to courses')),
        ]),
      ),
    );
  }
}

// ═══════════════════════════════════════════════════
// Wrapper: show draft list or wizard
// ═══════════════════════════════════════════════════

class EditorCreateCourseScreen extends StatefulWidget {
  const EditorCreateCourseScreen({super.key});

  @override
  State<EditorCreateCourseScreen> createState() => _EditorCreateCourseScreenState();
}

class _EditorCreateCourseScreenState extends State<EditorCreateCourseScreen> {
  bool _showFlow = false;
  int? _draftId;

  @override
  Widget build(BuildContext context) {
    if (_showFlow) {
      return EditorFlowScreen(
        draftId: _draftId,
        onBackToList: () => setState(() { _showFlow = false; _draftId = null; }),
      );
    }
    return _DraftListScreen(
      onStartNew: () => setState(() { _showFlow = true; _draftId = null; }),
      onResumeDraft: (id) => setState(() { _showFlow = true; _draftId = id; }),
    );
  }
}

// ═══════════════════════════════════════════════════
// Draft list screen
// ═══════════════════════════════════════════════════

class _DraftListScreen extends StatefulWidget {
  const _DraftListScreen({required this.onStartNew, required this.onResumeDraft});
  final VoidCallback onStartNew;
  final void Function(int id) onResumeDraft;

  @override
  State<_DraftListScreen> createState() => _DraftListScreenState();
}

class _DraftListScreenState extends State<_DraftListScreen> {
  List<EditorDraftListItem> _drafts = [];
  bool _loading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _loadDrafts();
  }

  Future<void> _loadDrafts() async {
    setState(() { _loading = true; _error = null; });
    try {
      final list = await CourseGenerationService.listDrafts();
      if (mounted) setState(() { _drafts = list; _loading = false; });
    } catch (e) {
      if (mounted) setState(() { _error = e.toString(); _loading = false; });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Create Course'), elevation: 0),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
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
            Text(_error!, style: const TextStyle(color: Colors.red))
          else if (_drafts.isEmpty)
            Text('No drafts yet.', style: TextStyle(color: Colors.grey[600]))
          else
            ListView.separated(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: _drafts.length,
              separatorBuilder: (_, __) => const SizedBox(height: 8),
              itemBuilder: (context, i) {
                final d = _drafts[i];
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
        ]),
      ),
    );
  }
}
