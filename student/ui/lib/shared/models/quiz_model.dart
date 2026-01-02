enum PracticeModes {
  words,
  step,
  structure,
  dialogue,
  dialogueLines,
  refresh,
}

class QuizOption {
  final String sentence;
  final bool correct;
  bool selected;

  QuizOption({
    required this.sentence,
    required this.correct,
    this.selected = false,
  });

  factory QuizOption.fromJson(Map<String, dynamic> json) {
    return QuizOption(
      sentence: json['option'] ?? '',
      correct: json['correct'] ?? false,
      selected: json['selected'] ?? false,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'option': sentence,
      'correct': correct,
      'selected': selected,
    };
  }
}

enum QuizQuestionType {
  singleChoice,
  multipleChoice,
  explanation,
  wordSearch,
}

class QuizSentence {
  final String sentence;
  final List<QuizOption> options;
  final List<dynamic> words;
  final String id;
  final String? dialogueId;
  final String? dialogueLine;
  final String? translit;
  final String? sound;
  final QuizQuestionType questionType;

  bool answered = false;
  int attempts = 0;

  QuizSentence({
    required this.sentence,
    required this.options,
    required this.words,
    required this.id,
    this.dialogueId,
    this.dialogueLine,
    this.translit,
    this.sound,
    this.questionType = QuizQuestionType.singleChoice,
  });

  factory QuizSentence.fromJson(Map<String, dynamic> json) {
    final typeString = (json['question_type'] ?? '').toString().toLowerCase();
    QuizQuestionType questionType = QuizQuestionType.singleChoice;
    if (typeString == 'multiple' ||
        typeString == 'multiple_choice' ||
        typeString == 'multi' ||
        typeString == 'multiple-select' ||
        typeString == 'multiple_selection') {
      questionType = QuizQuestionType.multipleChoice;
    } else if (typeString == 'explanation' ||
        typeString == 'info' ||
        typeString == 'informational') {
      questionType = QuizQuestionType.explanation;
    } else if (typeString == 'word_search' ||
        typeString == 'wordsearch' ||
        typeString == 'word-search') {
      questionType = QuizQuestionType.wordSearch;
    }

    return QuizSentence(
      sentence: json['sentence'] ?? '',
      words: json['words'] ?? [],
      id: json['sentence_id'] ?? '',
      sound: json['sound'],
      dialogueId: json['dialogue_id'],
      dialogueLine: json['dialogue_line'],
      translit: json['translit'],
      questionType: questionType,
      options: List<dynamic>.from(json['options'] ?? [])
          .map((i) => QuizOption.fromJson(i))
          .toList(),
    );
  }

  Map<String, dynamic> toJson() {
    String questionTypeString = 'single';
    if (questionType == QuizQuestionType.multipleChoice) {
      questionTypeString = 'multiple';
    } else if (questionType == QuizQuestionType.explanation) {
      questionTypeString = 'explanation';
    } else if (questionType == QuizQuestionType.wordSearch) {
      questionTypeString = 'word_search';
    }

    return {
      'sentence': sentence,
      'words': words,
      'sentence_id': id,
      'sound': sound,
      'dialogue_id': dialogueId,
      'dialogue_line': dialogueLine,
      'translit': translit,
      'question_type': questionTypeString,
      'options': options.map((option) => option.toJson()).toList(),
    };
  }

  bool hasAudio() {
    return sound != null && sound!.isNotEmpty;
  }
}

class Quiz {
  final String lang;
  final String toLang;
  final List<QuizSentence> sentences;
  final String mode;
  final String practiceType;
  final String practiceId;
  final String dialogueId;
  final double remaining;
  final double practiceTimes;
  final double practiceMark;
  final double accuracy;

  Quiz({
    required this.lang,
    required this.toLang,
    required this.sentences,
    required this.mode,
    required this.practiceType,
    required this.practiceId,
    required this.dialogueId,
    required this.remaining,
    required this.practiceTimes,
    required this.practiceMark,
    required this.accuracy,
  });

  factory Quiz.fromJson(Map<String, dynamic> json) {
    return Quiz(
      lang: json['lang'] ?? '',
      toLang: json['to_lang'] ?? '',
      mode: json['mode'] ?? '',
      practiceType: json['practice_type'] ?? '',
      practiceId: json['practice_id'] ?? '',
      dialogueId: json['dialogue_id'] ?? '',
      remaining: (json['remaining'] ?? 0).toDouble(),
      practiceTimes: (json['practice_times'] ?? 0).toDouble(),
      practiceMark: (json['practice_mark'] ?? 0).toDouble(),
      accuracy: (json['accuracy'] ?? 0).toDouble(),
      sentences: List<dynamic>.from(json['sentences'] ?? [])
          .map((i) => QuizSentence.fromJson(i))
          .toList(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'lang': lang,
      'to_lang': toLang,
      'mode': mode,
      'practice_type': practiceType,
      'practice_id': practiceId,
      'dialogue_id': dialogueId,
      'remaining': remaining,
      'practice_times': practiceTimes,
      'practice_mark': practiceMark,
      'accuracy': accuracy,
      'sentences': sentences.map((sentence) => sentence.toJson()).toList(),
    };
  }
}

class QuizRequest {
  final String userId;
  final String lang;
  final String toLang;
  final String corpus;
  final String practiceId;
  final String practiceType;
  final String practiceMode;
  final bool reverseMode;
  final String lastMode;

  QuizRequest({
    required this.userId,
    required this.lang,
    required this.toLang,
    required this.corpus,
    required this.practiceId,
    required this.practiceType,
    required this.practiceMode,
    required this.reverseMode,
    required this.lastMode,
  });

  Map<String, dynamic> toJson() {
    return {
      'user_id': userId,
      'lang': lang,
      'to_lang': toLang,
      'corpus': corpus,
      'practice_id': practiceId,
      'practice_type': practiceType,
      'practice_mode': practiceMode,
      'reverse_mode': reverseMode,
      'last_mode': lastMode,
    };
  }
} 