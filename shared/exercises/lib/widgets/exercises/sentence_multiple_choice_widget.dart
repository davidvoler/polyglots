import 'package:flutter/material.dart';

import '../../models/sentence_multiple_choice_exercise.dart';

class SentenceMultipleChoiceWidget extends StatelessWidget {
  const SentenceMultipleChoiceWidget({super.key, required this.exercise});

  final SentenceMultipleChoiceExercise exercise;

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
                : 'Choose the correct word',
            style: Theme.of(context).textTheme.titleMedium,
          ),
          const SizedBox(height: 12),
          Text('Target word: ${exercise.word}'),
          const SizedBox(height: 12),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: exercise.options
                .map((opt) => OutlinedButton(
                      onPressed: () {},
                      child: Text(opt),
                    ))
                .toList(),
          ),
        ],
      ),
    );
  }
}

