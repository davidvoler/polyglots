import 'dart:convert';

import 'package:http/http.dart' as http;

import '../models/models.dart';

class ExercisesService {
  ExercisesService({
    http.Client? client,
    String? baseUrl,
  })  : _client = client ?? http.Client(),
        baseUrl = baseUrl ?? const String.fromEnvironment(
          'EXERCISES_BASE_URL',
          defaultValue: '',
        );

  final http.Client _client;
  final String baseUrl;

  Future<List<Exercise>> fetchExercises() async {
    if (baseUrl.isEmpty) {
      return _loadLocalMock();
    }

    final uri = Uri.parse('$baseUrl/exercises');
    final response = await _client.get(uri);
    if (response.statusCode != 200) {
      throw Exception(
        'Failed to load exercises (status ${response.statusCode})',
      );
    }

    final payload = jsonDecode(response.body) as List<dynamic>;
    return payload
        .map((entry) => Exercise.fromJson(entry as Map<String, dynamic>))
        .toList();
  }

  Future<List<Exercise>> _loadLocalMock() async {
    final mock = <Map<String, dynamic>>[
      {
        'exercise_type': ExerciseType.identifyWordsInSpeech.asKey,
        'title': 'Identify words',
        'instruction': 'Pick the words you hear.',
        'sentence': 'The quick brown fox jumps over the lazy dog',
        'correct_options': ['quick', 'brown', 'fox'],
        'wrong_options': ['table', 'mouse', 'screen'],
      },
      {
        'exercise_type': ExerciseType.letterInWords.asKey,
        'title': 'Letter in words',
        'instruction': 'Select the words containing the letter A.',
        'letter': 'a',
        'correct_options': ['apple', 'car', 'map'],
        'wrong_options': ['desk', 'phone', 'light'],
      },
      {
        'exercise_type': ExerciseType.memoryGame.asKey,
        'title': 'Memory grid',
        'instruction': 'Find the matching pairs.',
        'extra_data': {
          'grid': [
            ['A', 'B'],
            ['B', 'A'],
          ],
        },
      },
      {
        'exercise_type': ExerciseType.sentence_multiple_choice.asKey,
        'title': 'Fill the blank',
        'instruction': 'Choose the correct word.',
        'word': 'cat',
        'correct_options': ['cat'],
        'wrong_options': ['dog', 'bird', 'fish'],
      },
      {
        'exercise_type': ExerciseType.sentence_single_choice.asKey,
        'title': 'Choose the right sentence',
        'instruction': 'Pick the translated sentence.',
        'sentence': 'El gato duerme.',
        'correct_options': ['The cat sleeps.'],
        'wrong_options': ['The dog sleeps.', 'The cat runs.'],
      },
      {
        'exercise_type': ExerciseType.typeQuestion.asKey,
        'title': 'Type the word',
        'instruction': 'Use the on-screen keyboard.',
        'extra_data': {
          'word': 'hola',
          'keyboard': ['h', 'o', 'l', 'a', 'b', 'c', 'd', 'e'],
        },
      },
    ];

    return mock.map(Exercise.fromJson).toList();
  }
}

