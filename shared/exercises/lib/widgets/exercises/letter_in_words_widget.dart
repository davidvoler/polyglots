import 'package:flutter/material.dart';

import '../../models/letter_in_words_exercise.dart';

class LetterInWordsWidget extends StatelessWidget {
  const LetterInWordsWidget({super.key, required this.exercise});

  final LetterInWordsExercise exercise;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Find words containing "${exercise.letter}"',
            style: Theme.of(context).textTheme.titleMedium,
          ),
          const SizedBox(height: 12),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: [
              ...exercise.correctOptions.map(
                (w) => Chip(
                  label: Text(w),
                  backgroundColor: Colors.green.withOpacity(0.2),
                ),
              ),
              ...exercise.incorrectOptions.map(
                (w) => Chip(
                  label: Text(w),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}

