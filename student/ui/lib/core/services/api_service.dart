import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_dotenv/flutter_dotenv.dart';
import '../../shared/models/quiz_model.dart';
import '../../shared/models/language_model.dart';

class ApiService {
  static const int _timeoutSeconds = 10;
  
  static String get _baseUrl {
    // Use localhost for local development, otherwise use the configured URL
    // if (const bool.fromEnvironment('dart.vm.product') == false) {
    //   // Development mode - use localhost
    //   return 'http://localhost:8000';
    // }
    final base =  dotenv.env['BASE_PATH'] ?? 'https://polyglots.social';
    print('🔗 API Configuration:');
    print('   Base URL: ${base}');
    print('   HTTPS: $_isHttps');
    return base;
  }
  
  static bool get _isHttps {
    // Use HTTP for localhost, HTTPS for production
    if (const bool.fromEnvironment('dart.vm.product') == false) {
      return false; // HTTP for localhost
    }
    return dotenv.env['IS_HTTPS'] == '1';
  }
  
  static Uri _getUri(String path) {
    if (_isHttps) {
      return Uri.https(_baseUrl, path);
    } else {
      return Uri.http(_baseUrl, path);
    }
  }
  
  static String get _baseSoundUrl {
    // Use localhost for local development, otherwise use the configured URL
    // if (const bool.fromEnvironment('dart.vm.product') == false) {
    //   // Development mode - use localhost
    //   return 'http://localhost:8000';
    // }
    return dotenv.env['BASE_SOUND_URL'] ?? 'https://polyglots.social';
  }
  
  static String getSoundUrl(String? soundPath) {
    if (soundPath == null || soundPath.isEmpty) {
      print('❌ Sound path is null or empty');
      return '';
    }
    
    final fullUrl = '$_baseSoundUrl$soundPath';
    print('🔊 Generated sound URL: $fullUrl');
    return fullUrl;
  }
  
  // Test if audio file is accessible
  static Future<bool> testAudioUrl(String? soundPath) async {
    if (soundPath == null || soundPath.isEmpty) return false;
    
    try {
      final audioUrl = getSoundUrl(soundPath);
      final response = await http.head(Uri.parse(audioUrl));
      final isAccessible = response.statusCode == 200;
      print('🔊 Audio file accessible: $isAccessible (${response.statusCode})');
      return isAccessible;
    } catch (e) {
      print('❌ Audio file not accessible: $e');
      return false;
    }
  }
  
