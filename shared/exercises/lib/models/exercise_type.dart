enum ExerciseType {
  identifyWordsInSpeech,
  letterInWords,
  memoryGame,
  sentenceMultipleChoice,
  sentenceSingleChoice,
  typeQuestion,
  unknown,
}

extension ExerciseTypeX on ExerciseType {
  String get asKey {
    switch (this) {
      case ExerciseType.identifyWordsInSpeech:
        return 'identify_words_in_speech';
      case ExerciseType.letterInWords:
        return 'letter_in_words';
      case ExerciseType.memoryGame:
        return 'memory_game';
      case ExerciseType.sentenceMultipleChoice:
        return 'sentence_multiple_choice';
      case ExerciseType.sentenceSingleChoice:
        return 'sentence_single_choice';
      case ExerciseType.typeQuestion:
        return 'type_question';
      case ExerciseType.unknown:
        return 'unknown';
    }
  }

  static ExerciseType fromKey(String? raw) {
    switch (raw) {
      case 'identify_words_in_speech':
        return ExerciseType.identifyWordsInSpeech;
      case 'letter_in_words':
        return ExerciseType.letterInWords;
      case 'memory_game':
        return ExerciseType.memoryGame;
      case 'sentence_multiple_choice':
        return ExerciseType.sentenceMultipleChoice;
      case 'sentence_single_choice':
        return ExerciseType.sentenceSingleChoice;
      case 'type_question':
        return ExerciseType.typeQuestion;
      default:
        return ExerciseType.unknown;
    }
  }
}

