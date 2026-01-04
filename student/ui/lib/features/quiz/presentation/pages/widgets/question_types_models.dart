import '../../../../../shared/models/quiz_model.dart';

enum DemoQuestionKind {
  singleChoice,
  multipleChoice,
  explanation,
  wordSearch,
  typing,
  memoryCards,
}

abstract class DemoQuestion {
  DemoQuestionKind get kind;
  QuizSentence get sentence;
  const DemoQuestion();
}

class SingleChoiceDemoQuestion extends DemoQuestion {
  @override
  final DemoQuestionKind kind = DemoQuestionKind.singleChoice;
  @override
  final QuizSentence sentence;

  const SingleChoiceDemoQuestion({required this.sentence});
}

class MultipleChoiceDemoQuestion extends DemoQuestion {
  @override
  final DemoQuestionKind kind = DemoQuestionKind.multipleChoice;
  @override
  final QuizSentence sentence;

  const MultipleChoiceDemoQuestion({required this.sentence});
}

class ExplanationDemoQuestion extends DemoQuestion {
  @override
  final DemoQuestionKind kind = DemoQuestionKind.explanation;
  @override
  final QuizSentence sentence;

  const ExplanationDemoQuestion({required this.sentence});
}

class WordSearchDemoQuestion extends DemoQuestion {
  @override
  final DemoQuestionKind kind = DemoQuestionKind.wordSearch;
  @override
  final QuizSentence sentence;
  final List<String> grid;
  final List<String> targets;

  const WordSearchDemoQuestion({
    required this.sentence,
    required this.grid,
    required this.targets,
  });
}

class TypingDemoQuestion extends DemoQuestion {
  @override
  final DemoQuestionKind kind = DemoQuestionKind.typing;
  @override
  final QuizSentence sentence;
  final List<String> targets;
  final List<String>? letters;

  const TypingDemoQuestion({
    required this.sentence,
    required this.targets,
    this.letters,
  });
}

class MemoryCardDemoQuestion extends DemoQuestion {
  @override
  final DemoQuestionKind kind = DemoQuestionKind.memoryCards;
  @override
  final QuizSentence sentence;
  final List<String> letters;

  const MemoryCardDemoQuestion({
    required this.sentence,
    required this.letters,
  });
}

class CellPos {
  final int row;
  final int col;
  const CellPos(this.row, this.col);
}

class MemoryCardItem {
  final String letter;
  final bool revealed;
  final bool matched;

  const MemoryCardItem({
    required this.letter,
    required this.revealed,
    required this.matched,
  });
}

