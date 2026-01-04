import 'package:flutter/material.dart';
import 'dart:async';

import '../../../../shared/models/quiz_model.dart';
import 'widgets/explanation_question.dart';
import 'widgets/multiple_choice_question.dart';
import 'widgets/question_types_models.dart';
import 'widgets/single_choice_question.dart';
import 'widgets/typing_question.dart';
import 'widgets/word_search_question.dart';
import 'widgets/memory_card_question.dart';

class QuestionTypesDemoPage extends StatefulWidget {
  const QuestionTypesDemoPage({super.key});

  @override
  State<QuestionTypesDemoPage> createState() => _QuestionTypesDemoPageState();
}

class _MemoryCardState {
  final String letter;
  final bool revealed;
  final bool matched;

  const _MemoryCardState({
    required this.letter,
    this.revealed = false,
    this.matched = false,
  });

  _MemoryCardState copyWith({bool? revealed, bool? matched}) {
    return _MemoryCardState(
      letter: letter,
      revealed: revealed ?? this.revealed,
      matched: matched ?? this.matched,
    );
  }
}

class _QuestionTypesDemoPageState extends State<QuestionTypesDemoPage> {
  late final List<DemoQuestion> _questions;
  int _currentIndex = 0;
  Set<int> _selected = {};
  bool _submitted = false;
  bool _isCorrect = false;
  List<CellPos> _selectedCells = [];
  Set<String> _foundWords = {};
  String _typedAnswer = '';
  double _typingTimeLeft = 10.0;
  bool _showTypingPrompt = false;
  Timer? _typingTimer;
  Timer? _revealTimer;
  final TextEditingController _typingController = TextEditingController();
  List<_MemoryCardState> _memoryCards = [];
  int? _memoryFirstIndex;
  bool _memoryReady = false;
  bool _memoryLock = false;
  Timer? _memoryHideTimer;

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
    _memoryHideTimer?.cancel();
    _typingController.dispose();
    super.dispose();
  }

  List<DemoQuestion> _buildDemoQuestions() {
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
    final memoryLetters = '言語明日問題仕事間に合わ美人'.split('');

    return [
      SingleChoiceDemoQuestion(
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
      MultipleChoiceDemoQuestion(
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
      ExplanationDemoQuestion(
        sentence: QuizSentence(
          id: 'explain_1',
          sentence: 'Tip: In multiple-selection questions, choose every correct option before submitting.',
          options: const [],
          words: const [],
          questionType: QuizQuestionType.explanation,
        ),
      ),
      WordSearchDemoQuestion(
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
      TypingDemoQuestion(
        sentence: QuizSentence(
          id: 'typing_1',
          sentence: 'Memorize this word, then type it.',
          options: const [],
          words: const [],
          questionType: QuizQuestionType.typing,
        ),
        targets: const ['bonjour'],
      ),
      TypingDemoQuestion(
        sentence: QuizSentence(
          id: 'typing_jp_1',
          sentence: 'Type the Japanese word 見える (to be visible).',
          options: const [],
          words: const [],
          questionType: QuizQuestionType.typing,
        ),
        targets: const ['見える'],
        letters: const ['見', '束', '座', 'っ', 'る', 'い', 'う', 'え', 'で', 'ら'],
      ),
      MemoryCardDemoQuestion(
        sentence: QuizSentence(
          id: 'memory_cards_1',
          sentence: 'Memory cards: match each pair of Japanese characters.',
          options: const [],
          words: const [],
          questionType: QuizQuestionType.explanation,
        ),
        letters: memoryLetters,
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
      _memoryCards = [];
      _memoryFirstIndex = null;
      _memoryReady = false;
      _memoryLock = false;
    });
    _typingTimer?.cancel();
    _revealTimer?.cancel();
    _memoryHideTimer?.cancel();
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
    final question = _questions[_currentIndex];
    if (question is! TypingDemoQuestion) return;
    final target = question.targets.first;
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
              label: Text(_labelForType(question.kind)),
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

  String _labelForType(DemoQuestionKind kind) {
    switch (kind) {
      case DemoQuestionKind.singleChoice:
        return 'Single Choice';
      case DemoQuestionKind.multipleChoice:
        return 'Multiple Selection';
      case DemoQuestionKind.explanation:
        return 'Explanation';
      case DemoQuestionKind.wordSearch:
        return 'Word Search';
      case DemoQuestionKind.typing:
        return 'Typing';
      case DemoQuestionKind.memoryCards:
        return 'Memory Cards';
    }
  }

  Widget _buildQuestionContent(DemoQuestion question) {
    final sentence = question.sentence;
    switch (question.kind) {
      case DemoQuestionKind.explanation:
        return ExplanationQuestion(text: sentence.sentence);
      case DemoQuestionKind.wordSearch:
        final q = question as WordSearchDemoQuestion;
        if (q.grid.isEmpty) {
          return ExplanationQuestion(text: sentence.sentence);
        }
        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              sentence.sentence,
              style: const TextStyle(fontSize: 18),
            ),
            const SizedBox(height: 12),
            Expanded(
              child: WordSearchQuestion(
                grid: q.grid,
                selectedCells: _selectedCells,
                submitted: _submitted,
                isCorrect: _isCorrect,
                onCellTap: _onGridTap,
              ),
            ),
          ],
        );
      case DemoQuestionKind.typing:
        final q = question as TypingDemoQuestion;
        final letters = q.letters ?? q.targets.expand((e) => e.split('')).toList();
        return TypingQuestion(
          targetWord: q.targets.first,
          letters: letters,
          showPrompt: _showTypingPrompt,
          typingTimeLeft: _typingTimeLeft,
          controller: _typingController,
          submitted: _submitted,
          isCorrect: _isCorrect,
          onChanged: (val) => setState(() => _typedAnswer = val),
          onLetterTap: _onTypingLetterTap,
        );
      case DemoQuestionKind.memoryCards:
        final q = question as MemoryCardDemoQuestion;
        final cards = _memoryCards
            .map((c) => MemoryCardItem(
                  letter: c.letter,
                  revealed: c.revealed,
                  matched: c.matched,
                ))
            .toList();
        final pairsFound = _memoryCards.where((c) => c.matched).length ~/ 2;
        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              sentence.sentence,
              style: const TextStyle(fontSize: 18),
            ),
            const SizedBox(height: 8),
            Text(
              _memoryReady
                  ? 'Flip two cards at a time. Matched pairs stay visible.'
                  : 'Memorize the cards. They will hide shortly.',
              style: TextStyle(color: Colors.grey.shade700),
            ),
            const SizedBox(height: 12),
            Expanded(
              child: MemoryCardQuestion(
                cards: cards,
                onTap: _onMemoryCardTap,
                interactionEnabled: _memoryReady && !_submitted && !_memoryLock,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              'Pairs found: $pairsFound / ${q.letters.length}',
              style: const TextStyle(fontWeight: FontWeight.w600),
            ),
            if (_submitted && _isCorrect)
              Padding(
                padding: const EdgeInsets.only(top: 8),
                child: Text(
                  'Great job! All pairs matched.',
                  style: TextStyle(color: Colors.green.shade700),
                ),
              ),
          ],
        );
      case DemoQuestionKind.multipleChoice:
        return MultipleChoiceQuestion(
          options: sentence.options,
          selected: _selected,
          submitted: _submitted,
          onToggle: _onToggle,
        );
      case DemoQuestionKind.singleChoice:
        return SingleChoiceQuestion(
          options: sentence.options,
          selected: _selected,
          submitted: _submitted,
          onTap: _onSingleTap,
        );
    }
  }

  void _onGridTap(int row, int col) {
    final question = _questions[_currentIndex];
    if (question.kind != DemoQuestionKind.wordSearch) return;
    if (_submitted) return;

    final existingIndex = _selectedCells.indexWhere((c) => c.row == row && c.col == col);
    setState(() {
      if (existingIndex >= 0) {
        _selectedCells.removeAt(existingIndex);
      } else {
        _selectedCells.add(CellPos(row, col));
      }
    });
  }

  void _submitWordSearch() {
    final question = _questions[_currentIndex];
    if (question is! WordSearchDemoQuestion) return;
    final grid = question.grid;
    final targets = question.targets;
    if (_submitted) return;

    final selected = List<CellPos>.from(_selectedCells);
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

  void _onMemoryCardTap(int idx) {
    if (_submitted || !_memoryReady || _memoryLock || idx < 0 || idx >= _memoryCards.length) {
      return;
    }
    final card = _memoryCards[idx];
    if (card.matched || card.revealed) return;

    setState(() {
      _memoryCards[idx] = card.copyWith(revealed: true);
    });

    if (_memoryFirstIndex == null) {
      _memoryFirstIndex = idx;
      return;
    }

    final firstIdx = _memoryFirstIndex!;
    final firstCard = _memoryCards[firstIdx];
    final secondCard = _memoryCards[idx];
    _memoryLock = true;

    if (firstCard.letter == secondCard.letter) {
      setState(() {
        _memoryCards[firstIdx] = firstCard.copyWith(matched: true);
        _memoryCards[idx] = secondCard.copyWith(matched: true);
      });
      _memoryFirstIndex = null;
      _memoryLock = false;
      _checkMemoryCompletion();
    } else {
      Timer(const Duration(milliseconds: 700), () {
        if (!mounted) return;
        setState(() {
          _memoryCards[firstIdx] = _memoryCards[firstIdx].copyWith(revealed: false);
          _memoryCards[idx] = _memoryCards[idx].copyWith(revealed: false);
        });
        _memoryFirstIndex = null;
        _memoryLock = false;
      });
    }
  }

  void _checkMemoryCompletion() {
    final allMatched = _memoryCards.isNotEmpty && _memoryCards.every((c) => c.matched);
    if (allMatched) {
      setState(() {
        _submitted = true;
        _isCorrect = true;
      });
    }
  }

  void _onTypingLetterTap(String c) {
    if (_submitted || _showTypingPrompt) return;
    final newText = _typingController.text + c;
    setState(() {
      _typingController.text = newText;
      _typingController.selection = TextSelection.fromPosition(
        TextPosition(offset: newText.length),
      );
      _typedAnswer = newText;
    });
  }

  void _setupForCurrentQuestion() {
    final question = _questions[_currentIndex];
    if (question.kind == DemoQuestionKind.memoryCards) {
      _memoryHideTimer?.cancel();
      final q = question as MemoryCardDemoQuestion;
      final duplicated = [...q.letters, ...q.letters];
      duplicated.shuffle();
      setState(() {
        _memoryCards = duplicated
            .map((l) => _MemoryCardState(letter: l, revealed: true, matched: false))
            .toList();
        _memoryReady = false;
        _memoryFirstIndex = null;
        _memoryLock = false;
      });
      _memoryHideTimer = Timer(const Duration(seconds: 3), () {
        if (!mounted) return;
        setState(() {
          _memoryCards = _memoryCards
              .map((c) => c.matched ? c : c.copyWith(revealed: false))
              .toList();
          _memoryReady = true;
        });
      });
    }
    if (question.kind == DemoQuestionKind.typing) {
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


  Widget _buildFooter(DemoQuestion question) {
    final isExplanation = question.kind == DemoQuestionKind.explanation;
    final isWordSearch = question.kind == DemoQuestionKind.wordSearch;
    final isTyping = question.kind == DemoQuestionKind.typing;
    final isMultiple = question.kind == DemoQuestionKind.multipleChoice;
    final isMemory = question.kind == DemoQuestionKind.memoryCards;

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
        if (_submitted && !_isCorrect && !isExplanation && !isWordSearch && !isMemory)
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
