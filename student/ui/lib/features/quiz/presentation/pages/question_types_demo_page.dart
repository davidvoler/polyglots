import 'package:flutter/material.dart';

import '../../../../shared/models/quiz_model.dart';

class QuestionTypesDemoPage extends StatefulWidget {
  const QuestionTypesDemoPage({super.key});

  @override
  State<QuestionTypesDemoPage> createState() => _QuestionTypesDemoPageState();
}

class _QuestionTypesDemoPageState extends State<QuestionTypesDemoPage> {
  late final List<QuizSentence> _questions;
  int _currentIndex = 0;
  Set<int> _selected = {};
  bool _submitted = false;
  bool _isCorrect = false;

  @override
  void initState() {
    super.initState();
    _questions = _buildDemoQuestions();
  }

  List<QuizSentence> _buildDemoQuestions() {
    return [
      QuizSentence(
        id: 'single_1',
        sentence: 'What does "Bonjour" mean?',
        options: [
          QuizOption(sentence: 'Goodbye', correct: false),
          QuizOption(sentence: 'Hello', correct: true),
          QuizOption(sentence: 'Thank you', correct: false),
          QuizOption(sentence: 'Please', correct: false),
        ],
        words: const [],
        questionType: QuizQuestionType.singleChoice,
      ),
      QuizSentence(
        id: 'multi_1',
        sentence: 'Select all fruits.',
        options: [
          QuizOption(sentence: 'Apple', correct: true),
          QuizOption(sentence: 'Car', correct: false),
          QuizOption(sentence: 'Banana', correct: true),
          QuizOption(sentence: 'Table', correct: false),
        ],
        words: const [],
        questionType: QuizQuestionType.multipleChoice,
      ),
      QuizSentence(
        id: 'explain_1',
        sentence: 'Tip: In multiple-selection questions, choose every correct option before submitting.',
        options: const [],
        words: const [],
        questionType: QuizQuestionType.explanation,
      ),
      QuizSentence(
        id: 'wordsearch_1',
        sentence: 'Find the word "car" in the grid below:\n\na b c\nc a a\nd b r',
        options: const [],
        words: const [],
        questionType: QuizQuestionType.wordSearch,
      ),
    ];
  }

  void _resetStateForQuestion() {
    setState(() {
      _selected = {};
      _submitted = false;
      _isCorrect = false;
    });
  }

  void _next() {
    if (_currentIndex < _questions.length - 1) {
      setState(() {
        _currentIndex++;
      });
      _resetStateForQuestion();
    }
  }

  void _prev() {
    if (_currentIndex > 0) {
      setState(() {
        _currentIndex--;
      });
      _resetStateForQuestion();
    }
  }

  void _onSingleTap(int idx) {
    if (_submitted) return;
    setState(() {
      _selected = {idx};
      _submitted = true;
      _isCorrect = _questions[_currentIndex].options[idx].correct;
    });
  }

  void _onToggle(int idx) {
    if (_submitted) return;
    setState(() {
      if (_selected.contains(idx)) {
        _selected.remove(idx);
      } else {
        _selected.add(idx);
      }
    });
  }

  void _submitMultiple() {
    if (_submitted) return;
    final question = _questions[_currentIndex];
    final correctSet = <int>{};
    for (var i = 0; i < question.options.length; i++) {
      if (question.options[i].correct) correctSet.add(i);
    }
    setState(() {
      _submitted = true;
      _isCorrect = _selected.isNotEmpty &&
          _selected.length == correctSet.length &&
          _selected.containsAll(correctSet);
    });
  }

