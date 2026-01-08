import 'dart:convert';
import 'package:http/http.dart' as http;

// Models for word selection
class WordSelect {
  final String lang;
  final String word;
  final String pos;
  final int maxWcount;
  final int minWcount;
  final int sentencesCount;
  final int rootCount;

  WordSelect({
    required this.lang,
    required this.word,
    required this.pos,
    required this.maxWcount,
    required this.minWcount,
    required this.sentencesCount,
    required this.rootCount,
  });

  factory WordSelect.fromJson(Map<String, dynamic> json) {
    return WordSelect(
      lang: json['lang'] ?? '',
      word: json['word'] ?? '',
      pos: json['pos'] ?? '',
      maxWcount: json['max_wcount'] ?? 0,
      minWcount: json['min_wcount'] ?? 0,
      sentencesCount: json['sentences_count'] ?? 0,
      rootCount: json['root_count'] ?? 0,
    );
  }
}

class ModuleWords {
  final String name;
  final int num;
  final List<WordSelect> words;
  final int wordCount;

  ModuleWords({
    required this.name,
    required this.num,
    required this.words,
    required this.wordCount,
  });

  factory ModuleWords.fromJson(Map<String, dynamic> json) {
    return ModuleWords(
      name: json['name'] ?? '',
      num: json['num'] ?? 0,
      words: (json['words'] as List<dynamic>?)
          ?.map((word) => WordSelect.fromJson(word))
          .toList() ?? [],
      wordCount: json['word_count'] ?? 0,
    );
  }
}

class CourseGenerationService {
  // TODO: Update this to match your server URL
  static const String baseUrl = 'http://localhost:8002/api/v1';
  
  /// Select words for modules using the word selection API
  ///
  /// [lang] - Language code
  /// [wordsPerModules] - Number of words per module
  /// [ratioIncrease] - Ratio increase factor
  /// [skipCount] - Number of words to skip
  /// Returns a list of ModuleWords
  static Future<List<ModuleWords>> selectWordsForModules({
    required String lang,
    int wordsPerModules = 5,
    double ratioIncrease = 0.08,
    int skipCount = 0,
  }) async {
    try {
      final url = Uri.parse('$baseUrl/words_select/');

      final requestBody = {
        'lang': lang,
        'words_per_modules': wordsPerModules,
        'ratio_increase': ratioIncrease,
        'skip_count': skipCount,
      };

      final response = await http.post(
        url,
        headers: {
          'Content-Type': 'application/json',
        },
        body: jsonEncode(requestBody),
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        return data.map((module) => ModuleWords.fromJson(module)).toList();
      } else {
        throw Exception(
          'Failed to select words: ${response.statusCode} - ${response.body}',
        );
      }
    } catch (e) {
      throw Exception('Error selecting words: $e');
    }
  }

  /// Generate a course using the course generation API
  ///
  /// [request] - CourseTemplateRequest data
  /// Returns the GeneratedCourse response
  static Future<Map<String, dynamic>> generateCourse({
    required String lang,
    required String toLang,
    double wordsPerModuleStart = 2.0,
    double wordsPerModuleIncreaseFactor = 0.3,
    int sentenceLengthStart = 3,
    double sentenceLengthIncreaseFactor = 0.1,
    double verbs = 0.4,
    double nouns = 0.4,
    double adjectives = 0.1,
    double adverbs = 0.1,
    int grammarPerModule = 1,
    bool greetingModule = false,
    bool readingModule = false,
    bool readingExercises = false,
    bool writingExercises = false,
  }) async {
    try {
      final url = Uri.parse('$baseUrl/generate/course');
      
      final requestBody = {
        'lang': lang,
        'to_lang': toLang,
        'words_per_module_start': wordsPerModuleStart,
        'words_per_module_increase_factor': wordsPerModuleIncreaseFactor,
        'sentence_length_start': sentenceLengthStart,
        'sentence_length_increase_factor': sentenceLengthIncreaseFactor,
        'verbs': verbs,
        'nouns': nouns,
        'adjectives': adjectives,
        'adverbs': adverbs,
        'grammar_per_module': grammarPerModule,
        'greeting_module': greetingModule,
        'reading_module': readingModule,
        'reading_exercises': readingExercises,
        'writing_exercises': writingExercises,
      };

      final response = await http.post(
        url,
        headers: {
          'Content-Type': 'application/json',
        },
        body: jsonEncode(requestBody),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body) as Map<String, dynamic>;
      } else {
        throw Exception(
          'Failed to generate course: ${response.statusCode} - ${response.body}',
        );
      }
    } catch (e) {
      throw Exception('Error generating course: $e');
    }
  }

  /// Convert language name to language code
  static String getLanguageCode(String languageName) {
    final languageMap = {
      'English': 'en',
      'Spanish': 'es',
      'French': 'fr',
      'German': 'de',
      'Italian': 'it',
      'Portuguese': 'pt',
      'Japanese': 'ja',
      'Chinese': 'zh',
      'Korean': 'ko',
      'Arabic': 'ar',
      'Russian': 'ru',
      'Hindi': 'hi',
      'Turkish': 'tr',
      'Polish': 'pl',
      'Dutch': 'nl',
      'Swedish': 'sv',
      'Norwegian': 'no',
      'Danish': 'da',
      'Finnish': 'fi',
      'Greek': 'el',
      'Czech': 'cs',
      'Romanian': 'ro',
      'Hungarian': 'hu',
      'Thai': 'th',
      'Vietnamese': 'vi',
      'Indonesian': 'id',
    };
    return languageMap[languageName] ?? 'en';
  }
}

