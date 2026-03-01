import 'package:flutter/material.dart';
import '../services/course_generation_service.dart';

class GenerateCourseWizardScreen extends StatefulWidget {
  const GenerateCourseWizardScreen({super.key});

  @override
  State<GenerateCourseWizardScreen> createState() => _GenerateCourseWizardScreenState();
}

class _GenerateCourseWizardScreenState extends State<GenerateCourseWizardScreen> {
  int _currentStep = 0;
  final PageController _pageController = PageController();
  
  // Step 1: Language Selection
  String? _selectedLanguage;
  String? _selectedStudentLanguage;
  
  // Step 2: Course Goals
  final Set<String> _selectedGoals = {};
  final TextEditingController _courseDescriptionController = TextEditingController();
  
  // Step 3: Student Levels
  double _readingLevel = 1.0;
  double _writingLevel = 1.0;
  double _vocabularyLevel = 1.0;
  double _speakingLevel = 1.0;
  double _hiraganaLevel = 1.0;
  double _kanjiLevel = 1.0;
  double _katakanaLevel = 1.0;
  
  // Step 4: Course Structure
  final TextEditingController _numberOfLessonsController = TextEditingController();
  final TextEditingController _newWordsPerLessonController = TextEditingController();
  final TextEditingController _wordsIncreaseFactorController = TextEditingController(text: '0.3');
  final TextEditingController _sentenceLengthStartController = TextEditingController(text: '3');
  final TextEditingController _sentenceLengthIncreaseFactorController = TextEditingController(text: '0.1');
  final TextEditingController _grammarPerModuleController = TextEditingController(text: '1');
  
  // Step 4: Word Selection
  final TextEditingController _wordsPerModuleController = TextEditingController(text: '5');
  final TextEditingController _ratioIncreaseController = TextEditingController(text: '0.08');
  final TextEditingController _skipCountController = TextEditingController(text: '0');
  List<ModuleWords> _selectedModules = [];
  bool _isLoadingWords = false;

  // Step 6: Advanced Options
  bool _greetingModule = true;
  bool _readingModule = false;
  bool _readingExercises = false;
  bool _writingExercises = false;
  
  // Loading state
  bool _isGenerating = false;

  final List<String> _languages = [
    'English',
    'Spanish',
    'French',
    'German',
    'Italian',
    'Portuguese',
    'Japanese',
    'Chinese',
    'Korean',
    'Arabic',
    'Russian',
    'Hindi',
    'Turkish',
    'Polish',
    'Dutch',
    'Swedish',
    'Norwegian',
    'Danish',
    'Finnish',
    'Greek',
    'Czech',
    'Romanian',
    'Hungarian',
    'Thai',
    'Vietnamese',
    'Indonesian',
  ];

  bool get _isJapanese => _selectedLanguage == 'Japanese';

  @override
  void dispose() {
    _pageController.dispose();
    _courseDescriptionController.dispose();
    _numberOfLessonsController.dispose();
    _newWordsPerLessonController.dispose();
    _wordsIncreaseFactorController.dispose();
    _sentenceLengthStartController.dispose();
    _sentenceLengthIncreaseFactorController.dispose();
    _grammarPerModuleController.dispose();
    _wordsPerModuleController.dispose();
    _ratioIncreaseController.dispose();
    _skipCountController.dispose();
    super.dispose();
  }

