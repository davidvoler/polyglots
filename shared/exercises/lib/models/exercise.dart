import 'exercise_type.dart';
import 'identify_words_in_speech_exercise.dart';
import 'letter_in_words_exercise.dart';
import 'memory_game_exercise.dart';
import 'sentence_multiple_choice_exercise.dart';
import 'sentence_single_choice_exercise.dart';
import 'type_question_exercise.dart';
import 'unknown_exercise.dart';

abstract class Exercise {
  const Exercise({
    required this.type,
    this.title = '',
    this.instruction = '',
    this.audioLink = '',
    this.extraData = const {},
  });

  final ExerciseType type;
  final String title;
  final String instruction;
  final String audioLink;
  final Map<String, dynamic> extraData;

  static Exercise fromJson(Map<String, dynamic> json) {
    final type = ExerciseTypeX.fromKey(json['exercise_type'] as String?);
    switch (type) {
      case ExerciseType.identifyWordsInSpeech:
        return IdentifyWordsInSpeechExercise.fromJson(json);
      case ExerciseType.letterInWords:
        return LetterInWordsExercise.fromJson(json);
      case ExerciseType.memoryGame:
        return MemoryGameExercise.fromJson(json);
      case ExerciseType.sentenceMultipleChoice:
        return SentenceMultipleChoiceExercise.fromJson(json);
      case ExerciseType.sentenceSingleChoice:
        return SentenceSingleChoiceExercise.fromJson(json);
      case ExerciseType.typeQuestion:
        return TypeQuestionExercise.fromJson(json);
      case ExerciseType.unknown:
        return UnknownExercise(raw: json);
    }
  }

  Map<String, dynamic> toJson();
}

