import 'exercise.dart';
import 'exercise_type.dart';

class SentenceSingleChoiceExercise extends Exercise {
  const SentenceSingleChoiceExercise({
    required this.sentence,
    required this.correctOption,
    required this.wrongOptions,
    String title = '',
    String instruction = '',
    String audioLink = '',
    Map<String, dynamic> extraData = const {},
  }) : super(
          type: ExerciseType.sentenceSingleChoice,
          title: title,
          instruction: instruction,
          audioLink: audioLink,
          extraData: extraData,
        );

  final String sentence;
  final String correctOption;
  final List<String> wrongOptions;

  factory SentenceSingleChoiceExercise.fromJson(Map<String, dynamic> json) {
    final extra =
        Map<String, dynamic>.from(json['extra_data'] as Map? ?? const {});
    final correctOptions =
        List<String>.from(json['correct_options'] as List? ?? const []);
    return SentenceSingleChoiceExercise(
      sentence: json['sentence'] as String? ?? '',
      correctOption: correctOptions.isNotEmpty ? correctOptions.first : '',
      wrongOptions:
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
        'sentence': sentence,
        'correct_options': [correctOption],
        'wrong_options': wrongOptions,
        'audio_link': audioLink,
        'extra_data': extraData,
      };
}

