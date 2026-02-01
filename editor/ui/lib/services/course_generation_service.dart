import 'dart:convert';
import 'package:http/http.dart' as http;

// Models for word selection (matches Python WordSelect: word, pos, min_wcount, max_wcount, sentences_count, root_count, greeting)
class WordSelect {
  final String lang;
  final String word;
  final String pos;
  final int maxWcount;
  final int minWcount;
  final int sentencesCount;
  final int rootCount;
  final bool greeting;

  WordSelect({
    required this.lang,
    required this.word,
    required this.pos,
    required this.maxWcount,
    required this.minWcount,
    required this.sentencesCount,
    required this.rootCount,
    this.greeting = false,
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
      greeting: json['greeting'] ?? false,
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

class CourseOption {
  final String code;
  final String name;
  CourseOption({required this.code, required this.name});
  factory CourseOption.fromJson(Map<String, dynamic> json) =>
      CourseOption(code: json['code'] ?? '', name: json['name'] ?? '');
}

class QuestionTypeOption {
  final String id;
  final String name;
  final String description;
  final String applicableTo;
  QuestionTypeOption({
    required this.id,
    required this.name,
    this.description = '',
    this.applicableTo = 'sentence',
  });
  factory QuestionTypeOption.fromJson(Map<String, dynamic> json) =>
      QuestionTypeOption(
        id: json['id'] ?? '',
        name: json['name'] ?? '',
        description: json['description'] ?? '',
        applicableTo: json['applicable_to'] ?? 'sentence',
      );
}

class CourseOptionsResponse {
  final List<CourseOption> languages;
  final List<QuestionTypeOption> questionTypes;
  CourseOptionsResponse({required this.languages, required this.questionTypes});
  factory CourseOptionsResponse.fromJson(Map<String, dynamic> json) =>
      CourseOptionsResponse(
        languages: (json['languages'] as List<dynamic>?)
            ?.map((e) => CourseOption.fromJson(e as Map<String, dynamic>))
            .toList() ?? [],
        questionTypes: (json['question_types'] as List<dynamic>?)
            ?.map((e) => QuestionTypeOption.fromJson(e as Map<String, dynamic>))
            .toList() ?? [],
      );
}

class WordCount {
  final String word;
  final int cnt;
  WordCount({required this.word, required this.cnt});
  factory WordCount.fromJson(Map<String, dynamic> json) =>
      WordCount(word: json['word'] ?? '', cnt: json['cnt'] ?? 0);
}

class WordWithWeight {
  final String word;
  final int weight;
  WordWithWeight({required this.word, required this.weight});
}

class SentenceForWordItem {
  final int id;
  final int toId;
  final String sentence;
  final String translation;
  final List<String> options;
  final int lenElm;
  SentenceForWordItem({
    required this.id,
    this.toId = 0,
    required this.sentence,
    required this.translation,
    this.options = const [],
    this.lenElm = 0,
  });
  factory SentenceForWordItem.fromJson(Map<String, dynamic> json) =>
      SentenceForWordItem(
        id: json['id'] ?? 0,
        toId: json['to_id'] ?? 0,
        sentence: json['sentence'] ?? '',
        translation: json['translation'] ?? '',
        options: (json['options'] as List<dynamic>?)?.cast<String>() ?? [],
        lenElm: json['len_elm'] ?? 0,
      );
}

class SentencesForWordResponse {
  final String word;
  final String lang;
  final String toLang;
  final List<SentenceForWordItem> sentences;
  SentencesForWordResponse({
    required this.word,
    required this.lang,
    required this.toLang,
    required this.sentences,
  });
  factory SentencesForWordResponse.fromJson(Map<String, dynamic> json) =>
      SentencesForWordResponse(
        word: json['word'] ?? '',
        lang: json['lang'] ?? '',
        toLang: json['to_lang'] ?? '',
        sentences: (json['sentences'] as List<dynamic>?)
            ?.map((e) => SentenceForWordItem.fromJson(e as Map<String, dynamic>))
            .toList() ?? [],
      );
}

class CourseGenerationService {
  // TODO: Update this to match your server URL
  static const String baseUrl = 'http://localhost:8005/api/v1';
  
  /// Step 1: Get course options (languages, question types)
  static Future<CourseOptionsResponse> getCourseOptions() async {
    final url = Uri.parse('$baseUrl/generate/course_options');
    final response = await http.get(url);
    if (response.statusCode != 200) throw Exception('Failed to load course options: ${response.statusCode}');
    return CourseOptionsResponse.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
  }

  /// Step 2a: Get greeting/polite words for lang
  static Future<List<ModuleWords>> getGreetingWords({required String lang}) async {
    final url = Uri.parse('$baseUrl/words_select/greeting_words');
    final response = await http.post(url, headers: {'Content-Type': 'application/json'}, body: jsonEncode({'lang': lang}));
    if (response.statusCode != 200) throw Exception('Failed to load greeting words: ${response.statusCode}');
    final List<dynamic> data = jsonDecode(response.body);
    return data.map((e) => ModuleWords.fromJson(e as Map<String, dynamic>)).toList();
  }

  /// Correct Wizard step 3: Load all words (greeting + corpus) from all_words
  static Future<List<WordSelect>> getAllWords({required String lang, int skipCount = 0}) async {
    final url = Uri.parse('$baseUrl/words_select/all_words');
    final response = await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'lang': lang, 'skip_count': skipCount}),
    );
    if (response.statusCode != 200) throw Exception('Failed to load words: ${response.statusCode}');
    final List<dynamic> data = jsonDecode(response.body);
    return data.map((e) => WordSelect.fromJson(e as Map<String, dynamic>)).toList();
  }

