import 'dart:convert';

import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:http/http.dart' as http;

import '../../shared/models/course_model.dart';

class CourseService {
  static const int _timeoutSeconds = 10;

  static String get _baseUrl {
    return dotenv.env['BASE_PATH'] ?? 'https://polyglots.social';
  }

  static bool get _isHttps {
    if (const bool.fromEnvironment('dart.vm.product') == false) {
      return false;
    }
    return dotenv.env['IS_HTTPS'] == '1';
  }

  static Uri _getUri(String path) {
    return _isHttps ? Uri.https(_baseUrl, path) : Uri.http(_baseUrl, path);
  }

  static Future<List<Course>> fetchCourses({
    required String lang,
    required String toLang,
  }) async {
    try {
      final client = http.Client();
      final url = _getUri('/api/v1/course/');
      final payload = {'lang': lang, 'to_lang': toLang};

      final response = await client
          .post(
            url,
            body: json.encode(payload),
            headers: const {
              'Accept': 'application/json',
              'Content-Type': 'application/json',
            },
          )
          .timeout(
            const Duration(seconds: _timeoutSeconds),
            onTimeout: () => http.Response('Timeout', 408),
          );

      print('📥 fetchCourses status: ${response.statusCode}');

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        return data
            .map((item) => Course.fromJson(item as Map<String, dynamic>))
            .toList();
      }

      throw Exception('Failed to load courses (${response.statusCode})');
    } catch (e) {
      print('❌ fetchCourses failed: $e');
      rethrow;
    }
  }

  static Future<Course> fetchCourseById(int courseId) async {
    try {
      final client = http.Client();
      final url = _getUri('/api/v1/course/course/$courseId');

      final response = await client
          .get(
            url,
            headers: const {
              'Accept': 'application/json',
            },
          )
          .timeout(
            const Duration(seconds: _timeoutSeconds),
            onTimeout: () => http.Response('Timeout', 408),
          );

      print('📥 fetchCourseById status: ${response.statusCode}');

      if (response.statusCode == 200) {
        final Map<String, dynamic> data =
            json.decode(response.body) as Map<String, dynamic>;
        return Course.fromJson(data);
      }

      throw Exception('Failed to load course (${response.statusCode})');
    } catch (e) {
      print('❌ fetchCourseById failed: $e');
      rethrow;
    }
  }
}

