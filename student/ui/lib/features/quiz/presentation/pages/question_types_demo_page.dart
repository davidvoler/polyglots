import 'package:flutter/material.dart';
import 'dart:async';

import '../../../../shared/models/quiz_model.dart';

class QuestionTypesDemoPage extends StatefulWidget {
  const QuestionTypesDemoPage({super.key});

  @override
  State<QuestionTypesDemoPage> createState() => _QuestionTypesDemoPageState();
}

class _DemoQuestion {
  final QuizSentence sentence;
  final List<String>? grid; // optional word search grid
  final List<String>? targets;

  _DemoQuestion({
    required this.sentence,
    this.grid,
    this.targets,
  });
}

class _CellPos {
  final int row;
  final int col;
  _CellPos(this.row, this.col);
}

class _QuestionTypesDemoPageState extends State<QuestionTypesDemoPage> {
  late final List<_DemoQuestion> _questions;
  int _currentIndex = 0;
  Set<int> _selected = {};
  bool _submitted = false;
  bool _isCorrect = false;
  List<_CellPos> _selectedCells = [];
  Set<String> _foundWords = {};
  String _typedAnswer = '';
  double _typingTimeLeft = 10.0;
  bool _showTypingPrompt = false;
  Timer? _typingTimer;
  Timer? _revealTimer;
  final TextEditingController _typingController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _questions = _buildDemoQuestions();
    _setupForCurrentQuestion();
  }

  @override
  void dispose() {
    _typingTimer?.cancel();
    _revealTimer?.cancel();
    _typingController.dispose();
    super.dispose();
  }

  List<_DemoQuestion> _buildDemoQuestions() {
    final wordSearchGrid = [
      'catarefghi',
      'oqrstuvwxp',
      'plmnocatrd',
      'abcarxyzab',
      'defghijklm',
      'nopcatqrst',
      'vwxyzabcde',
      'fghijklmnq',
      'rstuvwxyzr',
      'catzzzzzzz',
    ];
    final wordTargets = ['cat', 'car', 'arc'];

    return [
      _DemoQuestion(
        sentence: QuizSentence(
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
      ),
      _DemoQuestion(
        sentence: QuizSentence(
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
      ),
      _DemoQuestion(
        sentence: QuizSentence(
          id: 'explain_1',
          sentence: 'Tip: In multiple-selection questions, choose every correct option before submitting.',
          options: const [],
          words: const [],
          questionType: QuizQuestionType.explanation,
        ),
      ),
      _DemoQuestion(
        sentence: QuizSentence(
          id: 'wordsearch_1',
          sentence: 'Find the words: ${wordTargets.map((w) => w.toUpperCase()).join(", ")}.\nWords can be in any direction.',
          options: const [],
          words: wordTargets,
          questionType: QuizQuestionType.wordSearch,
        ),
        grid: wordSearchGrid,
        targets: wordTargets,
      ),
      _DemoQuestion(
        sentence: QuizSentence(
          id: 'typing_1',
          sentence: 'Memorize this word, then type it.',
          options: const [],
          words: const [],
          questionType: QuizQuestionType.typing,
        ),
        targets: const ['bonjour'],
      ),
    ];
  }

  void _resetStateForQuestion() {
    setState(() {
      _selected = {};
      _submitted = false;
      _isCorrect = false;
      _selectedCells = [];
      _foundWords = {};
      _typedAnswer = '';
      _typingTimeLeft = 10.0;
      _showTypingPrompt = false;
      _typingController.clear();
    });
    _typingTimer?.cancel();
    _revealTimer?.cancel();
    _setupForCurrentQuestion();
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
      _isCorrect = _questions[_currentIndex].sentence.options[idx].correct;
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
    final question = _questions[_currentIndex].sentence;
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

  void _submitTyping() {
    if (_submitted) return;
    final target = _questions[_currentIndex].targets?.first ?? '';
    final normalizedInput = _typedAnswer.trim().toLowerCase();
    final normalizedTarget = target.toLowerCase();
    final isCorrect = normalizedInput == normalizedTarget;
    _typingTimer?.cancel();
    setState(() {
      _submitted = true;
      _isCorrect = isCorrect;
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
              label: Text(_labelForType(question.sentence.questionType)),
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
      case QuizQuestionType.typing:
        return 'Typing';
    }
  }

  Widget _buildQuestionContent(_DemoQuestion question) {
    final sentence = question.sentence;
    switch (sentence.questionType) {
      case QuizQuestionType.explanation:
      case QuizQuestionType.wordSearch:
      case QuizQuestionType.typing:
        if (sentence.questionType == QuizQuestionType.wordSearch && question.grid != null) {
          return Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                sentence.sentence,
                style: const TextStyle(fontSize: 18),
              ),
              const SizedBox(height: 12),
              Expanded(
                child: sentence.questionType == QuizQuestionType.wordSearch
                    ? _buildWordSearchGrid(question)
                    : _buildTypingArea(question),
              ),
            ],
          );
        }
        return SingleChildScrollView(
          child: Text(
            sentence.sentence,
            style: const TextStyle(fontSize: 18),
          ),
        );
      case QuizQuestionType.multipleChoice:
        return ListView.builder(
          itemCount: sentence.options.length,
          itemBuilder: (context, idx) {
            final opt = sentence.options[idx];
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
          itemCount: sentence.options.length,
          itemBuilder: (context, idx) {
            final opt = sentence.options[idx];
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

  Widget _buildWordSearchGrid(_DemoQuestion question) {
    final grid = question.grid!;
    return AspectRatio(
      aspectRatio: 1,
      child: GridView.builder(
        physics: const NeverScrollableScrollPhysics(),
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 10,
        ),
        itemCount: 100,
        itemBuilder: (context, idx) {
          final row = idx ~/ 10;
          final col = idx % 10;
          final letter = grid[row][col].toUpperCase();
          final selected = _selectedCells.any((c) => c.row == row && c.col == col);
          final matched = _submitted && _isCorrect && selected;
          Color bg = Colors.white;
          Color border = Colors.grey.shade300;
          if (selected) {
            bg = Colors.blue.shade50;
            border = Colors.blue.shade400;
          }
          if (matched) {
            bg = Colors.green.shade50;
            border = Colors.green.shade400;
          }

          return GestureDetector(
            onTap: () => _onGridTap(row, col),
            child: Container(
              decoration: BoxDecoration(
                color: bg,
                border: Border.all(color: border),
              ),
              child: Center(
                child: Text(
                  letter,
                  style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w700),
                ),
              ),
            ),
          );
        },
      ),
    );
  }

  void _onGridTap(int row, int col) {
    final question = _questions[_currentIndex];
    if (question.sentence.questionType != QuizQuestionType.wordSearch) return;
    if (_submitted) return;

    final existingIndex = _selectedCells.indexWhere((c) => c.row == row && c.col == col);
    setState(() {
      if (existingIndex >= 0) {
        _selectedCells.removeAt(existingIndex);
      } else {
        _selectedCells.add(_CellPos(row, col));
      }
    });
  }

  void _submitWordSearch() {
    final question = _questions[_currentIndex];
    final grid = question.grid;
    final targets = question.targets;
    if (grid == null || targets == null) return;
    if (_submitted) return;

    final selected = List<_CellPos>.from(_selectedCells);
    if (selected.isEmpty) {
      setState(() {
        _submitted = true;
        _isCorrect = false;
      });
      return;
    }

    bool isLinear = true;
    if (selected.length > 1) {
      final dr = selected[1].row - selected[0].row;
      final dc = selected[1].col - selected[0].col;
      for (int i = 1; i < selected.length; i++) {
        final prev = selected[i - 1];
        final cur = selected[i];
        if (cur.row - prev.row != dr || cur.col - prev.col != dc) {
          isLinear = false;
          break;
        }
      }
    }

    String wordFromSelection = '';
    for (final cell in selected) {
      if (cell.row < 0 || cell.row >= grid.length) continue;
      final rowStr = grid[cell.row];
      if (cell.col < 0 || cell.col >= rowStr.length) continue;
      wordFromSelection += rowStr[cell.col];
    }
    final forward = wordFromSelection.toLowerCase();
    final backward = String.fromCharCodes(forward.runes.toList().reversed);

    final targetSet = targets.map((e) => e.toLowerCase()).toSet();
    final matched = isLinear && (targetSet.contains(forward) || targetSet.contains(backward));

    setState(() {
      _submitted = true;
      _isCorrect = matched;
      if (matched) {
        _foundWords.add(forward);
        _foundWords.add(backward);
      }
    });
  }

  void _setupForCurrentQuestion() {
    final question = _questions[_currentIndex];
    if (question.sentence.questionType == QuizQuestionType.typing) {
      setState(() {
        _showTypingPrompt = true;
      });
      _revealTimer = Timer(const Duration(seconds: 4), () {
        setState(() {
          _showTypingPrompt = false;
          _typingTimeLeft = 10.0;
        });
        _typingTimer = Timer.periodic(const Duration(milliseconds: 100), (timer) {
          setState(() {
            _typingTimeLeft = (_typingTimeLeft - 0.1).clamp(0.0, 10.0);
            if (_typingTimeLeft <= 0) {
              _typingTimer?.cancel();
              _submitTyping();
            }
          });
        });
      });
    }
  }

  Widget _buildTypingArea(_DemoQuestion question) {
    final targetWord = question.targets?.first ?? '';
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          _showTypingPrompt ? 'Memorize this word' : 'Type the word you just saw:',
          style: TextStyle(color: Colors.grey.shade700, fontWeight: FontWeight.w600),
        ),
        const SizedBox(height: 8),
        if (_showTypingPrompt)
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: Colors.blue.shade50,
              borderRadius: BorderRadius.circular(12),
            ),
            child: Text(
              targetWord.toUpperCase(),
              textAlign: TextAlign.center,
              style: const TextStyle(fontSize: 32, fontWeight: FontWeight.bold),
            ),
          ),
        if (!_showTypingPrompt) ...[
          LinearProgressIndicator(
            value: _typingTimeLeft / 10.0,
            backgroundColor: Colors.grey.shade200,
            valueColor: AlwaysStoppedAnimation<Color>(_typingTimeLeft > 3 ? Colors.blue : Colors.red),
            minHeight: 8,
          ),
          const SizedBox(height: 12),
          TextField(
            controller: _typingController,
            onChanged: (val) => setState(() {
              _typedAnswer = val;
            }),
            decoration: const InputDecoration(
              border: OutlineInputBorder(),
              hintText: 'Type here…',
            ),
            enabled: !_submitted,
          ),
          const SizedBox(height: 12),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: targetWord
                .split('')
                .map(
                  (c) => ElevatedButton(
                    onPressed: _submitted
                        ? null
                        : () {
                            final newText = _typingController.text + c;
                            setState(() {
                              _typingController.text = newText;
                              _typingController.selection = TextSelection.fromPosition(
                                TextPosition(offset: newText.length),
                              );
                              _typedAnswer = newText;
                            });
                          },
                    child: Text(c.toUpperCase()),
                  ),
                )
                .toList(),
          ),
          const SizedBox(height: 12),
          if (_submitted)
            Text(
              _isCorrect ? 'Correct!' : 'Incorrect. The word was "${targetWord.toUpperCase()}".',
              style: TextStyle(
                color: _isCorrect ? Colors.green.shade700 : Colors.red.shade700,
                fontWeight: FontWeight.w600,
              ),
            ),
        ],
      ],
    );
  }

  Widget _buildFooter(_DemoQuestion question) {
    final isExplanation = question.sentence.questionType == QuizQuestionType.explanation;
    final isWordSearch = question.sentence.questionType == QuizQuestionType.wordSearch;
    final isTyping = question.sentence.questionType == QuizQuestionType.typing;
    final isMultiple = question.sentence.questionType == QuizQuestionType.multipleChoice;

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
        if (isWordSearch && !_submitted)
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: _submitWordSearch,
              child: const Text('Check Selection'),
            ),
          ),
        if (isTyping && !_submitted && !_showTypingPrompt)
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: _submitTyping,
              child: const Text('Submit'),
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
