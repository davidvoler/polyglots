import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../models/models.dart';
import '../services/exercises_service.dart';

final exercisesServiceProvider = Provider<ExercisesService>((ref) {
  return ExercisesService();
});

final exercisesProvider = FutureProvider<List<Exercise>>((ref) {
  final service = ref.watch(exercisesServiceProvider);
  return service.fetchExercises();
});

