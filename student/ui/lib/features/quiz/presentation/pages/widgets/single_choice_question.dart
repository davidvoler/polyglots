import 'package:flutter/material.dart';

import '../../../../../shared/models/quiz_model.dart';

class SingleChoiceQuestion extends StatelessWidget {
  final List<QuizOption> options;
  final Set<int> selected;
  final bool submitted;
  final void Function(int) onTap;

  const SingleChoiceQuestion({
    super.key,
    required this.options,
    required this.selected,
    required this.submitted,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: options.length,
      itemBuilder: (context, idx) {
        final opt = options[idx];
        final isSelected = selected.contains(idx);
        final showResult = submitted;
        final correct = opt.correct;

        Color bg = Colors.white;
        Color border = Colors.grey.shade300;
        if (showResult && correct) {
          bg = Colors.green.shade50;
          border = Colors.green.shade300;
        } else if (isSelected && showResult && !correct) {
          bg = Colors.red.shade50;
          border = Colors.red.shade300;
        } else if (isSelected) {
          bg = Colors.blue.shade50;
          border = Colors.blue.shade300;
        }

        return Container(
          margin: const EdgeInsets.only(bottom: 12),
          decoration: BoxDecoration(
            color: bg,
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: border),
          ),
          child: ListTile(
            onTap: () => onTap(idx),
            title: Text(opt.sentence),
            trailing: isSelected
                ? const Icon(Icons.check_circle, color: Colors.blue)
                : const Icon(Icons.radio_button_unchecked),
          ),
        );
      },
    );
  }
}

