import 'exercise.dart';
import 'exercise_type.dart';

class TypeQuestionExercise extends Exercise {
  const TypeQuestionExercise({
    required this.word,
    required this.keyboard,
    super.title,
    super.instruction,
    super.audioLink,
    super.extraData,
  }) : super(
          type: ExerciseType.typeQuestion,
        );

  final String word;
  final List<String> keyboard;

  factory TypeQuestionExercise.fromJson(Map<String, dynamic> json) {
    final extra =
        Map<String, dynamic>.from(json['extra_data'] as Map? ?? const {});
    final keyboard =
        List<String>.from(extra['keyboard'] as List? ?? const <String>[]);
    final word = (extra['word'] ?? json['word']) as String? ?? '';
    return TypeQuestionExercise(
      word: word,
      keyboard: keyboard,
      title: json['title'] as String? ?? '',
      instruction: json['instruction'] as String? ?? '',
      audioLink: json['audio_link'] as String? ?? '',
      extraData: extra,
    );
  }

  @override
  Map<String, dynamic> toJson() => {
        'exercise_type': type.asKey,
        'title': title,
        'instruction': instruction,
        'audio_link': audioLink,
        'extra_data': {
          ...extraData,
          'word': word,
          'keyboard': keyboard,
        },
      };
}

