import 'package:flutter/material.dart';

import 'question_types_models.dart';

class WordSearchQuestion extends StatelessWidget {
  final List<String> grid;
  final List<CellPos> selectedCells;
  final bool submitted;
  final bool isCorrect;
  final void Function(int row, int col) onCellTap;

  const WordSearchQuestion({
    super.key,
    required this.grid,
    required this.selectedCells,
    required this.submitted,
    required this.isCorrect,
    required this.onCellTap,
  });

  @override
  Widget build(BuildContext context) {
    return AspectRatio(
      aspectRatio: 1,
      child: GridView.builder(
        physics: const NeverScrollableScrollPhysics(),
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 10,
        ),
        itemCount: 100,
        itemBuilder: (context, idx) {
          final row = idx ~/ 10;
          final col = idx % 10;
          final letter = grid[row][col].toUpperCase();
          final selected = selectedCells.any((c) => c.row == row && c.col == col);
          final matched = submitted && isCorrect && selected;

          Color bg = Colors.white;
          Color border = Colors.grey.shade300;
          if (selected) {
            bg = Colors.blue.shade50;
            border = Colors.blue.shade400;
          }
          if (matched) {
            bg = Colors.green.shade50;
            border = Colors.green.shade400;
          }

          return GestureDetector(
            onTap: () => onCellTap(row, col),
            child: Container(
              decoration: BoxDecoration(
                color: bg,
                border: Border.all(color: border),
              ),
              child: Center(
                child: Text(
                  letter,
                  style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w700),
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}

