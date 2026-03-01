import 'exercise.dart';
import 'exercise_type.dart';

class IdentifyWordsInSpeechExercise extends Exercise {
  const IdentifyWordsInSpeechExercise({
    required this.text,
    required this.correctOptions,
    required this.incorrectOptions,
    super.title,
    super.instruction,
    super.audioLink,
    super.extraData,
  }) : super(
          type: ExerciseType.identifyWordsInSpeech,
        );

  final String text;
  final List<String> correctOptions;
  final List<String> incorrectOptions;

  factory IdentifyWordsInSpeechExercise.fromJson(Map<String, dynamic> json) {
    final extra =
        Map<String, dynamic>.from(json['extra_data'] as Map? ?? const {});
    return IdentifyWordsInSpeechExercise(
      text: json['sentence'] as String? ?? '',
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
        'sentence': text,
        'correct_options': correctOptions,
        'wrong_options': incorrectOptions,
        'audio_link': audioLink,
        'extra_data': extraData,
      };
}

