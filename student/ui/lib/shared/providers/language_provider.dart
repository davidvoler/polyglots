import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../models/language_model.dart';

// Language state class
class LanguageState {
  final List<Language> languages;
  final bool isLoading;
  final String? error;
  final String baseUrl;

  const LanguageState({
    this.languages = const [],
    this.isLoading = false,
    this.error,
    this.baseUrl = 'http://localhost:8000',
  });

  LanguageState copyWith({
    List<Language>? languages,
    bool? isLoading,
    String? error,
    String? baseUrl,
  }) {
    return LanguageState(
      languages: languages ?? this.languages,
      isLoading: isLoading ?? this.isLoading,
      error: error ?? this.error,
      baseUrl: baseUrl ?? this.baseUrl,
    );
  }

  bool get hasLanguages => languages.isNotEmpty;

  Language? findByCode(String code) {
    try {
      return languages.firstWhere((lang) => lang.code == code);
    } catch (e) {
      return null;
    }
  }

  Language get defaultSource {
    return findByCode('en') ?? SupportedLanguages.defaultSource;
  }

  Language get defaultTarget {
    return findByCode('fr') ?? SupportedLanguages.defaultTarget;
  }

  List<Language> get languagesWithSound {
    return languages.where((lang) => lang.sound).toList();
  }

  List<Language> get rtlLanguages {
    return languages.where((lang) => lang.rtl).toList();
  }
}

// Language provider
class LanguageNotifier extends StateNotifier<LanguageState> {
  LanguageNotifier() : super(const LanguageState());

  // Set base URL for API calls
  void setBaseUrl(String baseUrl) {
    state = state.copyWith(baseUrl: baseUrl);
  }

  // Load languages from server
  Future<void> loadLanguages() async {
    if (state.isLoading) return;

    state = state.copyWith(isLoading: true, error: null);

    try {
      final response = await http.get(
        Uri.parse('${state.baseUrl}/api/v1/language/languages'),
        headers: {
          'accept': 'application/json',
        },
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        final languages = data.map((json) => _languageFromJson(json)).toList();
        state = state.copyWith(
          languages: languages,
          isLoading: false,
          error: null,
        );
      } else {
        // Fallback to hardcoded languages if server is not available
        state = state.copyWith(
          languages: SupportedLanguages.all,
          isLoading: false,
          error: 'Failed to load languages: ${response.statusCode}',
        );
      }
    } catch (e) {
      // Fallback to hardcoded languages if server is not available
      state = state.copyWith(
        languages: SupportedLanguages.all,
        isLoading: false,
        error: 'Error loading languages: $e',
      );
    }
  }

  // Convert JSON to Language object
  Language _languageFromJson(Map<String, dynamic> json) {
    return Language(
      code: json['code2'] ?? '',
      name: json['name'] ?? '',
      nativeName: json['native_name'] ?? json['name'] ?? '',
      flag: json['icon'] ?? '🏳️',
      sound: json['sound'] ?? false,
      rtl: json['rtl'] ?? false,
    );
  }

  // Refresh languages
  Future<void> refresh() async {
    await loadLanguages();
  }

  // Clear error
  void clearError() {
    state = state.copyWith(error: null);
  }
}

// Provider instances
final languageProvider = StateNotifierProvider<LanguageNotifier, LanguageState>((ref) {
  return LanguageNotifier();
});

// Convenience providers
final languagesProvider = Provider<List<Language>>((ref) {
  return ref.watch(languageProvider).languages;
});

final languagesWithSoundProvider = Provider<List<Language>>((ref) {
  return ref.watch(languageProvider).languagesWithSound;
});

final rtlLanguagesProvider = Provider<List<Language>>((ref) {
  return ref.watch(languageProvider).rtlLanguages;
});

final defaultSourceLanguageProvider = Provider<Language>((ref) {
  return ref.watch(languageProvider).defaultSource;
});

final defaultTargetLanguageProvider = Provider<Language>((ref) {
  return ref.watch(languageProvider).defaultTarget;
}); 