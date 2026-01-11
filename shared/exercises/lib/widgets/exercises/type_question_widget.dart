import 'package:flutter/material.dart';

import '../../models/type_question_exercise.dart';

class TypeQuestionWidget extends StatefulWidget {
  const TypeQuestionWidget({super.key, required this.exercise});

  final TypeQuestionExercise exercise;

  @override
  State<TypeQuestionWidget> createState() => _TypeQuestionWidgetState();
}

class _TypeQuestionWidgetState extends State<TypeQuestionWidget> {
  late final TextEditingController _controller;

  @override
  void initState() {
    super.initState();
    _controller = TextEditingController();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _append(String letter) {
    final text = _controller.text;
    final selection = _controller.selection;
    final cursor = selection.isValid ? selection.baseOffset : text.length;
    final next = text.replaceRange(
      cursor,
      cursor,
      letter,
    );
    _controller.text = next;
    _controller.selection =
        TextSelection.collapsed(offset: cursor + letter.length);
  }

  void _backspace() {
    final text = _controller.text;
    if (text.isEmpty) return;
    final selection = _controller.selection;
    final cursor = selection.isValid ? selection.baseOffset : text.length;
    if (cursor <= 0) return;
    final next = text.replaceRange(cursor - 1, cursor, '');
    _controller.text = next;
    _controller.selection = TextSelection.collapsed(offset: cursor - 1);
  }

  void _clear() {
    _controller.clear();
  }

  @override
  Widget build(BuildContext context) {
    final exercise = widget.exercise;
    final keyboard = exercise.keyboard.toSet().toList()..sort();

    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            exercise.title.isNotEmpty ? exercise.title : 'Type the word',
            style: Theme.of(context).textTheme.titleMedium,
          ),
          const SizedBox(height: 12),
          Text(
            exercise.instruction.isNotEmpty
                ? exercise.instruction
                : 'Spell the word using the on-screen keyboard.',
          ),
          const SizedBox(height: 16),
          TextField(
            controller: _controller,
            decoration: InputDecoration(
              labelText: 'Your answer',
              hintText: 'Type here',
              suffixIcon: IconButton(
                tooltip: 'Clear',
                icon: const Icon(Icons.clear),
                onPressed: _controller.text.isEmpty ? null : _clear,
              ),
            ),
          ),
          const SizedBox(height: 16),
          Text(
            'Keyboard',
            style: Theme.of(context).textTheme.labelLarge,
          ),
          const SizedBox(height: 8),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: [
              ...keyboard.map(
                (letter) => ElevatedButton(
                  onPressed: () => _append(letter),
                  child: Text(letter),
                ),
              ),
              OutlinedButton.icon(
                onPressed: _controller.text.isEmpty ? null : _backspace,
                icon: const Icon(Icons.backspace),
                label: const Text('Backspace'),
              ),
            ],
          ),
          const SizedBox(height: 12),
          Text(
            'Target word: ${exercise.word}',
            style: Theme.of(context).textTheme.bodyMedium,
          ),
        ],
      ),
    );
  }
}

