import 'package:flutter/material.dart';
import '../services/course_generation_service.dart';

class GenerateWithAIScreen extends StatefulWidget {
  const GenerateWithAIScreen({super.key});

  @override
  State<GenerateWithAIScreen> createState() => _GenerateWithAIScreenState();
}

class _GenerateWithAIScreenState extends State<GenerateWithAIScreen> {
  final _formKey = GlobalKey<FormState>();
  String? _selectedLanguage;
  String? _selectedStudentLanguage;
  final TextEditingController _courseDescriptionController = TextEditingController();
  
  // Loading state
  bool _isGenerating = false;

  // Student Level Section
  double _readingLevel = 1.0;
  double _writingLevel = 1.0;
  double _vocabularyLevel = 1.0;
  double _speakingLevel = 1.0;
  double _hiraganaLevel = 1.0;
  double _kanjiLevel = 1.0;
  double _katakanaLevel = 1.0;

  // Goals Section
  final Set<String> _selectedGoals = {};
  final TextEditingController _testNameController = TextEditingController();
  final TextEditingController _freeTextGoalController = TextEditingController();

  // Lessons Section
  final TextEditingController _numberOfLessonsController = TextEditingController();
  final TextEditingController _quizzesPerLessonController = TextEditingController();
  final TextEditingController _newWordsPerLessonController = TextEditingController();

