import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'models/models.dart';
import 'providers/exercises_provider.dart';

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
        title: const Text('Exercises'),
      ),
      body: exercisesAsync.when(
        data: (items) {
          if (items.isEmpty) {
            return const Center(
              child: Text('No exercises found'),
            );
          }
          return ListView.separated(
            itemCount: items.length,
            separatorBuilder: (_, __) => const Divider(height: 1),
            itemBuilder: (context, index) {
              final exercise = items[index];
              return ListTile(
                title: Text(
                  exercise.title.isNotEmpty
                      ? exercise.title
                      : exercise.type.asKey,
                ),
                subtitle: Text(
                  exercise.instruction.isNotEmpty
                      ? exercise.instruction
                      : _subtitleFor(exercise),
                ),
                trailing: Text(exercise.type.asKey),
              );
            },
          );
        },
        error: (error, stackTrace) => Center(
          child: Text('Failed to load exercises: $error'),
        ),
        loading: () => const Center(child: CircularProgressIndicator()),
      ),
    );
  }

  String _subtitleFor(Exercise exercise) {
    switch (exercise.type) {
      case ExerciseType.identifyWordsInSpeech:
        final typed = exercise as IdentifyWordsInSpeechExercise;
        return 'Tap the words in: ${typed.text}';
      case ExerciseType.letterInWords:
        final typed = exercise as LetterInWordsExercise;
        return 'Find letter "${typed.letter}"';
      case ExerciseType.memoryGame:
        final typed = exercise as MemoryGameExercise;
        final rows = typed.grid.length;
        final cols = typed.grid.isNotEmpty ? typed.grid.first.length : 0;
        return 'Memory grid ${rows}x$cols';
      case ExerciseType.sentenceMultipleChoice:
        final typed = exercise as SentenceMultipleChoiceExercise;
        return 'Choose: ${typed.word}';
      case ExerciseType.sentenceSingleChoice:
        final typed = exercise as SentenceSingleChoiceExercise;
        return 'Translate: ${typed.sentence}';
      case ExerciseType.typeQuestion:
        final typed = exercise as TypeQuestionExercise;
        return 'Type: ${typed.word}';
      case ExerciseType.unknown:
        return 'Unknown exercise type';
    }
  }
}
