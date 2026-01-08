import 'package:flutter/material.dart';

class CourseQuestionnaireScreen extends StatefulWidget {
  const CourseQuestionnaireScreen({super.key});

  @override
  State<CourseQuestionnaireScreen> createState() => _CourseQuestionnaireScreenState();
}

class _CourseQuestionnaireScreenState extends State<CourseQuestionnaireScreen> {
  // Section 1: Course Basics
  String? selectedPurpose;
  final TextEditingController courseGoalController = TextEditingController();

  // Section 2: Student Profile
  final Set<String> selectedLevels = {};
  bool? includeLevelTest;
  final TextEditingController studentProfileController = TextEditingController();

  // Section 3: Learning Skills Balance
  double readingValue = 5;
  double writingValue = 5;
  double listeningValue = 5;
  double speakingValue = 5;

  // Section 4: Content Focus
  final Set<String> selectedPriorities = {};
  String? alphabetStatus;
  bool? includeAlphabetInstruction;

  // Section 5: Instructional Approach
  double grammarApproachValue = 5;
  final Set<String> selectedMethods = {};

  // Section 6: Course Structure
  String? courseOrganization;
  String? lessonCount;

  // Section 7: Special Considerations
  final TextEditingController specificTopicsController = TextEditingController();
  final TextEditingController topicsToAvoidController = TextEditingController();
  final TextEditingController constraintsController = TextEditingController();

  // Section 8: Additional Notes
  final TextEditingController additionalNotesController = TextEditingController();