  /// Correct Wizard step 8: Submit ordered list of words with weight (sort order)
  static Future<Map<String, dynamic>> submitWords({
    required String lang,
    String toLang = '',
    required List<WordWithWeight> words,
  }) async {
    final url = Uri.parse('$baseUrl/words_select/submit_words');
    final response = await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'lang': lang, 'to_lang': toLang, 'words': words.map((w) => {'word': w.word, 'weight': w.weight}).toList()}),
    );
    if (response.statusCode != 200) throw Exception('Failed to submit words: ${response.statusCode}');
    return jsonDecode(response.body) as Map<String, dynamic>;
  }

  /// Step 2b: Get common words (most common first)
  static Future<List<WordCount>> getCommonWords({
    required String lang,
    int limit = 200,
    int offset = 0,
  }) async {
    final url = Uri.parse('$baseUrl/generate/common_words');
    final response = await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'lang': lang, 'limit': limit, 'offset': offset}),
    );
    if (response.statusCode != 200) throw Exception('Failed to load common words: ${response.statusCode}');
    final map = jsonDecode(response.body) as Map<String, dynamic>;
    final words = map['words'] as List<dynamic>? ?? [];
    return words.map((e) => WordCount.fromJson(e as Map<String, dynamic>)).toList();
  }

  /// Step 3a: Get sentences for a word (for selection)
  static Future<SentencesForWordResponse> getSentencesForWord({
    required String lang,
    required String toLang,
    required String word,
    int limit = 30,
  }) async {
    final url = Uri.parse('$baseUrl/generate/sentences_for_word');
    final response = await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'lang': lang, 'to_lang': toLang, 'word': word, 'limit': limit}),
    );
    if (response.statusCode != 200) throw Exception('Failed to load sentences: ${response.statusCode}');
    return SentencesForWordResponse.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
  }

  /// Step 3b: Get question types list
  static Future<List<QuestionTypeOption>> getQuestionTypes() async {
    final url = Uri.parse('$baseUrl/generate/question_types');
    final response = await http.get(url);
    if (response.statusCode != 200) throw Exception('Failed to load question types: ${response.statusCode}');
    final List<dynamic> data = jsonDecode(response.body);
    return data.map((e) => QuestionTypeOption.fromJson(e as Map<String, dynamic>)).toList();
  }

  /// Step 4: Create course from editor (words, sentences per word, question types, group into modules)
  static Future<Map<String, dynamic>> createCourseFromEditor({
    required String lang,
    required String toLang,
    required String title,
    String description = '',
    required List<String> selectedWords,
    required Map<String, List<int>> sentencesPerWord,
    required List<String> enabledQuestionTypes,
    bool automateLesson = false,
    int lessonsPerModule = 10,
  }) async {
    final url = Uri.parse('$baseUrl/generate/create_course_from_editor');
    final response = await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'lang': lang,
        'to_lang': toLang,
        'title': title,
        'description': description,
        'selected_words': selectedWords,
        'sentences_per_word': sentencesPerWord,
        'enabled_question_types': enabledQuestionTypes,
        'automate_lesson': automateLesson,
        'lessons_per_module': lessonsPerModule,
      }),
    );
    if (response.statusCode != 200) throw Exception('Failed to create course: ${response.statusCode} - ${response.body}');
    return jsonDecode(response.body) as Map<String, dynamic>;
  }
  
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

