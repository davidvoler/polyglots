import 'exercise.dart';
import 'exercise_type.dart';

class UnknownExercise extends Exercise {
  const UnknownExercise({
    this.raw = const {},
  }) : super(
          type: ExerciseType.unknown,
          extraData: const {},
        );

  final Map<String, dynamic> raw;

  @override
  Map<String, dynamic> toJson() => raw;
}

