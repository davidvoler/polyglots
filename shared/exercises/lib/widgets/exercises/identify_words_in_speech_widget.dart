import 'package:flutter/material.dart';

import '../../models/identify_words_in_speech_exercise.dart';

class IdentifyWordsInSpeechWidget extends StatelessWidget {
  const IdentifyWordsInSpeechWidget({super.key, required this.exercise});

  final IdentifyWordsInSpeechExercise exercise;

  @override
  Widget build(BuildContext context) {
    final options = [
      ...exercise.correctOptions.map((e) => (e, true)),
      ...exercise.incorrectOptions.map((e) => (e, false)),
    ];

    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (exercise.instruction.isNotEmpty)
            Text(
              exercise.instruction,
              style: Theme.of(context).textTheme.titleMedium,
            ),
          const SizedBox(height: 12),
          Text(
            exercise.text,
            style: Theme.of(context).textTheme.bodyLarge,
          ),
          const SizedBox(height: 16),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: options
                .map(
                  (entry) => Chip(
                    label: Text(entry.$1),
                    backgroundColor:
                        entry.$2 ? Colors.green.withOpacity(0.2) : null,
                  ),
                )
                .toList(),
          ),
        ],
      ),
    );
  }
}

