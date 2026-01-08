import 'package:flutter/material.dart';

class TypingQuestion extends StatelessWidget {
  final String targetWord;
  final List<String> letters;
  final bool showPrompt;
  final double typingTimeLeft;
  final TextEditingController controller;
  final bool submitted;
  final bool isCorrect;
  final void Function(String) onChanged;
  final void Function(String) onLetterTap;

  const TypingQuestion({
    super.key,
    required this.targetWord,
    required this.letters,
    required this.showPrompt,
    required this.typingTimeLeft,
    required this.controller,
    required this.submitted,
    required this.isCorrect,
    required this.onChanged,
    required this.onLetterTap,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          showPrompt ? 'Memorize this word' : 'Type the word you just saw:',
          style: TextStyle(color: Colors.grey.shade700, fontWeight: FontWeight.w600),
        ),
        const SizedBox(height: 8),
        if (showPrompt)
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: Colors.blue.shade50,
              borderRadius: BorderRadius.circular(12),
            ),
            child: Text(
              targetWord,
              textAlign: TextAlign.center,
              style: const TextStyle(fontSize: 32, fontWeight: FontWeight.bold),
            ),
          ),
        if (!showPrompt)
          LinearProgressIndicator(
            value: typingTimeLeft / 10.0,
            backgroundColor: Colors.grey.shade200,
            valueColor: AlwaysStoppedAnimation<Color>(typingTimeLeft > 3 ? Colors.blue : Colors.red),
            minHeight: 8,
          ),
        const SizedBox(height: 12),
        TextField(
          controller: controller,
          onChanged: onChanged,
          decoration: const InputDecoration(
            border: OutlineInputBorder(),
            hintText: 'Type here…',
          ),
          enabled: !submitted && !showPrompt ? true : !showPrompt ? true : false,
          readOnly: showPrompt,
        ),
        const SizedBox(height: 12),
        if (!showPrompt)
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: letters
                .map(
                  (c) => ElevatedButton(
                    onPressed: submitted ? null : () => onLetterTap(c),
                    child: Text(c),
                  ),
                )
                .toList(),
          ),
        if (submitted)
          Padding(
            padding: const EdgeInsets.only(top: 12),
            child: Text(
              isCorrect ? 'Correct!' : 'Incorrect. The word was "$targetWord".',
              style: TextStyle(
                color: isCorrect ? Colors.green.shade700 : Colors.red.shade700,
                fontWeight: FontWeight.w600,
              ),
            ),
          ),
      ],
    );
  }
}

