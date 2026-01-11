import 'package:flutter/material.dart';

import '../../models/type_question_exercise.dart';

class TypeQuestionWidget extends StatelessWidget {
  const TypeQuestionWidget({super.key, required this.exercise});

  final TypeQuestionExercise exercise;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            exercise.title.isNotEmpty
                ? exercise.title
                : 'Type the word',
            style: Theme.of(context).textTheme.titleMedium,
          ),
          const SizedBox(height: 12),
          Text('Target word: ${exercise.word}'),
          const SizedBox(height: 12),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: exercise.keyboard
                .map(
                  (letter) => ElevatedButton(
                    onPressed: () {},
                    child: Text(letter),
                  ),
                )
                .toList(),
          ),
        ],
      ),
    );
  }
}

