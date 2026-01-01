import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'user_preferences_service.dart';

class UserService {
  static const int _timeoutSeconds = 10;

  static String get _baseUrl {
    // Use localhost for local development, otherwise use the configured URL
    // if (const bool.fromEnvironment('dart.vm.product') == false) {
    //   // Development mode - use localhost
    //   return 'localhost:8000';
    // }
    return dotenv.env['BASE_PATH'] ?? 'https://polyglots.social';
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

  // Fetch user preferences from backend
  static Future<bool> loadUserPreferences() async {
    if (UserPreferencesService.userId.isEmpty) {
      print('loadUserPreferences: userId is empty');
      return false;
    }

    try {
      final client = http.Client();
      final url = _getUri('/api/v1/auth/get_user_pref');
      final data = {'user_id': UserPreferencesService.userId};

      print('🔗 Fetching user preferences from: $url');

      final response = await client.post(
        url,
        body: json.encode(data),
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
      ).timeout(
        Duration(seconds: _timeoutSeconds),
        onTimeout: () {
          print('loadUserPreferences timeout');
          return http.Response('Timeout', 408);
        },
      );

      print('📥 loadUserPreferences status code: ${response.statusCode}');

      if (response.statusCode == 200) {
        final Map<String, dynamic> responseData = json.decode(response.body);
        print('📥 loadUserPreferences: $responseData');

        // Check if user data exists
        if (responseData.containsKey('user') && responseData['user'] != null) {
          final user = responseData['user'];
          final userVocab = responseData.containsKey('user_vocab') && 
                           responseData['user_vocab'] != null
              ? responseData['user_vocab']
              : {};

          // Update user preferences
          UserPreferencesService.userId = user['user_id'] ?? UserPreferencesService.userId;
          UserPreferencesService.lang = user['lang'] ?? '';
          UserPreferencesService.toLang = user['to_lang'] ?? '';
          UserPreferencesService.corpus = user['corpus'] ?? '';
          UserPreferencesService.practiceId = userVocab['current_practice_id'] ?? '';
          UserPreferencesService.practiceType = userVocab['current_practice_type'] ?? '';

          return true;
        }
      }
      return false;
    } catch (e) {
      print('❌ loadUserPreferences failed: $e');
      return false;
    }
  }

  // Fetch user status from backend
  static Future<bool> loadUserStatus() async {
    if (UserPreferencesService.userId.isEmpty) {
      print('loadUserStatus: userId is empty');
      return false;
    }

    try {
      final client = http.Client();
      final url = _getUri('/api/v1/auth/user_status');
      final data = {
        'user_id': UserPreferencesService.userId,
        'lang': UserPreferencesService.sourceLanguage.code,
        'to_lang': UserPreferencesService.targetLanguage.code,
        'corpus': UserPreferencesService.corpus,
      };

      print('🔗 Fetching user status from: $url');

      final response = await client.post(
        url,
        body: json.encode(data),
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
      ).timeout(
        Duration(seconds: _timeoutSeconds),
        onTimeout: () {
          print('loadUserStatus timeout');
          return http.Response('Timeout', 408);
        },
      );

      print('📥 loadUserStatus status code: ${response.statusCode}');

      if (response.statusCode == 200) {
        final Map<String, dynamic> responseData = json.decode(response.body);
        print('📥 loadUserStatus: $responseData');

        // Update user stats
        UserPreferencesService.completed = responseData['completed'] ?? 0;
        UserPreferencesService.remaining = responseData['remaining'] ?? 0;
        UserPreferencesService.accuracy = responseData['accuracy'] ?? 0;
        UserPreferencesService.times = responseData['times'] ?? 0;
        UserPreferencesService.minutes = responseData['minutes'] ?? 0;

        return true;
      }
      return false;
    } catch (e) {
      print('❌ loadUserStatus failed: $e');
      return false;
    }
  }

  // Initialize user data
  static Future<bool> initializeUser() async {
    try {
      final prefsLoaded = await loadUserPreferences();
      final statusLoaded = await loadUserStatus();
      
      return prefsLoaded || statusLoaded; // Return true if at least one succeeds
    } catch (e) {
      print('❌ Failed to initialize user from backend: $e');
      // Set default values if backend is not accessible
      UserPreferencesService.userId = 'ebd27953d70f';
      UserPreferencesService.lang = 'en';
      UserPreferencesService.toLang = 'fr';
      UserPreferencesService.corpus = 'common';
      UserPreferencesService.practiceId = '6';
      UserPreferencesService.practiceType = 'step';
      
      return false; // Backend not accessible, using defaults
    }
  }
  
  // Legacy methods for backward compatibility
  static Future<bool> saveUserPreferences() async {
    // This method is now handled by the new API service
    return true;
  }
  
  static Future<bool> saveQuizResults({
    required int score,
    required int totalQuestions,
    required int correctAnswers,
    required int incorrectAnswers,
  }) async {
    // This method is now handled by the new API service
    return true;
  }
} 