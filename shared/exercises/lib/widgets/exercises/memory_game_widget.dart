import 'package:flutter/material.dart';

import '../../models/memory_game_exercise.dart';

class MemoryGameWidget extends StatelessWidget {
  const MemoryGameWidget({super.key, required this.exercise});

  final MemoryGameExercise exercise;

  @override
  Widget build(BuildContext context) {
    final grid = exercise.grid;
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            exercise.title.isNotEmpty
                ? exercise.title
                : 'Memory game (${grid.length}x${grid.isNotEmpty ? grid.first.length : 0})',
            style: Theme.of(context).textTheme.titleMedium,
          ),
          const SizedBox(height: 12),
          if (grid.isEmpty)
            const Text('No grid data')
          else
            Table(
              border: TableBorder.all(color: Colors.grey.shade300),
              defaultVerticalAlignment: TableCellVerticalAlignment.middle,
              children: grid
                  .map(
                    (row) => TableRow(
                      children: row
                          .map(
                            (cell) => Padding(
                              padding: const EdgeInsets.all(8),
                              child: Center(child: Text('$cell')),
                            ),
                          )
                          .toList(),
                    ),
                  )
                  .toList(),
            ),
        ],
      ),
    );
  }
}

