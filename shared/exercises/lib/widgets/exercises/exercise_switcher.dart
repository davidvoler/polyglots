import 'package:flutter/material.dart';

import '../../models/models.dart';
import 'identify_words_in_speech_widget.dart';
import 'letter_in_words_widget.dart';
import 'memory_game_widget.dart';
import 'sentence_multiple_choice_widget.dart';
import 'sentence_single_choice_widget.dart';
import 'type_question_widget.dart';
import 'unknown_exercise_widget.dart';

class ExerciseSwitcher extends StatelessWidget {
  const ExerciseSwitcher({super.key, required this.exercise});

  final Exercise exercise;

  @override
  Widget build(BuildContext context) {
    switch (exercise.type) {
      case ExerciseType.identifyWordsInSpeech:
        return IdentifyWordsInSpeechWidget(
          exercise: exercise as IdentifyWordsInSpeechExercise,
        );
      case ExerciseType.letterInWords:
        return LetterInWordsWidget(
          exercise: exercise as LetterInWordsExercise,
        );
      case ExerciseType.memoryGame:
        return MemoryGameWidget(
          exercise: exercise as MemoryGameExercise,
        );
      case ExerciseType.sentenceMultipleChoice:
        return SentenceMultipleChoiceWidget(
          exercise: exercise as SentenceMultipleChoiceExercise,
        );
      case ExerciseType.sentenceSingleChoice:
        return SentenceSingleChoiceWidget(
          exercise: exercise as SentenceSingleChoiceExercise,
        );
      case ExerciseType.typeQuestion:
        return TypeQuestionWidget(
          exercise: exercise as TypeQuestionExercise,
        );
      case ExerciseType.unknown:
        return UnknownExerciseWidget(exercise: exercise);
    }
  }
}

