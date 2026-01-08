import 'package:flutter/material.dart';

class ExplanationQuestion extends StatelessWidget {
  final String text;

  const ExplanationQuestion({super.key, required this.text});

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      child: Text(
        text,
        style: const TextStyle(fontSize: 18),
      ),
    );
  }
}

