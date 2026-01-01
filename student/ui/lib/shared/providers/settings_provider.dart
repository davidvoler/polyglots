import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// Settings provider that saves values only to local storage (shared_preferences)
/// 
/// This provider manages the following settings:
/// - lang: Source language (saved as 'lang' in shared_preferences)
/// - toLang: Target language (saved as 'to_lang' in shared_preferences)
/// - showText: Whether to show text (saved as 'show_text' in shared_preferences)
/// - autoPlay: Whether to auto-play audio (saved as 'auto_play' in shared_preferences)
/// - showTranslit: Whether to show transliteration (saved as 'show_transliteration' in shared_preferences)
/// 
/// All settings are automatically persisted to shared_preferences when updated
/// and loaded from shared_preferences when the app starts.

/// Settings state class
class SettingsState {
  final String lang;
  final String toLang;
  final bool showText;
  final bool autoPlay;
  final bool showTranslit;

  const SettingsState({
    required this.lang,
    required this.toLang,
    required this.showText,
    required this.autoPlay,
    required this.showTranslit,
  });

  SettingsState copyWith({
    String? lang,
    String? toLang,
    bool? showText,
    bool? autoPlay,
    bool? showTranslit,
  }) {
    return SettingsState(
      lang: lang ?? this.lang,
      toLang: toLang ?? this.toLang,
      showText: showText ?? this.showText,
      autoPlay: autoPlay ?? this.autoPlay,
      showTranslit: showTranslit ?? this.showTranslit,
    );
  }
}

/// Settings provider using Riverpod
class SettingsNotifier extends StateNotifier<SettingsState> {
  static const String _langKey = 'lang';
  static const String _toLangKey = 'to_lang';
  static const String _showTextKey = 'show_text';
  static const String _autoPlayKey = 'auto_play';
  static const String _showTransliterationKey = 'show_transliteration';
  
  static late SharedPreferences _prefs;
  
  SettingsNotifier() : super(const SettingsState(
    lang: 'spanish',
    toLang: 'arabic',
    showText: false,
    autoPlay: true,
    showTranslit: false,
  )) {
    _initializePrefs();
  }

  /// Initialize shared preferences
  Future<void> _initializePrefs() async {
    _prefs = await SharedPreferences.getInstance();
    await _loadSettings();
  }

  /// Load settings from preferences
  Future<void> _loadSettings() async {
    state = state.copyWith(
      lang: _prefs.getString(_langKey) ?? 'spanish',
      toLang: _prefs.getString(_toLangKey) ?? 'arabic',
      showText: _prefs.getBool(_showTextKey) ?? false,
      autoPlay: _prefs.getBool(_autoPlayKey) ?? true,
      showTranslit: _prefs.getBool(_showTransliterationKey) ?? false,
    );
  }

  /// Update lang setting
  void updateLang(String language) {
    state = state.copyWith(lang: language);
    _prefs.setString(_langKey, language);
  }

  /// Update toLang setting
  void updateToLang(String language) {
    state = state.copyWith(toLang: language);
    _prefs.setString(_toLangKey, language);
  }

  /// Toggle show text setting
  void toggleShowText() {
    final newValue = !state.showText;
    state = state.copyWith(showText: newValue);
    _prefs.setBool(_showTextKey, newValue);
  }

  /// Toggle auto play setting
  void toggleAutoPlay() {
    final newValue = !state.autoPlay;
    state = state.copyWith(autoPlay: newValue);
    _prefs.setBool(_autoPlayKey, newValue);
  }

  /// Toggle show translit setting
  void toggleShowTranslit() {
    final newValue = !state.showTranslit;
    state = state.copyWith(showTranslit: newValue);
    _prefs.setBool(_showTransliterationKey, newValue);
  }

  // Legacy getters for backward compatibility
  String get selectedLanguage => state.lang;
  String get nativeLanguage => state.toLang;
  bool get autoPlaySound => state.autoPlay;
  bool get showTransliteration => state.showTranslit;
  
  // Legacy setters for backward compatibility
  void updateSelectedLanguage(String language) => updateLang(language);
  void updateNativeLanguage(String language) => updateToLang(language);
  void toggleAutoPlaySound() => toggleAutoPlay();
  void toggleShowTransliteration() => toggleShowTranslit();
}

/// Provider for settings state
final settingsProvider = StateNotifierProvider<SettingsNotifier, SettingsState>((ref) {
  return SettingsNotifier();
}); 