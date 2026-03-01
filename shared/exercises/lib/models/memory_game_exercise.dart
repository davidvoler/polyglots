import 'exercise.dart';
import 'exercise_type.dart';

class MemoryGameExercise extends Exercise {
  const MemoryGameExercise({
    required this.grid,
    super.title,
    super.instruction,
    super.audioLink,
    super.extraData,
  }) : super(
          type: ExerciseType.memoryGame,
        );

  final List<List<String>> grid;

  factory MemoryGameExercise.fromJson(Map<String, dynamic> json) {
    final extra =
        Map<String, dynamic>.from(json['extra_data'] as Map? ?? const {});
    final rawGrid = extra['grid'] as List? ?? const [];
    final parsedGrid = rawGrid
        .map(
          (row) => List<String>.from(row as List? ?? const []),
        )
        .toList();
    return MemoryGameExercise(
      grid: parsedGrid,
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
          'grid': grid,
        },
      };
}