  @override
  void dispose() {
    courseGoalController.dispose();
    studentProfileController.dispose();
    specificTopicsController.dispose();
    topicsToAvoidController.dispose();
    constraintsController.dispose();
    additionalNotesController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('AI Language Course Generator'),
        elevation: 0,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Section 1: Course Basics
            _buildSectionHeader('Section 1: Course Basics'),
            _buildQuestionHeader('What is the purpose of this course?'),
            _buildRadioTile('Exam preparation', 'exam', selectedPurpose, (val) {
              setState(() => selectedPurpose = val);
            }),
            _buildRadioTile('Daily/conversational use', 'daily', selectedPurpose, (val) {
              setState(() => selectedPurpose = val);
            }),
            _buildRadioTile('Professional/business communication', 'business', selectedPurpose, (val) {
              setState(() => selectedPurpose = val);
            }),
            _buildRadioTile('Travel and practical situations', 'travel', selectedPurpose, (val) {
              setState(() => selectedPurpose = val);
            }),
            _buildRadioTile('Hobby/cultural interest', 'hobby', selectedPurpose, (val) {
              setState(() => selectedPurpose = val);
            }),
            _buildRadioTile('Other', 'other', selectedPurpose, (val) {
              setState(() => selectedPurpose = val);
            }),
            const SizedBox(height: 16),
            _buildQuestionHeader('Please describe the specific goal in your own words:'),
            _buildTextField(courseGoalController, 'Course goal...', maxLines: 4),
            const SizedBox(height: 32),

            // Section 2: Student Profile
            _buildSectionHeader('Section 2: Student Profile'),
            _buildQuestionHeader('Which student levels will this course serve?'),
            _buildCheckboxTile('Complete beginners', 'beginner_0', selectedLevels),
            _buildCheckboxTile('Beginner (A1)', 'a1', selectedLevels),
            _buildCheckboxTile('Elementary (A2)', 'a2', selectedLevels),
            _buildCheckboxTile('Intermediate (B1)', 'b1', selectedLevels),
            _buildCheckboxTile('Upper-Intermediate (B2)', 'b2', selectedLevels),
            _buildCheckboxTile('Advanced (C1)', 'c1', selectedLevels),
            _buildCheckboxTile('Mastery (C2)', 'c2', selectedLevels),
            const SizedBox(height: 16),
            _buildQuestionHeader('Will this course include a placement/level test?'),
            _buildRadioTile('Yes', true, includeLevelTest, (val) {
              setState(() => includeLevelTest = val);
            }),
            _buildRadioTile('No', false, includeLevelTest, (val) {
              setState(() => includeLevelTest = val);
            }),
            const SizedBox(height: 16),
            _buildQuestionHeader('Describe your typical students:'),
            _buildTextField(studentProfileController, 'Student profile...', maxLines: 4),
            const SizedBox(height: 32),

            // Section 3: Learning Skills Balance
            _buildSectionHeader('Section 3: Learning Skills Balance'),
            _buildSliderQuestion('Reading', readingValue, (val) {
              setState(() => readingValue = val);
            }),
            _buildSliderQuestion('Writing', writingValue, (val) {
              setState(() => writingValue = val);
            }),
            _buildSliderQuestion('Listening/Understanding', listeningValue, (val) {
              setState(() => listeningValue = val);
            }),
            _buildSliderQuestion('Speaking', speakingValue, (val) {
              setState(() => speakingValue = val);
            }),
            const SizedBox(height: 32),

            // Section 4: Content Focus
            _buildSectionHeader('Section 4: Content Focus'),
            _buildQuestionHeader('Learning Priorities:'),
            _buildCheckboxTile('Vocabulary building', 'vocabulary', selectedPriorities),
            _buildCheckboxTile('Grammar and syntax (explicit)', 'grammar_explicit', selectedPriorities),
            _buildCheckboxTile('Grammar and syntax (by example)', 'grammar_example', selectedPriorities),
            _buildCheckboxTile('Correct sentence composition', 'composition', selectedPriorities),
            _buildCheckboxTile('Conversation practice', 'conversation', selectedPriorities),
            _buildCheckboxTile('Cultural context', 'culture', selectedPriorities),
            _buildCheckboxTile('Idiomatic expressions', 'idioms', selectedPriorities),
            _buildCheckboxTile('Professional terminology', 'professional', selectedPriorities),
            const SizedBox(height: 16),
            _buildQuestionHeader('Is the writing system/alphabet new to students?'),
            _buildRadioTile('Completely new', 'new', alphabetStatus, (val) {
              setState(() => alphabetStatus = val);
            }),
            _buildRadioTile('Partially familiar', 'partial', alphabetStatus, (val) {
              setState(() => alphabetStatus = val);
            }),
            _buildRadioTile('Already familiar', 'familiar', alphabetStatus, (val) {
              setState(() => alphabetStatus = val);
            }),
            _buildRadioTile('Mixed', 'mixed', alphabetStatus, (val) {
              setState(() => alphabetStatus = val);
            }),
            const SizedBox(height: 16),
            _buildQuestionHeader('Should the course include alphabet/reading instruction?'),
            _buildRadioTile('Yes, teach from scratch', 'scratch', includeAlphabetInstruction, (val) {
              setState(() => includeAlphabetInstruction = val);
            }),
            _buildRadioTile('Yes, review/strengthen', 'review', includeAlphabetInstruction, (val) {
              setState(() => includeAlphabetInstruction = val);
            }),
            _buildRadioTile('No, assume students can read', 'no', includeAlphabetInstruction, (val) {
              setState(() => includeAlphabetInstruction = val);
            }),
            _buildRadioTile('Include as optional module', 'optional', includeAlphabetInstruction, (val) {
              setState(() => includeAlphabetInstruction = val);
            }),
            const SizedBox(height: 32),

            // Section 5: Instructional Approach
            _buildSectionHeader('Section 5: Instructional Approach'),
            _buildQuestionHeader('How explicit should grammar instruction be?'),
            _buildSliderWithLabels('Explicit Rules', 'Learning by Example', grammarApproachValue, (val) {
              setState(() => grammarApproachValue = val);
            }),
            const SizedBox(height: 16),
            _buildQuestionHeader('Preferred Learning Methods:'),
            _buildCheckboxTile('Dialogues and conversations', 'dialogues', selectedMethods),
            _buildCheckboxTile('Text passages and stories', 'passages', selectedMethods),
            _buildCheckboxTile('Explicit grammar explanations', 'explanations', selectedMethods),
            _buildCheckboxTile('Visual aids and infographics', 'visuals', selectedMethods),
            _buildCheckboxTile('Audio and pronunciation', 'audio', selectedMethods),
            _buildCheckboxTile('Cultural context and scenarios', 'scenarios', selectedMethods),
            _buildCheckboxTile('Exercises and drills', 'exercises', selectedMethods),
            _buildCheckboxTile('Games and interactive activities', 'games', selectedMethods),
            const SizedBox(height: 32),

            // Section 6: Course Structure
            _buildSectionHeader('Section 6: Course Structure'),
            _buildQuestionHeader('How should lessons be organized?'),
            _buildRadioTile('By grammar topic', 'grammar', courseOrganization, (val) {
              setState(() => courseOrganization = val);
            }),
            _buildRadioTile('By vocabulary theme', 'vocabulary', courseOrganization, (val) {
              setState(() => courseOrganization = val);
            }),
            _buildRadioTile('By real-world situation', 'situation', courseOrganization, (val) {
              setState(() => courseOrganization = val);
            }),
            _buildRadioTile('By skill', 'skill', courseOrganization, (val) {
              setState(() => courseOrganization = val);
            }),
            _buildRadioTile('Mixed approach', 'mixed', courseOrganization, (val) {
              setState(() => courseOrganization = val);
            }),
            const SizedBox(height: 16),
            _buildQuestionHeader('Approximate number of lessons/units:'),
            _buildRadioTile('5-10 lessons', '5-10', lessonCount, (val) {
              setState(() => lessonCount = val);
            }),
            _buildRadioTile('10-20 lessons', '10-20', lessonCount, (val) {
              setState(() => lessonCount = val);
            }),
            _buildRadioTile('20-30 lessons', '20-30', lessonCount, (val) {
              setState(() => lessonCount = val);
            }),
            _buildRadioTile('30+ lessons', '30+', lessonCount, (val) {
              setState(() => lessonCount = val);
            }),
            _buildRadioTile('No preference', 'no_pref', lessonCount, (val) {
              setState(() => lessonCount = val);
            }),
            const SizedBox(height: 32),

            // Section 7: Special Considerations
            _buildSectionHeader('Section 7: Special Considerations'),
            _buildQuestionHeader('Any specific topics, vocabulary, or scenarios this course must cover?'),
            _buildTextField(specificTopicsController, 'Specific topics...', maxLines: 4),
            const SizedBox(height: 16),
            _buildQuestionHeader('Topics to AVOID or cultural sensitivities:'),
            _buildTextField(topicsToAvoidController, 'Topics to avoid...', maxLines: 4),
            const SizedBox(height: 16),
            _buildQuestionHeader('Any constraints or requirements?'),
            _buildTextField(constraintsController, 'Constraints...', maxLines: 4),
            const SizedBox(height: 32),

            // Section 8: Additional Notes
            _buildSectionHeader('Section 8: Additional Notes'),
            _buildQuestionHeader('Anything else you\'d like the AI to know?'),
            _buildTextField(additionalNotesController, 'Additional notes...', maxLines: 4),
            const SizedBox(height: 32),

            // Submit Button
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _submitForm,
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  backgroundColor: Colors.blue,
                ),
                child: const Text('Generate Course', style: TextStyle(fontSize: 16, color: Colors.white)),
              ),
            ),
            const SizedBox(height: 32),
          ],
        ),
      ),
    );
  }

  Widget _buildSectionHeader(String title) {
    return Padding(
      padding: const EdgeInsets.only(top: 24, bottom: 12),
      child: Text(
        title,
        style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.blue),
      ),
    );
  }

  Widget _buildQuestionHeader(String title) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Text(
        title,
        style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600),
      ),
    );
  }

  Widget _buildRadioTile(String label, dynamic value, dynamic groupValue, Function(dynamic) onChanged) {
    return RadioListTile(
      title: Text(label),
      value: value,
      groupValue: groupValue,
      onChanged: (val) => onChanged(val),
      contentPadding: EdgeInsets.zero,
    );
  }

  Widget _buildCheckboxTile(String label, String value, Set<String> set) {
    return CheckboxListTile(
      title: Text(label),
      value: set.contains(value),
      onChanged: (val) {
        setState(() {
          if (val == true) {
            set.add(value);
          } else {
            set.remove(value);
          }
        });
      },
      contentPadding: EdgeInsets.zero,
    );
  }

  Widget _buildTextField(TextEditingController controller, String hint, {int maxLines = 1}) {
    return TextField(
      controller: controller,
      maxLines: maxLines,
      decoration: InputDecoration(
        hintText: hint,
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
        contentPadding: const EdgeInsets.all(12),
      ),
    );
  }

  Widget _buildSliderQuestion(String label, double value, Function(double) onChanged) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('$label: ${value.toInt()}/10', style: const TextStyle(fontWeight: FontWeight.w500)),
        Slider(
          value: value,
          min: 0,
          max: 10,
          divisions: 10,
          onChanged: onChanged,
        ),
        const SizedBox(height: 16),
      ],
    );
  }

  Widget _buildSliderWithLabels(String leftLabel, String rightLabel, double value, Function(double) onChanged) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Slider(
          value: value,
          min: 0,
          max: 10,
          divisions: 10,
          onChanged: onChanged,
        ),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 8),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(leftLabel, style: const TextStyle(fontSize: 12)),
              Text(rightLabel, style: const TextStyle(fontSize: 12)),
            ],
          ),
        ),
        const SizedBox(height: 16),
      ],
    );
  }

  void _submitForm() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Form submitted! Generating your course...')),
    );
    // TODO: Send data to backend API
    print('Form Data:');
    print('Purpose: $selectedPurpose');
    print('Levels: $selectedLevels');
    print('Reading: $readingValue, Writing: $writingValue, Listening: $listeningValue, Speaking: $speakingValue');
  }
}
