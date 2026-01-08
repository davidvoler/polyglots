import 'package:flutter/material.dart';
import 'dart:math' as math;

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
    return LayoutBuilder(
      builder: (context, constraints) {
        // Make tiles square, slightly larger, and ensure everything fits without scrolling.
        const targetTileSize = 72.0;
        const spacing = 6.0;
        const minColumns = 3;
        final usableWidth = constraints.maxWidth;
        final usableHeight = constraints.maxHeight;

        int pickColumns() {
          if (cards.isEmpty) return minColumns;
          int maxColumns = math.max(minColumns, (usableWidth / targetTileSize).floor());
          maxColumns = math.min(maxColumns, cards.length);
          for (int cols = maxColumns; cols >= minColumns; cols--) {
            final rows = (cards.length / cols).ceil();
            final tileSize = (usableWidth - (cols - 1) * spacing) / cols;
            final neededHeight = rows * tileSize + (rows - 1) * spacing;
            if (neededHeight <= usableHeight) {
              return cols;
            }
          }
          return minColumns;
        }

        final crossAxisCount = pickColumns();

        return GridView.builder(
          physics: const NeverScrollableScrollPhysics(),
          gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: crossAxisCount,
            mainAxisSpacing: spacing,
            crossAxisSpacing: spacing,
            childAspectRatio: 1.0, // enforce square tiles
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
      },
    );
  }
}


