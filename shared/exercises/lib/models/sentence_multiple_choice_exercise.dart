import 'exercise.dart';
import 'exercise_type.dart';

class SentenceMultipleChoiceExercise extends Exercise {
  const SentenceMultipleChoiceExercise({
    required this.word,
    required this.options,
    String title = '',
    String instruction = '',
    String audioLink = '',
    Map<String, dynamic> extraData = const {},
  }) : super(
          type: ExerciseType.sentenceMultipleChoice,
          title: title,
          instruction: instruction,
          audioLink: audioLink,
          extraData: extraData,
        );

  final String word;
  final List<String> options;

  factory SentenceMultipleChoiceExercise.fromJson(Map<String, dynamic> json) {
    final extra =
        Map<String, dynamic>.from(json['extra_data'] as Map? ?? const {});
    final correct = List<String>.from(json['correct_options'] as List? ?? []);
    final wrong = List<String>.from(json['wrong_options'] as List? ?? []);
    return SentenceMultipleChoiceExercise(
      word: correct.isNotEmpty
          ? correct.first
          : (json['word'] as String? ?? ''),
      options: [...correct, ...wrong],
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
        'word': word,
        'options': options,
        'audio_link': audioLink,
        'extra_data': extraData,
      };
}