  List<WizardStep> get _steps => [
    WizardStep(
      title: 'Language Selection',
      subtitle: 'Choose the target language and student\'s native language',
      content: _buildLanguageStep(),
    ),
    WizardStep(
      title: 'Course Goals',
      subtitle: 'Define the purpose and goals of your course',
      content: _buildGoalsStep(),
    ),
    WizardStep(
      title: 'Student Levels',
      subtitle: 'Set the skill levels for your students',
      content: _buildLevelsStep(),
    ),
    WizardStep(
      title: 'Word Selection',
      subtitle: 'Select words for modules from the database',
      content: _buildWordSelectionStep(),
    ),
    WizardStep(
      title: 'Course Structure',
      subtitle: 'Configure lessons and vocabulary progression',
      content: _buildStructureStep(),
    ),
    WizardStep(
      title: 'Advanced Options',
      subtitle: 'Customize course features',
      content: _buildAdvancedStep(),
    ),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Generate Course with AI'),
        automaticallyImplyLeading: false,
        elevation: 0,
      ),
      body: Column(
        children: [
          // Step Indicator
          _buildStepIndicator(),
          
          // Content Area
          Expanded(
            child: PageView.builder(
              controller: _pageController,
              physics: const NeverScrollableScrollPhysics(), // Disable swipe
              itemCount: _steps.length,
              itemBuilder: (context, index) {
                return SingleChildScrollView(
                  padding: const EdgeInsets.all(24.0),
                  child: _steps[index].content,
                );
              },
            ),
          ),
          
          // Navigation Buttons
          _buildNavigationButtons(),
        ],
      ),
    );
  }

  Widget _buildStepIndicator() {
    return Container(
      padding: const EdgeInsets.all(16.0),
      decoration: BoxDecoration(
        color: Theme.of(context).colorScheme.surface,
        border: Border(
          bottom: BorderSide(
            color: Colors.grey[300]!,
            width: 1,
          ),
        ),
      ),
      child: Row(
        children: List.generate(_steps.length, (index) {
          final isActive = index == _currentStep;
          final isCompleted = index < _currentStep;
          
          return Expanded(
            child: Column(
              children: [
                Container(
                  width: 32,
                  height: 32,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: isActive || isCompleted
                        ? Theme.of(context).colorScheme.primary
                        : Colors.grey[300],
                  ),
                  child: Center(
                    child: isCompleted
                        ? const Icon(Icons.check, color: Colors.white, size: 20)
                        : Text(
                            '${index + 1}',
                            style: TextStyle(
                              color: isActive ? Colors.white : Colors.grey[600],
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  _steps[index].title,
                  style: TextStyle(
                    fontSize: 10,
                    fontWeight: isActive ? FontWeight.bold : FontWeight.normal,
                    color: isActive || isCompleted
                        ? Theme.of(context).colorScheme.primary
                        : Colors.grey[600],
                  ),
                  textAlign: TextAlign.center,
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
              ],
            ),
          );
        }),
      ),
    );
  }

  Widget _buildNavigationButtons() {
    return Container(
      padding: const EdgeInsets.all(16.0),
      decoration: BoxDecoration(
        color: Theme.of(context).colorScheme.surface,
        border: Border(
          top: BorderSide(
            color: Colors.grey[300]!,
            width: 1,
          ),
        ),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          if (_currentStep > 0)
            TextButton.icon(
              onPressed: _previousStep,
              icon: const Icon(Icons.arrow_back),
              label: const Text('Previous'),
            )
          else
            const SizedBox(width: 100),
          
          if (_currentStep < _steps.length - 1)
            ElevatedButton.icon(
              onPressed: _nextStep,
              icon: const Icon(Icons.arrow_forward),
              label: const Text('Next'),
            )
          else
            ElevatedButton.icon(
              onPressed: _isGenerating ? null : _generateCourse,
              icon: _isGenerating
                  ? const SizedBox(
                      width: 20,
                      height: 20,
                      child: CircularProgressIndicator(
                        strokeWidth: 2,
                        valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                      ),
                    )
                  : const Icon(Icons.auto_awesome),
              label: Text(_isGenerating ? 'Generating...' : 'Generate Course'),
            ),
        ],
      ),
    );
  }

  void _nextStep() {
    if (_currentStep < _steps.length - 1) {
      setState(() {
        _currentStep++;
      });
      _pageController.nextPage(
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeInOut,
      );
    }
  }

  void _previousStep() {
    if (_currentStep > 0) {
      setState(() {
        _currentStep--;
      });
      _pageController.previousPage(
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeInOut,
      );
    }
  }

  Future<void> _loadWordsForModules() async {
    if (_selectedLanguage == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Please select a language first'),
          backgroundColor: Colors.red,
        ),
      );
      return;
    }

    setState(() {
      _isLoadingWords = true;
    });

    try {
      final langCode = CourseGenerationService.getLanguageCode(_selectedLanguage!);
      final wordsPerModules = int.tryParse(_wordsPerModuleController.text) ?? 5;
      final ratioIncrease = double.tryParse(_ratioIncreaseController.text) ?? 0.08;
      final skipCount = int.tryParse(_skipCountController.text) ?? 0;

      final modules = await CourseGenerationService.selectWordsForModules(
        lang: langCode,
        wordsPerModules: wordsPerModules,
        ratioIncrease: ratioIncrease,
        skipCount: skipCount,
      );

      setState(() {
        _selectedModules = modules;
        _isLoadingWords = false;
      });

      if (modules.isEmpty) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('No modules found with the current parameters'),
            backgroundColor: Colors.orange,
          ),
        );
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Loaded ${modules.length} modules with words'),
            backgroundColor: Colors.green,
          ),
        );
      }
    } catch (e) {
      setState(() {
        _isLoadingWords = false;
      });

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Error loading words: $e'),
          backgroundColor: Colors.red,
          duration: const Duration(seconds: 5),
        ),
      );
    }
  }

  // Step 1: Language Selection
  Widget _buildLanguageStep() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Choose the target language and student\'s native language',
          style: Theme.of(context).textTheme.bodyLarge?.copyWith(
            color: Colors.grey[600],
          ),
        ),
        const SizedBox(height: 24),
        _buildDropdownField(
          'Target Language',
          _selectedLanguage,
          (value) => setState(() => _selectedLanguage = value),
        ),
        const SizedBox(height: 16),
        _buildDropdownField(
          'Student\'s Native Language',
          _selectedStudentLanguage,
          (value) => setState(() => _selectedStudentLanguage = value),
        ),
      ],
    );
  }

  // Step 2: Course Goals
  Widget _buildGoalsStep() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Define the purpose and goals of your course',
          style: Theme.of(context).textTheme.bodyLarge?.copyWith(
            color: Colors.grey[600],
          ),
        ),
        const SizedBox(height: 24),
        const Text(
          'Course Goals (select all that apply):',
          style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
        ),
        const SizedBox(height: 12),
        _buildCheckboxTile('Exam preparation', 'exam'),
        _buildCheckboxTile('Daily conversation', 'daily'),
        _buildCheckboxTile('Business communication', 'business'),
        _buildCheckboxTile('Travel situations', 'travel'),
        _buildCheckboxTile('Cultural interest', 'hobby'),
        const SizedBox(height: 24),
        TextField(
          controller: _courseDescriptionController,
          maxLines: 4,
          decoration: InputDecoration(
            labelText: 'Course Description (optional)',
            hintText: 'Describe your course goals in detail...',
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(8),
            ),
          ),
        ),
      ],
    );
  }

  // Step 3: Student Levels
  Widget _buildLevelsStep() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Set the skill levels for your students',
          style: Theme.of(context).textTheme.bodyLarge?.copyWith(
            color: Colors.grey[600],
          ),
        ),
        const SizedBox(height: 24),
        _buildSkillSlider('Reading', _readingLevel, (value) {
          setState(() => _readingLevel = value);
        }),
        _buildSkillSlider('Writing', _writingLevel, (value) {
          setState(() => _writingLevel = value);
        }),
        _buildSkillSlider('Vocabulary', _vocabularyLevel, (value) {
          setState(() => _vocabularyLevel = value);
        }),
        _buildSkillSlider('Speaking', _speakingLevel, (value) {
          setState(() => _speakingLevel = value);
        }),
        if (_isJapanese) ...[
          const SizedBox(height: 24),
          const Divider(),
          const SizedBox(height: 24),
          const Text(
            'Japanese-Specific Levels',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 16),
          _buildSkillSlider('Hiragana', _hiraganaLevel, (value) {
            setState(() => _hiraganaLevel = value);
          }),
          _buildSkillSlider('Kanji', _kanjiLevel, (value) {
            setState(() => _kanjiLevel = value);
          }),
          _buildSkillSlider('Katakana', _katakanaLevel, (value) {
            setState(() => _katakanaLevel = value);
          }),
        ],
      ],
    );
  }

  // Step 4: Word Selection
  Widget _buildWordSelectionStep() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Select words for modules from the database',
          style: Theme.of(context).textTheme.bodyLarge?.copyWith(
            color: Colors.grey[600],
          ),
        ),
        const SizedBox(height: 24),
        const Text(
          'Word Selection Parameters',
          style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600),
        ),
        const SizedBox(height: 16),
        TextField(
          controller: _wordsPerModuleController,
          decoration: InputDecoration(
            labelText: 'Words per Module',
            hintText: 'Number of words to select for each module',
            helperText: 'Default: 5',
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(8),
            ),
          ),
          keyboardType: TextInputType.number,
        ),
        const SizedBox(height: 16),
        TextField(
          controller: _ratioIncreaseController,
          decoration: InputDecoration(
            labelText: 'Ratio Increase Factor',
            hintText: 'How much to increase words per module',
            helperText: 'Default: 0.08 (e.g., 5 → 5.4 → 5.8)',
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(8),
            ),
          ),
          keyboardType: const TextInputType.numberWithOptions(decimal: true),
        ),
        const SizedBox(height: 16),
        TextField(
          controller: _skipCountController,
          decoration: InputDecoration(
            labelText: 'Skip Count',
            hintText: 'Number of words to skip from the beginning',
            helperText: 'Default: 0 (start from most common words)',
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(8),
            ),
          ),
          keyboardType: TextInputType.number,
        ),
        const SizedBox(height: 24),
        SizedBox(
          width: double.infinity,
          child: ElevatedButton.icon(
            onPressed: _isLoadingWords ? null : _loadWordsForModules,
            icon: _isLoadingWords
                ? const SizedBox(
                    width: 20,
                    height: 20,
                    child: CircularProgressIndicator(
                      strokeWidth: 2,
                      valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                    ),
                  )
                : const Icon(Icons.search),
            label: Text(_isLoadingWords ? 'Loading...' : 'Load Word Modules'),
            style: ElevatedButton.styleFrom(
              padding: const EdgeInsets.symmetric(vertical: 16),
            ),
          ),
        ),
        const SizedBox(height: 24),
        if (_selectedModules.isNotEmpty) ...[
          const Text(
            'Selected Modules Preview',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600),
          ),
          const SizedBox(height: 16),
          Container(
            constraints: const BoxConstraints(maxHeight: 400),
            decoration: BoxDecoration(
              border: Border.all(color: Colors.grey[300]!),
              borderRadius: BorderRadius.circular(8),
            ),
            child: ListView.builder(
              shrinkWrap: true,
              itemCount: _selectedModules.length,
              itemBuilder: (context, index) {
                final module = _selectedModules[index];
                return ExpansionTile(
                  title: Text(
                    '${module.name} (${module.wordCount} words)',
                    style: const TextStyle(fontWeight: FontWeight.w500),
                  ),
                  children: [
                    Padding(
                      padding: const EdgeInsets.all(16),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Words in this module:',
                            style: TextStyle(
                              fontWeight: FontWeight.w500,
                              color: Colors.grey[700],
                            ),
                          ),
                          const SizedBox(height: 8),
                          Wrap(
                            spacing: 8,
                            runSpacing: 8,
                            children: module.words.map((word) {
                              return Chip(
                                label: Text(
                                  '${word.word} (${word.pos})',
                                  style: const TextStyle(fontSize: 12),
                                ),
                                backgroundColor: Colors.blue[50],
                              );
                            }).toList(),
                          ),
                        ],
                      ),
                    ),
                  ],
                );
              },
            ),
          ),
        ],
      ],
    );
  }

  // Step 5: Course Structure
  Widget _buildStructureStep() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Configure lessons and vocabulary',
          style: Theme.of(context).textTheme.bodyLarge?.copyWith(
            color: Colors.grey[600],
          ),
        ),
        const SizedBox(height: 24),
        TextField(
          controller: _numberOfLessonsController,
          decoration: InputDecoration(
            labelText: 'Number of Lessons (optional)',
            hintText: 'Enter number of lessons',
            helperText: 'Leave empty for default',
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(8),
            ),
          ),
          keyboardType: TextInputType.number,
        ),
        const SizedBox(height: 16),
        TextField(
          controller: _newWordsPerLessonController,
          decoration: InputDecoration(
            labelText: 'Words per Module (Start)',
            hintText: 'Enter starting number of words per module',
            helperText: 'Default: 2',
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(8),
            ),
          ),
          keyboardType: const TextInputType.numberWithOptions(decimal: true),
        ),
        const SizedBox(height: 16),
        TextField(
          controller: _wordsIncreaseFactorController,
          decoration: InputDecoration(
            labelText: 'Words Increase Factor',
            hintText: 'How much to increase words per module',
            helperText: 'Default: 0.3 (e.g., 2 → 2.3 → 2.6)',
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(8),
            ),
          ),
          keyboardType: const TextInputType.numberWithOptions(decimal: true),
        ),
        const SizedBox(height: 16),
        TextField(
          controller: _sentenceLengthStartController,
          decoration: InputDecoration(
            labelText: 'Sentence Length (Start)',
            hintText: 'Starting sentence length',
            helperText: 'Default: 3 words',
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(8),
            ),
          ),
          keyboardType: TextInputType.number,
        ),
        const SizedBox(height: 16),
        TextField(
          controller: _sentenceLengthIncreaseFactorController,
          decoration: InputDecoration(
            labelText: 'Sentence Length Increase Factor',
            hintText: 'How much to increase sentence length',
            helperText: 'Default: 0.1 (e.g., 3 → 3.1 → 3.2)',
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(8),
            ),
          ),
          keyboardType: const TextInputType.numberWithOptions(decimal: true),
        ),
        const SizedBox(height: 16),
        TextField(
          controller: _grammarPerModuleController,
          decoration: InputDecoration(
            labelText: 'Grammar Points per Module',
            hintText: 'Number of grammar explanations per module',
            helperText: 'Default: 1',
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(8),
            ),
          ),
          keyboardType: TextInputType.number,
        ),
      ],
    );
  }

  // Step 5: Advanced Options
  Widget _buildAdvancedStep() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Customize course features',
          style: Theme.of(context).textTheme.bodyLarge?.copyWith(
            color: Colors.grey[600],
          ),
        ),
        const SizedBox(height: 24),
        SwitchListTile(
          title: const Text('Greeting Module'),
          subtitle: const Text('Include a module with greeting words and phrases'),
          value: _greetingModule,
          onChanged: (value) => setState(() => _greetingModule = value),
        ),
        SwitchListTile(
          title: const Text('Reading Module'),
          subtitle: const Text('Include reading practice lessons'),
          value: _readingModule,
          onChanged: (value) => setState(() => _readingModule = value),
        ),
        SwitchListTile(
          title: const Text('Reading Exercises'),
          subtitle: const Text('Add focused reading exercises to each module'),
          value: _readingExercises,
          onChanged: (value) => setState(() => _readingExercises = value),
        ),
        SwitchListTile(
          title: const Text('Writing Exercises'),
          subtitle: const Text('Add focused writing exercises to each module'),
          value: _writingExercises,
          onChanged: (value) => setState(() => _writingExercises = value),
        ),
      ],
    );
  }

  Widget _buildDropdownField(String label, String? value, Function(String?) onChanged) {
    return DropdownButtonFormField<String>(
      initialValue: value,
      decoration: InputDecoration(
        labelText: label,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
        ),
      ),
      items: _languages.map((lang) {
        return DropdownMenuItem(
          value: lang,
          child: Text(lang),
        );
      }).toList(),
      onChanged: onChanged,
    );
  }

  Widget _buildCheckboxTile(String title, String value) {
    return CheckboxListTile(
      title: Text(title),
      value: _selectedGoals.contains(value),
      onChanged: (checked) {
        setState(() {
          if (checked == true) {
            _selectedGoals.add(value);
          } else {
            _selectedGoals.remove(value);
          }
        });
      },
      contentPadding: EdgeInsets.zero,
    );
  }

  Widget _buildSkillSlider(String label, double value, Function(double) onChanged) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              label,
              style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w500),
            ),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
              decoration: BoxDecoration(
                color: Theme.of(context).colorScheme.primaryContainer,
                borderRadius: BorderRadius.circular(12),
              ),
              child: Text(
                '${value.toInt()}/10',
                style: TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.w600,
                  color: Theme.of(context).colorScheme.onPrimaryContainer,
                ),
              ),
            ),
          ],
        ),
        const SizedBox(height: 8),
        Slider(
          value: value,
          min: 1,
          max: 10,
          divisions: 9,
          label: value.toInt().toString(),
          onChanged: onChanged,
        ),
        const SizedBox(height: 16),
      ],
    );
  }

  Future<void> _generateCourse() async {
    // Validate required fields
    if (_selectedLanguage == null || _selectedStudentLanguage == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Please select both target language and student language'),
          backgroundColor: Colors.red,
        ),
      );
      return;
    }

    if (_selectedModules.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Please load word modules first in the Word Selection step'),
          backgroundColor: Colors.red,
        ),
      );
      return;
    }

    setState(() {
      _isGenerating = true;
    });

    try {
      // Convert language names to codes
      final langCode = CourseGenerationService.getLanguageCode(_selectedLanguage!);
      final toLangCode = CourseGenerationService.getLanguageCode(_selectedStudentLanguage!);

      // Determine if reading/writing exercises should be enabled based on skill levels
      final enableReading = _readingLevel >= 3.0;
      final enableWriting = _writingLevel >= 3.0;
      
      // Use default word ratios (word selection is now handled via the word selection API)
      final verbsRatio = 0.4;
      final nounsRatio = 0.4;
      final adjectivesRatio = 0.1;
      final adverbsRatio = 0.1;

      // Parse CourseTemplate values with defaults
      final wordsPerModuleStart = _newWordsPerLessonController.text.isNotEmpty
          ? double.tryParse(_newWordsPerLessonController.text) ?? 2.0
          : 2.0;
      
      final wordsPerModuleIncreaseFactor = _wordsIncreaseFactorController.text.isNotEmpty
          ? double.tryParse(_wordsIncreaseFactorController.text) ?? 0.3
          : 0.3;
      
      final sentenceLengthStart = _sentenceLengthStartController.text.isNotEmpty
          ? int.tryParse(_sentenceLengthStartController.text) ?? 3
          : 3;
      
      final sentenceLengthIncreaseFactor = _sentenceLengthIncreaseFactorController.text.isNotEmpty
          ? double.tryParse(_sentenceLengthIncreaseFactorController.text) ?? 0.1
          : 0.1;
      
      final grammarPerModule = _grammarPerModuleController.text.isNotEmpty
          ? int.tryParse(_grammarPerModuleController.text) ?? 1
          : 1;

      // Show loading message
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Generating course... This may take a moment.'),
          backgroundColor: Colors.blue,
          duration: Duration(seconds: 2),
        ),
      );

      // Call the API
      final courseData = await CourseGenerationService.generateCourse(
        lang: langCode,
        toLang: toLangCode,
        wordsPerModuleStart: wordsPerModuleStart,
        wordsPerModuleIncreaseFactor: wordsPerModuleIncreaseFactor,
        sentenceLengthStart: sentenceLengthStart,
        sentenceLengthIncreaseFactor: sentenceLengthIncreaseFactor,
        verbs: verbsRatio,
        nouns: nounsRatio,
        adjectives: adjectivesRatio,
        adverbs: adverbsRatio,
        grammarPerModule: grammarPerModule,
        greetingModule: _greetingModule,
        readingModule: _readingModule || enableReading,
        readingExercises: _readingExercises || (enableReading && _readingLevel >= 5.0),
        writingExercises: _writingExercises || (enableWriting && _writingLevel >= 5.0),
      );

      setState(() {
        _isGenerating = false;
      });

      // Show success message
      if (mounted) {
        final moduleCount = (courseData['modules'] as List?)?.length ?? 0;
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              'Course generated successfully! Modules: $moduleCount',
            ),
            backgroundColor: Colors.green,
          ),
        );

        // Navigate back to courses screen
        Navigator.of(context).pop();
      }
    } catch (e) {
      setState(() {
        _isGenerating = false;
      });

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Error generating course: $e'),
            backgroundColor: Colors.red,
            duration: const Duration(seconds: 5),
          ),
        );
      }
    }
  }
}

class WizardStep {
  final String title;
  final String subtitle;
  final Widget content;

  WizardStep({
    required this.title,
    required this.subtitle,
    required this.content,
  });
}

