import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

/// Progress data model
class ProgressData {
  final int questionsToday;
  final int totalQuestions;
  final int lastQuizScore;
  final double progressPercentage;
  final Map<String, dynamic>? rawData;

  const ProgressData({
    required this.questionsToday,
    required this.totalQuestions,
    required this.lastQuizScore,
    required this.progressPercentage,
    this.rawData,
  });

  factory ProgressData.fromJson(Map<String, dynamic> json) {
    // Extract data from the API response
    // Adjust these fields based on the actual API response structure
    final questionsToday = json['questions_today'] ?? 0;
    final totalQuestions = json['total_questions'] ?? 0;
    final lastQuizScore = json['last_quiz_score'] ?? 0;
    final progressPercentage = json['progress_percentage'] ?? 0.0;

    return ProgressData(
      questionsToday: questionsToday,
      totalQuestions: totalQuestions,
      lastQuizScore: lastQuizScore,
      progressPercentage: progressPercentage.toDouble(),
      rawData: json,
    );
  }

  factory ProgressData.defaultData() {
    return const ProgressData(
      questionsToday: 12,
      totalQuestions: 234,
      lastQuizScore: 3,
      progressPercentage: 45.0,
    );
  }
}

/// Progress state
class ProgressState {
  final ProgressData? data;
  final bool isLoading;
  final String? error;
  final DateTime? lastUpdated;

  const ProgressState({
    this.data,
    this.isLoading = false,
    this.error,
    this.lastUpdated,
  });

  ProgressState copyWith({
    ProgressData? data,
    bool? isLoading,
    String? error,
    DateTime? lastUpdated,
  }) {
    return ProgressState(
      data: data ?? this.data,
      isLoading: isLoading ?? this.isLoading,
      error: error,
      lastUpdated: lastUpdated ?? this.lastUpdated,
    );
  }
}

/// Progress provider using Riverpod
class ProgressNotifier extends StateNotifier<ProgressState> {
  ProgressNotifier() : super(const ProgressState()) {
    // Load initial data
    loadProgress();
  }

  /// Load progress data from the backend
  Future<void> loadProgress() async {
    state = state.copyWith(isLoading: true, error: null);

    try {
      final progressData = await _fetchProgressFromAPI();
      state = state.copyWith(
        data: progressData,
        isLoading: false,
        lastUpdated: DateTime.now(),
      );
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: 'Failed to load progress: $e',
        data: ProgressData.defaultData(), // Fallback to default data
      );
    }
  }

  /// Fetch progress data from the API
  Future<ProgressData> _fetchProgressFromAPI() async {
    const String baseUrl = 'http://localhost:8000';
    const String endpoint = '/api/v1/stats/progress';
    
    final url = Uri.parse('$baseUrl$endpoint');
    
    final requestBody = {
      'user_id': 'ebd27953d70f',
      'lang': 'de', // This should come from settings provider
      'granularity': 'day',
      'customer_id': 'polyglots',
    };

    try {
      final response = await http.post(
        url,
        headers: {
          'accept': 'application/json',
          'Content-Type': 'application/json',
        },
        body: jsonEncode(requestBody),
      );

      if (response.statusCode == 200) {
        final jsonData = jsonDecode(response.body) as Map<String, dynamic>;
        return ProgressData.fromJson(jsonData);
      } else {
        throw Exception('Failed to load progress: ${response.statusCode}');
      }
    } catch (e) {
      print('Error fetching progress: $e');
      // Return default data if API fails
      return ProgressData.defaultData();
    }
  }

  /// Refresh progress data
  Future<void> refresh() async {
    await loadProgress();
  }

  /// Clear error
  void clearError() {
    state = state.copyWith(error: null);
  }

  /// Update progress data manually (for testing or offline mode)
  void updateProgress(ProgressData newData) {
    state = state.copyWith(
      data: newData,
      lastUpdated: DateTime.now(),
    );
  }
}

/// Provider for progress state
final progressProvider = StateNotifierProvider<ProgressNotifier, ProgressState>((ref) {
  return ProgressNotifier();
});

/// Provider for progress data only
final progressDataProvider = Provider<ProgressData?>((ref) {
  final progressState = ref.watch(progressProvider);
  return progressState.data;
});

/// Provider for questions today
final questionsTodayProvider = Provider<int>((ref) {
  final progressData = ref.watch(progressDataProvider);
  return progressData?.questionsToday ?? 12;
});

/// Provider for total questions
final totalQuestionsProvider = Provider<int>((ref) {
  final progressData = ref.watch(progressDataProvider);
  return progressData?.totalQuestions ?? 234;
});

/// Provider for last quiz score
final lastQuizScoreProvider = Provider<int>((ref) {
  final progressData = ref.watch(progressDataProvider);
  return progressData?.lastQuizScore ?? 3;
});

/// Provider for progress percentage
final progressPercentageProvider = Provider<double>((ref) {
  final progressData = ref.watch(progressDataProvider);
  return progressData?.progressPercentage ?? 45.0;
}); 