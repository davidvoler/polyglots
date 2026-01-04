import 'package:flutter/material.dart';

import 'question_types_models.dart';

class MemoryCardQuestion extends StatelessWidget {
  final List<MemoryCardItem> cards;
  final void Function(int index) onTap;
  final bool interactionEnabled;

  const MemoryCardQuestion({
    super.key,
    required this.cards,
    required this.onTap,
    this.interactionEnabled = true,
  });

  @override
  Widget build(BuildContext context) {
    return GridView.builder(
      physics: const NeverScrollableScrollPhysics(),
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 4,
        mainAxisSpacing: 8,
        crossAxisSpacing: 8,
      ),
      itemCount: cards.length,
      itemBuilder: (context, idx) {
        final card = cards[idx];
        final showing = card.matched || card.revealed;
        final bg = card.matched
            ? Colors.green.shade50
            : (showing ? Colors.blue.shade50 : Colors.white);
        final border = card.matched
            ? Colors.green.shade300
            : (showing ? Colors.blue.shade300 : Colors.grey.shade300);

        return GestureDetector(
          onTap: interactionEnabled ? () => onTap(idx) : null,
          child: Container(
            decoration: BoxDecoration(
              color: bg,
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: border),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.05),
                  blurRadius: 4,
                  offset: const Offset(0, 2),
                ),
              ],
            ),
            child: Center(
              child: Text(
                showing ? card.letter : '?',
                style: const TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ),
        );
      },
    );
  }
}


