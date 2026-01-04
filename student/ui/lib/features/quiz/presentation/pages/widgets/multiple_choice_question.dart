import 'package:flutter/material.dart';

import '../../../../../shared/models/quiz_model.dart';

class MultipleChoiceQuestion extends StatelessWidget {
  final List<QuizOption> options;
  final Set<int> selected;
  final bool submitted;
  final void Function(int) onToggle;

  const MultipleChoiceQuestion({
    super.key,
    required this.options,
    required this.selected,
    required this.submitted,
    required this.onToggle,
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
        if (showResult) {
          if (correct) {
            bg = Colors.green.shade50;
            border = Colors.green.shade300;
          } else if (isSelected) {
            bg = Colors.red.shade50;
            border = Colors.red.shade300;
          }
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
          child: CheckboxListTile(
            value: isSelected,
            onChanged: submitted ? null : (_) => onToggle(idx),
            title: Text(opt.sentence),
            controlAffinity: ListTileControlAffinity.leading,
          ),
        );
      },
    );
  }
}

