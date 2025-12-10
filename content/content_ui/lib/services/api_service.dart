import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/corpus.dart';
import '../models/sentence.dart';
import '../models/requests.dart';

class ApiService {
  final String baseUrl;

  ApiService({this.baseUrl = 'http://localhost:8000'});

  // Get list of corpuses
  Future<List<Corpus>> getCorpuses() async {
    try {
      // Note: You'll need to create this endpoint in your FastAPI backend
      final response = await http.get(Uri.parse('$baseUrl/api/corpus'));
      
      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        return data.map((json) => Corpus.fromJson(json)).toList();
      } else {
        throw Exception('Failed to load corpuses: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error fetching corpuses: $e');
    }
  }

  // Add a new corpus
  Future<Corpus> addCorpus(AddCorpusRequest request) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/corpus'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(request.toJson()),
      );

      if (response.statusCode == 200 || response.statusCode == 201) {
        return Corpus.fromJson(json.decode(response.body));
      } else {
        throw Exception('Failed to add corpus: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error adding corpus: $e');
    }
  }

  // Translate corpus
  Future<Map<String, dynamic>> translateCorpus(TranslateRequest request) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/translate'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(request.toJson()),
      );

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Failed to translate corpus: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error translating corpus: $e');
    }
  }

  // Analyze sentences
  Future<Map<String, dynamic>> analyzeSentences(AnalyzeRequest request) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/analyze_sentence'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(request.toJson()),
      );

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Failed to analyze sentences: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error analyzing sentences: $e');
    }
  }

  // Get sentences for review
  Future<List<Sentence>> getSentencesForReview(ReviewRequest request) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/api/review').replace(
          queryParameters: {
            'operation': request.operation,
            'source': request.source,
            'lang': request.lang,
            'review': request.review.toString(),
            'limit': request.limit.toString(),
            'offset': request.offset.toString(),
          },
        ),
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        return data.map((json) => Sentence.fromJson(json)).toList();
      } else {
        throw Exception('Failed to load sentences: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error fetching sentences: $e');
    }
  }

  // Transliterate corpus
  Future<Map<String, dynamic>> transliterateCorpus(TransliterateRequest request) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/transliterate'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(request.toJson()),
      );

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Failed to transliterate corpus: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error transliterating corpus: $e');
    }
  }

  // Load CSV
  Future<Map<String, dynamic>> loadCsv(LoadCsvRequest request) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/load_csv'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(request.toJson()),
      );

      if (response.statusCode == 200 || response.statusCode == 201) {
        return json.decode(response.body);
      } else {
        throw Exception('Failed to load CSV: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error loading CSV: $e');
    }
  }

  // Generate content
  Future<Map<String, dynamic>> generateContent(GenerateContentRequest request) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/generate_content'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(request.toJson()),
      );

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Failed to generate content: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error generating content: $e');
    }
  }

  // Group sentences
  Future<Map<String, dynamic>> groupSentences(GroupSentencesRequest request) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/group_sentences'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(request.toJson()),
      );

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Failed to group sentences: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error grouping sentences: $e');
    }
  }

  // Process dialogues
  Future<Map<String, dynamic>> processDialogues(DialoguesRequest request) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/dialogues'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(request.toJson()),
      );

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Failed to process dialogues: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error processing dialogues: $e');
    }
  }

  // Analyze subtitles
  Future<Map<String, dynamic>> analyzeSubtitles(BatchRequest request) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/subtitles'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(request.toJson()),
      );

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Failed to analyze subtitles: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error analyzing subtitles: $e');
    }
  }

  // Get courses
  Future<Map<String, dynamic>> getCourses(CoursesRequest request) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/api/courses').replace(
          queryParameters: {
            if (request.corpus != null) 'corpus': request.corpus!,
            if (request.lang != null) 'lang': request.lang!,
            if (request.toLang != null) 'to_lang': request.toLang!,
          },
        ),
      );

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Failed to load courses: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error fetching courses: $e');
    }
  }
}