  @override
  Widget build(BuildContext context) {
    final question = _questions[_currentIndex];
    return Scaffold(
      appBar: AppBar(
        title: const Text('Question Types Demo'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Demo ${_currentIndex + 1} of ${_questions.length}',
              style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
            ),
            const SizedBox(height: 8),
            Chip(
              label: Text(_labelForType(question.questionType)),
              backgroundColor: Colors.blue.shade50,
              labelStyle: TextStyle(color: Colors.blue.shade700),
            ),
            const SizedBox(height: 16),
            Expanded(
              child: _buildQuestionContent(question),
            ),
            const SizedBox(height: 16),
            _buildFooter(question),
          ],
        ),
      ),
    );
  }

  String _labelForType(QuizQuestionType type) {
    switch (type) {
      case QuizQuestionType.singleChoice:
        return 'Single Choice';
      case QuizQuestionType.multipleChoice:
        return 'Multiple Selection';
      case QuizQuestionType.explanation:
        return 'Explanation';
      case QuizQuestionType.wordSearch:
        return 'Word Search';
    }
  }

  Widget _buildQuestionContent(QuizSentence question) {
    switch (question.questionType) {
      case QuizQuestionType.explanation:
      case QuizQuestionType.wordSearch:
        return SingleChildScrollView(
          child: Text(
            question.sentence,
            style: const TextStyle(fontSize: 18),
          ),
        );
      case QuizQuestionType.multipleChoice:
        return ListView.builder(
          itemCount: question.options.length,
          itemBuilder: (context, idx) {
            final opt = question.options[idx];
            final selected = _selected.contains(idx);
            final showResult = _submitted;
            final correct = opt.correct;

            Color bg = Colors.white;
            Color border = Colors.grey.shade300;
            if (showResult) {
              if (correct) {
                bg = Colors.green.shade50;
                border = Colors.green.shade300;
              } else if (selected) {
                bg = Colors.red.shade50;
                border = Colors.red.shade300;
              }
            } else if (selected) {
              bg = Colors.blue.shade50;
              border = Colors.blue.shade300;
            }

            return Container(
              margin: const EdgeInsets.only(bottom: 12),
              decoration: BoxDecoration(
                color: bg,
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: border),
              ),
              child: CheckboxListTile(
                value: selected,
                onChanged: _submitted ? null : (_) => _onToggle(idx),
                title: Text(opt.sentence),
                controlAffinity: ListTileControlAffinity.leading,
              ),
            );
          },
        );
      case QuizQuestionType.singleChoice:
        return ListView.builder(
          itemCount: question.options.length,
          itemBuilder: (context, idx) {
            final opt = question.options[idx];
            final selected = _selected.contains(idx);
            final showResult = _submitted;
            final correct = opt.correct;

            Color bg = Colors.white;
            Color border = Colors.grey.shade300;
            if (showResult && correct) {
              bg = Colors.green.shade50;
              border = Colors.green.shade300;
            } else if (selected && showResult && !correct) {
              bg = Colors.red.shade50;
              border = Colors.red.shade300;
            } else if (selected) {
              bg = Colors.blue.shade50;
              border = Colors.blue.shade300;
            }

            return Container(
              margin: const EdgeInsets.only(bottom: 12),
              decoration: BoxDecoration(
                color: bg,
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: border),
              ),
              child: ListTile(
                onTap: () => _onSingleTap(idx),
                title: Text(opt.sentence),
                trailing: selected
                    ? const Icon(Icons.check_circle, color: Colors.blue)
                    : const Icon(Icons.radio_button_unchecked),
              ),
            );
          },
        );
    }
  }

  Widget _buildFooter(QuizSentence question) {
    final isExplanation = question.questionType == QuizQuestionType.explanation;
    final isWordSearch = question.questionType == QuizQuestionType.wordSearch;
    final isMultiple = question.questionType == QuizQuestionType.multipleChoice;

    return Column(
      children: [
        if (isMultiple && !_submitted)
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: _submitMultiple,
              child: const Text('Check Answer'),
            ),
          ),
        if (_submitted && !_isCorrect && !isExplanation && !isWordSearch)
          Padding(
            padding: const EdgeInsets.symmetric(vertical: 8),
            child: Text(
              'Not quite. Try again or move on.',
              style: TextStyle(color: Colors.red.shade700),
            ),
          ),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            TextButton(
              onPressed: _currentIndex == 0 ? null : _prev,
              child: const Text('Previous'),
            ),
            TextButton(
              onPressed: _currentIndex == _questions.length - 1 ? null : _next,
              child: const Text('Next'),
            ),
          ],
        ),
      ],
    );
  }
}

