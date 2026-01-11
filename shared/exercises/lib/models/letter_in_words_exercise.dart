import 'exercise.dart';
import 'exercise_type.dart';

class LetterInWordsExercise extends Exercise {
  const LetterInWordsExercise({
    required this.letter,
    required this.correctOptions,
    required this.incorrectOptions,
    String title = '',
    String instruction = '',
    String audioLink = '',
    Map<String, dynamic> extraData = const {},
  }) : super(
          type: ExerciseType.letterInWords,
          title: title,
          instruction: instruction,
          audioLink: audioLink,
          extraData: extraData,
        );

  final String letter;
  final List<String> correctOptions;
  final List<String> incorrectOptions;

  factory LetterInWordsExercise.fromJson(Map<String, dynamic> json) {
    final extra =
        Map<String, dynamic>.from(json['extra_data'] as Map? ?? const {});
    return LetterInWordsExercise(
      letter: json['letter'] as String? ?? '',
      correctOptions:
          List<String>.from(json['correct_options'] as List? ?? const []),
      incorrectOptions:
          List<String>.from(json['wrong_options'] as List? ?? const []),
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
        'letter': letter,
        'correct_options': correctOptions,
        'wrong_options': incorrectOptions,
        'audio_link': audioLink,
        'extra_data': extraData,
      };
}

