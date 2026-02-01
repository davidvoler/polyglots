import 'package:flutter/material.dart';
import '../services/course_generation_service.dart';

/// Editor flow: 1) Course options  2) Select/reorder words  3) Sentences + question types  4) Group into modules & create
class EditorFlowScreen extends StatefulWidget {
  const EditorFlowScreen({super.key});

  @override
  State<EditorFlowScreen> createState() => _EditorFlowScreenState();
}

class _EditorFlowScreenState extends State<EditorFlowScreen> {
  int _step = 0;
  final PageController _pageController = PageController();

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

  // Step 3: Sentences per word (simplified: we store word -> count or use automate)
  bool _automateLesson = false;
  final Map<String, List<int>> _sentencesPerWord = {};
  int _lessonsPerModule = 10;

  // Step 4: Create
  bool _creating = false;
  String? _createResult;

  @override
  void initState() {
    super.initState();
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
    } catch (e) {
      setState(() {
        _optionsError = e.toString();
        _loadingOptions = false;
      });
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
        title: const Text('Create course (4 steps)'),
        elevation: 0,
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
    return SingleChildScrollView(
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
          const SizedBox(height: 8),
          if (_allWords.isEmpty)
            const Text('Load words to see list.')
          else
            ReorderableListView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: _allWords.length,
              onReorder: _onReorder,
              itemBuilder: (context, index) {
                final w = _allWords[index];
                return Card(
                  key: ValueKey('${w.word}_$index'),
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
        ],
      ),
    );
  }

  Widget _buildStep3() {
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
            onChanged: (s) => _lessonsPerModule = int.tryParse(s) ?? 10,
            decoration: InputDecoration(
              hintText: '$_lessonsPerModule',
              suffixText: 'lessons per module',
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildStep4() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(24),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('4. Group lessons into modules and create course', style: TextStyle(fontWeight: FontWeight.bold)),
          const SizedBox(height: 16),
          Text('Words: ${_allWords.length}. Modules: ${(_allWords.length / _lessonsPerModule).ceil()} (${_lessonsPerModule} lessons per module).'),
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
              onPressed: () {
                _pageController.previousPage(duration: const Duration(milliseconds: 200), curve: Curves.easeInOut);
                setState(() => _step--);
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
