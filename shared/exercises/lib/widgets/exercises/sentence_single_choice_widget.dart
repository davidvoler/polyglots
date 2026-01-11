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
            'Choose the right translation for:',
            style: Theme.of(context).textTheme.titleMedium,
          ),
          const SizedBox(height: 8),
          Text(
            exercise.sentence,
            style: Theme.of(context)
                .textTheme
                .headlineSmall
                ?.copyWith(fontWeight: FontWeight.w600),
          ),
          const SizedBox(height: 16),
          ...options.map(
            (opt) => ListTile(
              title: Text(
                opt,
                style: Theme.of(context)
                    .textTheme
                    .titleMedium
                    ?.copyWith(fontSize: 18),
              ),
              leading: const Icon(Icons.circle_outlined),
              onTap: () {},
            ),
          ),
        ],
      ),
    );
  }
}

