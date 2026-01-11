import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'models/models.dart';
import 'providers/exercises_provider.dart';
import 'providers/quiz_providers.dart';
import 'widgets/exercises/exercise_switcher.dart';

void main() {
  runApp(const ProviderScope(child: MyApp()));
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Exercises',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const ExercisesPage(),
    );
  }
}

class ExercisesPage extends ConsumerWidget {
  const ExercisesPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final exercisesAsync = ref.watch(exercisesProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Exercises Quiz'),
      ),
      body: exercisesAsync.when(
        data: (items) {
          if (items.isEmpty) {
            return const Center(child: Text('No exercises found'));
          }

          final index = ref.watch(currentExerciseIndexProvider);
          final clampedIndex = index.clamp(0, items.length - 1);
          // If the state drifts beyond the available range, snap it back.
          if (clampedIndex != index) {
            WidgetsBinding.instance.addPostFrameCallback((_) {
              ref.read(currentExerciseIndexProvider.notifier).state =
                  clampedIndex;
            });
          }
          final exercise = items[clampedIndex];

          return Column(
            children: [
              Padding(
                padding:
                    const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      'Exercise ${clampedIndex + 1} of ${items.length}',
                      style: Theme.of(context).textTheme.titleMedium,
                    ),
                    Text(exercise.type.asKey),
                  ],
                ),
              ),
              const Divider(height: 1),
              Expanded(
                child: ExerciseSwitcher(exercise: exercise),
              ),
              const Divider(height: 1),
              Padding(
                padding:
                    const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                child: Row(
                  children: [
                    Expanded(
                      child: OutlinedButton(
                        onPressed: clampedIndex > 0
                            ? () => ref
                                .read(currentExerciseIndexProvider.notifier)
                                .state = clampedIndex - 1
                            : null,
                        child: const Text('Previous'),
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: ElevatedButton(
                        onPressed: clampedIndex < items.length - 1
                            ? () => ref
                                .read(currentExerciseIndexProvider.notifier)
                                .state = clampedIndex + 1
                            : null,
                        child: Text(
                          clampedIndex < items.length - 1
                              ? 'Next'
                              : 'Done',
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          );
        },
        error: (error, stackTrace) => Center(
          child: Text('Failed to load exercises: $error'),
        ),
        loading: () => const Center(child: CircularProgressIndicator()),
      ),
    );
  }
}