  static Future<Quiz> getQuiz(QuizRequest request) async {
    try {
      final url = _getUri('/api/v1/quiz/get_quiz');
      final client = http.Client();

      print('🔗 API Configuration:');
      print('   Base URL: ${_baseUrl}');
      print('   HTTPS: $_isHttps');
      print('   Full URL: $url');
      print('📤 Request data: ${request.toJson()}');

      final response = await client.post(
        url,
        body: json.encode(request.toJson()),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Authorization': 'Some token', // TODO: Implement proper auth
        },
      ).timeout(
        Duration(seconds: _timeoutSeconds),
        onTimeout: () {
          throw TimeoutException('Connection timeout, please try again later');
        },
      );

      print('📥 Response status: ${response.statusCode}');
      print('📥 Response body: ${response.body}');

      if (response.statusCode == 200) {
        final Map<String, dynamic> responseData =
            json.decode(utf8.decode(response.bodyBytes));
        return Quiz.fromJson(responseData);
      } else {
        throw ApiException(
          'API error: Status ${response.statusCode}',
          response.statusCode,
          response.body,
        );
      }
    } catch (e) {
      print('❌ API error: $e');
      if (e is ApiException) {
        rethrow;
      }
      throw ApiException('Network error: $e', 0, e.toString());
    }
  }
  
  // Fallback method to create a demo quiz when API fails
  static Quiz createDemoQuiz({
    required String lang,
    required String toLang,
    String practiceId = 'demo_practice',
    String practiceType = 'demo',
  }) {
    // Get language objects for better demo content
    final sourceLang = SupportedLanguages.findByCode(lang) ?? SupportedLanguages.defaultSource;
    final targetLang = SupportedLanguages.findByCode(toLang) ?? SupportedLanguages.defaultTarget;
    
    // Create dynamic demo content based on selected languages
    final demoSentences = _createDemoSentences(sourceLang, targetLang);
    
    return Quiz(
      lang: lang,
      toLang: toLang,
      sentences: demoSentences,
      mode: 'demo',
      practiceType: practiceType,
      practiceId: practiceId,
      dialogueId: '',
      remaining: 0.0,
      practiceTimes: 0.0,
      practiceMark: 0.0,
      accuracy: 0.0,
    );
  }
  
  // Helper method to create dynamic demo sentences based on selected languages
  static List<QuizSentence> _createDemoSentences(Language sourceLang, Language targetLang) {
    // Common demo content for different language pairs
    final demoContent = {
      'en': {
        'fr': [
          {
            'question': 'What does "Bonjour" mean in English?',
            'correct': 'Hello',
            'options': ['Hello', 'Goodbye', 'Thank you', 'Please'],
            'word': 'Bonjour',
            'translit': 'bohn-ZHOOR',
          },
          {
            'question': 'How do you say "Thank you" in French?',
            'correct': 'Merci',
            'options': ['Bonjour', 'Merci', 'Au revoir', 'S\'il vous plaît'],
            'word': 'Merci',
            'translit': 'mehr-SEE',
          },
        ],
        'es': [
          {
            'question': 'What does "Hola" mean in English?',
            'correct': 'Hello',
            'options': ['Hello', 'Goodbye', 'Thank you', 'Please'],
            'word': 'Hola',
            'translit': 'OH-lah',
          },
          {
            'question': 'How do you say "Thank you" in Spanish?',
            'correct': 'Gracias',
            'options': ['Hola', 'Gracias', 'Adiós', 'Por favor'],
            'word': 'Gracias',
            'translit': 'GRAH-see-ahs',
          },
        ],
        'de': [
          {
            'question': 'What does "Hallo" mean in English?',
            'correct': 'Hello',
            'options': ['Hello', 'Goodbye', 'Thank you', 'Please'],
            'word': 'Hallo',
            'translit': 'HAH-loh',
          },
          {
            'question': 'How do you say "Thank you" in German?',
            'correct': 'Danke',
            'options': ['Hallo', 'Danke', 'Auf Wiedersehen', 'Bitte'],
            'word': 'Danke',
            'translit': 'DAHN-kuh',
          },
        ],
      },
    };
    
    // Get demo content for the language pair, or use default
    final content = demoContent[sourceLang.code]?[targetLang.code] ?? 
                   demoContent['en']?['fr'] ?? 
                   demoContent['en']!['fr']!;
    
    return content.asMap().entries.map((entry) {
      final index = entry.key;
      final item = entry.value;
      
      return QuizSentence(
        sentence: item['question'] as String,
        options: (item['options'] as List<String>).map((option) => 
          QuizOption(
            sentence: option,
            correct: option == item['correct'],
          )
        ).toList(),
        words: [item['word'] as String],
        id: 'demo_${index + 1}',
        translit: item['translit'] as String,
        sound: '/demo/${(item['word'] as String).toLowerCase()}.mp3',
      );
    }).toList();
  }
}

class ApiException implements Exception {
  final String message;
  final int statusCode;
  final String responseBody;
  
  ApiException(this.message, this.statusCode, this.responseBody);
  
  @override
  String toString() => 'ApiException: $message (Status: $statusCode)';
}

class TimeoutException implements Exception {
  final String message;
  
  TimeoutException(this.message);
  
  @override
  String toString() => 'TimeoutException: $message';
} 