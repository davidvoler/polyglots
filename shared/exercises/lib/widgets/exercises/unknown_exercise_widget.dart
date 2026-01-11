import 'package:flutter/material.dart';

import '../../models/exercise.dart';
import '../../models/exercise_type.dart';

class UnknownExerciseWidget extends StatelessWidget {
  const UnknownExerciseWidget({super.key, required this.exercise});

  final Exercise exercise;

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Text('Unknown exercise type: ${exercise.type.asKey}'),
    );
  }
}

