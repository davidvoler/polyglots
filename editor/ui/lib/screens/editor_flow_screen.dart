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

  // Step 2: Words (greetings + common)
  List<WordSelect> _greetingWords = [];
  List<WordCount> _commonWords = [];
  final List<String> _selectedWords = [];
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
        _langCode ??= _languages.isNotEmpty ? _languages.first.code : null;
        _toLangCode ??= _languages.length > 1 ? _languages[1].code : _languages.first.code;
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
      final greetingModules = await CourseGenerationService.getGreetingWords(lang: _langCode!);
      final common = await CourseGenerationService.getCommonWords(lang: _langCode!, limit: 200);
      List<WordSelect> greeting = [];
      for (final m in greetingModules) {
        greeting.addAll(m.words);
      }
      setState(() {
        _greetingWords = greeting;
        _commonWords = common;
        _loadingWords = false;
      });
    } catch (e) {
      setState(() {
        _wordsError = e.toString();
        _loadingWords = false;
      });
    }
  }

  void _toggleWord(String word) {
    setState(() {
      if (_selectedWords.contains(word)) {
        _selectedWords.remove(word);
      } else {
        _selectedWords.add(word);
      }
    });
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
    if (_langCode == null || _toLangCode == null || _selectedWords.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Set languages and select at least one word.')),
      );
      return;
    }
    setState(() {
      _creating = true;
      _createResult = null;
    });
    try {
      final result = await CourseGenerationService.createCourseFromEditor(
        lang: _langCode!,
        toLang: _toLangCode!,
        title: _titleController.text.trim().isEmpty ? 'New course' : _titleController.text.trim(),
        description: _descriptionController.text.trim(),
        selectedWords: _selectedWords,
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
                child: Text(_loadingWords ? 'Loading...' : 'Load words'),
              ),
            ],
          ),
          if (_wordsError != null) Padding(padding: const EdgeInsets.only(top: 8), child: Text(_wordsError!, style: const TextStyle(color: Colors.red))),
          const SizedBox(height: 16),
          const Text('2a. Greeting / polite words', style: TextStyle(fontWeight: FontWeight.bold)),
          ..._greetingWords.map((w) => ListTile(
                title: Text(w.word),
                trailing: Icon(_selectedWords.contains(w.word) ? Icons.check_circle : Icons.radio_button_unchecked),
                onTap: () => _toggleWord(w.word),
              )),
          const SizedBox(height: 16),
          const Text('2b. Common words (most common first)', style: TextStyle(fontWeight: FontWeight.bold)),
          ..._commonWords.take(100).map((w) => ListTile(
                title: Text('${w.word} (${w.cnt})'),
                trailing: Icon(_selectedWords.contains(w.word) ? Icons.check_circle : Icons.radio_button_unchecked),
                onTap: () => _toggleWord(w.word),
              )),
          if (_selectedWords.isNotEmpty)
            Padding(
              padding: const EdgeInsets.only(top: 16),
              child: Text('Selected: ${_selectedWords.length} words', style: const TextStyle(fontWeight: FontWeight.bold)),
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
          Text('Selected words: ${_selectedWords.length}. Sentence selection per word can be added in a follow-up (open each word → load sentences → pick ~10).', style: TextStyle(color: Colors.grey[600])),
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
          Text('Words: ${_selectedWords.length}. Modules: ${(_selectedWords.length / _lessonsPerModule).ceil()} (${_lessonsPerModule} lessons per module).'),
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
              onPressed: () {
                if (_step == 0 && _langCode != null) _loadWords();
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