  // Common language options
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
    'Other',
  ];

  bool get _isJapanese => _selectedLanguage == 'Japanese';

  @override
  void dispose() {
    _courseDescriptionController.dispose();
    _testNameController.dispose();
    _freeTextGoalController.dispose();
    _numberOfLessonsController.dispose();
    _quizzesPerLessonController.dispose();
    _newWordsPerLessonController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Generate with AI'),
        automaticallyImplyLeading: false,
        elevation: 0,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24.0),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Language Selection
              _buildSection(
                'Language Selection',
                'Select the target language for the course and the student\'s native language. Provide a description to help the AI understand your course goals.',
                [
                  _buildDropdownField(
                    'Language',
                    _selectedLanguage,
                    'Select the language being taught',
                    (value) => setState(() {
                      _selectedLanguage = value;
                      // Reset Japanese-specific levels if language changes
                      if (!_isJapanese) {
                        _hiraganaLevel = 1.0;
                        _kanjiLevel = 1.0;
                        _katakanaLevel = 1.0;
                      }
                    }),
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'Please select a language';
                      }
                      return null;
                    },
                  ),
                  const SizedBox(height: 16),
                  _buildDropdownField(
                    'Student Language',
                    _selectedStudentLanguage,
                    'Select the student\'s native language',
                    (value) => setState(() => _selectedStudentLanguage = value),
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'Please select a student language';
                      }
                      return null;
                    },
                  ),
                  const SizedBox(height: 16),
                  TextFormField(
                    controller: _courseDescriptionController,
                    maxLines: 5,
                    decoration: InputDecoration(
                      labelText: 'Course Description',
                      hintText: 'Describe what you want the AI to generate for this course...',
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(8),
                      ),
                      contentPadding: const EdgeInsets.all(16),
                      alignLabelWithHint: true,
                    ),
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'Please provide a course description';
                      }
                      return null;
                    },
                  ),
                ],
              ),

              const SizedBox(height: 16),

              // Student Level Section
              _buildExpansionTile(
                'Student Level',
                Icons.school,
                'Specify the student\'s proficiency level for each skill area using the 1-10 scale (Novice to Advanced). Additional options appear for Japanese courses.',
                _buildStudentLevelContent(),
              ),

              const SizedBox(height: 16),

              // Goals Section
              _buildExpansionTile(
                'Goals',
                Icons.flag,
                'Select the primary learning objectives for this course. You can choose multiple goals and add specific test names or custom goals.',
                _buildGoalsContent(),
              ),

              const SizedBox(height: 16),

              // Lessons Section
              _buildExpansionTile(
                'Lessons',
                Icons.book,
                'Define the course structure by specifying the number of lessons, quizzes per lesson, and vocabulary to be introduced in each lesson.',
                _buildLessonsContent(),
              ),

              const SizedBox(height: 32),

              // Generate Button
              ElevatedButton(
                onPressed: _isGenerating ? null : _handleGenerate,
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  backgroundColor: Theme.of(context).colorScheme.primary,
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(8),
                  ),
                ),
                child: _isGenerating
                    ? Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          SizedBox(
                            width: 20,
                            height: 20,
                            child: CircularProgressIndicator(
                              strokeWidth: 2,
                              valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                            ),
                          ),
                          const SizedBox(width: 12),
                          Text(
                            'Generating...',
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                              color: Colors.white,
                            ),
                          ),
                        ],
                      )
                    : Text(
                        'Generate',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                          color: Colors.white,
                        ),
                      ),
              ),
              const SizedBox(height: 24),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildSection(String title, String description, List<Widget> children) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
      ),
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              title,
              style: const TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              description,
              style: TextStyle(
                fontSize: 14,
                color: Colors.grey[600],
                height: 1.4,
              ),
            ),
            const SizedBox(height: 16),
            ...children,
          ],
        ),
      ),
    );
  }

  Widget _buildExpansionTile(String title, IconData icon, String description, Widget content) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
      ),
      child: ExpansionTile(
        leading: Icon(icon, color: Theme.of(context).colorScheme.primary),
        title: Text(
          title,
          style: const TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.bold,
          ),
        ),
        subtitle: Padding(
          padding: const EdgeInsets.only(top: 4.0),
          child: Text(
            description,
            style: TextStyle(
              fontSize: 13,
              color: Colors.grey[600],
              fontWeight: FontWeight.normal,
              height: 1.3,
            ),
          ),
        ),
        children: [
          Padding(
            padding: const EdgeInsets.all(20.0),
            child: content,
          ),
        ],
      ),
    );
  }

  Widget _buildDropdownField(
    String label,
    String? value,
    String hint,
    Function(String?) onChanged, {
    String? Function(String?)? validator,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          label,
          style: const TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.w600,
          ),
        ),
        const SizedBox(height: 8),
        DropdownButtonFormField<String>(
          initialValue: value,
          decoration: InputDecoration(
            hintText: hint,
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(8),
            ),
            contentPadding: const EdgeInsets.symmetric(
              horizontal: 16,
              vertical: 12,
            ),
          ),
          items: _languages.map((String language) {
            return DropdownMenuItem<String>(
              value: language,
              child: Text(language),
            );
          }).toList(),
          onChanged: onChanged,
          validator: validator,
        ),
      ],
    );
  }

  String _getSkillLevelLabel(double value) {
    if (value <= 2) return 'Novice';
    if (value <= 4) return 'Beginner';
    if (value <= 7) return 'Intermediate';
    return 'Advanced';
  }

  Widget _buildStudentLevelContent() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        _buildSkillSlider('Reading', _readingLevel, (value) {
          setState(() => _readingLevel = value);
        }),
        const SizedBox(height: 16),
        _buildSkillSlider('Writing', _writingLevel, (value) {
          setState(() => _writingLevel = value);
        }),
        const SizedBox(height: 16),
        _buildSkillSlider('Vocabulary', _vocabularyLevel, (value) {
          setState(() => _vocabularyLevel = value);
        }),
        const SizedBox(height: 16),
        _buildSkillSlider('Speaking', _speakingLevel, (value) {
          setState(() => _speakingLevel = value);
        }),
        if (_isJapanese) ...[
          const SizedBox(height: 24),
          const Divider(height: 1),
          const SizedBox(height: 24),
          const Text(
            'Japanese-Specific Levels',
            style: TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.w600,
            ),
          ),
          const SizedBox(height: 16),
          _buildSkillSlider('Hiragana', _hiraganaLevel, (value) {
            setState(() => _hiraganaLevel = value);
          }),
          const SizedBox(height: 16),
          _buildSkillSlider('Kanji', _kanjiLevel, (value) {
            setState(() => _kanjiLevel = value);
          }),
          const SizedBox(height: 16),
          _buildSkillSlider('Katakana', _katakanaLevel, (value) {
            setState(() => _katakanaLevel = value);
          }),
        ],
      ],
    );
  }

  Widget _buildSkillSlider(String label, double value, Function(double) onChanged) {
    final skillLevel = _getSkillLevelLabel(value);
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              label,
              style: const TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.w600,
              ),
            ),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
              decoration: BoxDecoration(
                color: Theme.of(context).colorScheme.primaryContainer,
                borderRadius: BorderRadius.circular(12),
              ),
              child: Text(
                '$skillLevel (${value.toInt()})',
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
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 4.0),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                '1 - Novice',
                style: TextStyle(
                  fontSize: 12,
                  color: Colors.grey[600],
                ),
              ),
              Text(
                '10 - Advanced',
                style: TextStyle(
                  fontSize: 12,
                  color: Colors.grey[600],
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildGoalsContent() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        _buildCheckboxTile('Better communication skills', _selectedGoals.contains('communication'), (value) {
          setState(() {
            if (value == true) {
              _selectedGoals.add('communication');
            } else {
              _selectedGoals.remove('communication');
            }
          });
        }),
        _buildCheckboxTile('Test', _selectedGoals.contains('test'), (value) {
          setState(() {
            if (value == true) {
              _selectedGoals.add('test');
            } else {
              _selectedGoals.remove('test');
            }
          });
        }),
        if (_selectedGoals.contains('test')) ...[
          const SizedBox(height: 8),
          Padding(
            padding: const EdgeInsets.only(left: 40.0),
            child: TextFormField(
              controller: _testNameController,
              decoration: InputDecoration(
                hintText: 'Write the test name',
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(8),
                ),
                contentPadding: const EdgeInsets.symmetric(
                  horizontal: 16,
                  vertical: 12,
                ),
              ),
            ),
          ),
          const SizedBox(height: 12),
        ],
        _buildCheckboxTile('Reading', _selectedGoals.contains('reading'), (value) {
          setState(() {
            if (value == true) {
              _selectedGoals.add('reading');
            } else {
              _selectedGoals.remove('reading');
            }
          });
        }),
        _buildCheckboxTile('Writing', _selectedGoals.contains('writing'), (value) {
          setState(() {
            if (value == true) {
              _selectedGoals.add('writing');
            } else {
              _selectedGoals.remove('writing');
            }
          });
        }),
        _buildCheckboxTile('Speaking', _selectedGoals.contains('speaking'), (value) {
          setState(() {
            if (value == true) {
              _selectedGoals.add('speaking');
            } else {
              _selectedGoals.remove('speaking');
            }
          });
        }),
        _buildCheckboxTile('Grammar', _selectedGoals.contains('grammar'), (value) {
          setState(() {
            if (value == true) {
              _selectedGoals.add('grammar');
            } else {
              _selectedGoals.remove('grammar');
            }
          });
        }),
        _buildCheckboxTile('Cultural Context', _selectedGoals.contains('cultural'), (value) {
          setState(() {
            if (value == true) {
              _selectedGoals.add('cultural');
            } else {
              _selectedGoals.remove('cultural');
            }
          });
        }),
        _buildCheckboxTile('Hobby', _selectedGoals.contains('hobby'), (value) {
          setState(() {
            if (value == true) {
              _selectedGoals.add('hobby');
            } else {
              _selectedGoals.remove('hobby');
            }
          });
        }),
        const SizedBox(height: 12),
        TextFormField(
          controller: _freeTextGoalController,
          maxLines: 4,
          decoration: InputDecoration(
            labelText: 'Free text',
            hintText: 'Enter any additional goals...',
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(8),
            ),
            contentPadding: const EdgeInsets.all(16),
            alignLabelWithHint: true,
          ),
        ),
      ],
    );
  }

  Widget _buildLessonsContent() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        TextFormField(
          controller: _numberOfLessonsController,
          decoration: InputDecoration(
            labelText: 'Number of lessons',
            hintText: 'Enter number of lessons',
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(8),
            ),
            contentPadding: const EdgeInsets.symmetric(
              horizontal: 16,
              vertical: 12,
            ),
          ),
          keyboardType: TextInputType.number,
          validator: (value) {
            if (value == null || value.isEmpty) {
              return 'Please enter number of lessons';
            }
            if (int.tryParse(value) == null || int.parse(value) <= 0) {
              return 'Please enter a valid positive number';
            }
            return null;
          },
        ),
        const SizedBox(height: 16),
        TextFormField(
          controller: _quizzesPerLessonController,
          decoration: InputDecoration(
            labelText: 'Number of quizzes per lesson',
            hintText: 'Enter number of quizzes',
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(8),
            ),
            contentPadding: const EdgeInsets.symmetric(
              horizontal: 16,
              vertical: 12,
            ),
          ),
          keyboardType: TextInputType.number,
          validator: (value) {
            if (value == null || value.isEmpty) {
              return 'Please enter number of quizzes per lesson';
            }
            if (int.tryParse(value) == null || int.parse(value) < 0) {
              return 'Please enter a valid non-negative number';
            }
            return null;
          },
        ),
        const SizedBox(height: 16),
        TextFormField(
          controller: _newWordsPerLessonController,
          decoration: InputDecoration(
            labelText: 'Number of new words per lesson',
            hintText: 'Enter number of new words',
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(8),
            ),
            contentPadding: const EdgeInsets.symmetric(
              horizontal: 16,
              vertical: 12,
            ),
          ),
          keyboardType: TextInputType.number,
          validator: (value) {
            if (value == null || value.isEmpty) {
              return 'Please enter number of new words per lesson';
            }
            if (int.tryParse(value) == null || int.parse(value) < 0) {
              return 'Please enter a valid non-negative number';
            }
            return null;
          },
        ),
      ],
    );
  }

  Widget _buildCheckboxTile(String title, bool value, Function(bool?) onChanged) {
    return CheckboxListTile(
      title: Text(title),
      value: value,
      onChanged: onChanged,
      contentPadding: EdgeInsets.zero,
      controlAffinity: ListTileControlAffinity.leading,
    );
  }

  Future<void> _handleGenerate() async {
    if (_formKey.currentState!.validate()) {
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
        
        // Use fixed word ratios (can be customized in wizard)
        // Default distribution: 40% verbs, 40% nouns, 10% adjectives, 10% adverbs
        final verbsRatio = 0.4;
        final nounsRatio = 0.4;
        final adjectivesRatio = 0.1;
        final adverbsRatio = 0.1;

        // Calculate words per module based on new words per lesson
        final wordsPerModule = _newWordsPerLessonController.text.isNotEmpty
            ? double.tryParse(_newWordsPerLessonController.text) ?? 2.0
            : 2.0;

        // Show loading message
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Generating course... This may take a moment.'),
            backgroundColor: Colors.blue,
            duration: Duration(seconds: 2),
          ),
        );

        // Call the API - using same logic as wizard for consistency
        final courseData = await CourseGenerationService.generateCourse(
          lang: langCode,
          toLang: toLangCode,
          wordsPerModuleStart: wordsPerModule,
          wordsPerModuleIncreaseFactor: 0.3,
          sentenceLengthStart: _readingLevel.toInt().clamp(1, 10),
          sentenceLengthIncreaseFactor: 0.1,
          verbs: verbsRatio,
          nouns: nounsRatio,
          adjectives: adjectivesRatio,
          adverbs: adverbsRatio,
          grammarPerModule: 1,
          greetingModule: true, // Default greeting module (same as wizard default)
          readingModule: enableReading, // Auto-enable based on skill levels (same as wizard)
          readingExercises: enableReading && _readingLevel >= 5.0, // Auto-enable based on skill levels (same as wizard)
          writingExercises: enableWriting && _writingLevel >= 5.0, // Auto-enable based on skill levels (same as wizard)
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

          // TODO: Navigate to course preview/review screen with courseData
          // Navigator.push(
          //   context,
          //   MaterialPageRoute(
          //     builder: (context) => CoursePreviewScreen(courseData: courseData),
          //   ),
          // );
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
}
