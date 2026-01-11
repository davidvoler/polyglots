import 'package:flutter/material.dart';

import '../../models/sentence_single_choice_exercise.dart';

class SentenceSingleChoiceWidget extends StatelessWidget {
  const SentenceSingleChoiceWidget({super.key, required this.exercise});

  final SentenceSingleChoiceExercise exercise;

  @override
  Widget build(BuildContext context) {
    final options = [
      exercise.correctOption,
      ...exercise.wrongOptions,
    ];

    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            exercise.title.isNotEmpty
                ? exercise.title
                : 'Choose the right sentence',
            style: Theme.of(context).textTheme.titleMedium,
          ),
          const SizedBox(height: 12),
          Text('Sentence: ${exercise.sentence}'),
          const SizedBox(height: 12),
          ...options.map(
            (opt) => ListTile(
              title: Text(opt),
              leading: const Icon(Icons.circle_outlined),
              onTap: () {},
            ),
          ),
        ],
      ),
    );
  }
}

