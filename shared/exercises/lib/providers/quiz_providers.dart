import 'package:flutter_riverpod/flutter_riverpod.dart';

/// Tracks the current exercise index in the quiz flow.
final currentExerciseIndexProvider = StateProvider.autoDispose<int>(
  (ref) => 0,
);

