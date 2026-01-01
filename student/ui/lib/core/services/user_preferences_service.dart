import 'package:shared_preferences/shared_preferences.dart';
import '../../shared/models/language_model.dart';

class UserPreferencesService {
  static const String _userIdKey = 'user_id';
  static const String _langKey = 'lang';
  static const String _toLangKey = 'to_lang';
  static const String _corpusKey = 'corpus';
  static const String _practiceIdKey = 'practice_id';
  static const String _practiceTypeKey = 'practice_type';
  static const String _lastModeKey = 'last_mode';
  static const String _showTextKey = 'show_text';
  static const String _autoPlayKey = 'auto_play';
  static const String _showTransliterationKey = 'show_transliteration';
  static const String _reverseModeKey = 'reverse_mode';
  static const String _previewHeaderKey = 'preview_header';
  static const String _levelKey = 'level';
  static const String _completedKey = 'completed';
  static const String _remainingKey = 'remaining';
  static const String _accuracyKey = 'accuracy';
  static const String _timesKey = 'times';
  static const String _minutesKey = 'minutes';
  
  static late SharedPreferences _prefs;
  
  static Future<void> initialize() async {
    _prefs = await SharedPreferences.getInstance();
  }
  
  // User settings
  static String get userId => _prefs.getString(_userIdKey) ?? 'ebd27953d70f';
  static set userId(String value) => _prefs.setString(_userIdKey, value);
  
  static String get lang => _prefs.getString(_langKey) ?? 'en';
  static set lang(String value) => _prefs.setString(_langKey, value);
  
  static String get toLang => _prefs.getString(_toLangKey) ?? 'fr';
  static set toLang(String value) => _prefs.setString(_toLangKey, value);
  
  // Legacy properties for backward compatibility
  static String get selectedLanguage => toLang;
  static set selectedLanguage(String value) => toLang = value;
  
  static String get nativeLanguage => lang;
  static set nativeLanguage(String value) => lang = value;
  
  static bool get autoPlaySound => autoPlay;
  static set autoPlaySound(bool value) => autoPlay = value;
  
  // Language objects
  static Language get sourceLanguage => 
      SupportedLanguages.findByCode(lang) ?? SupportedLanguages.defaultSource;
  static set sourceLanguage(Language language) => lang = language.code;
  
  static Language get targetLanguage => 
      SupportedLanguages.findByCode(toLang) ?? SupportedLanguages.defaultTarget;
  static set targetLanguage(Language language) => toLang = language.code;
  
  static LanguagePair get languagePair => 
      LanguagePair(sourceLanguage: sourceLanguage, targetLanguage: targetLanguage);
  
  static String get corpus => _prefs.getString(_corpusKey) ?? 'common';
  static set corpus(String value) => _prefs.setString(_corpusKey, value);
  
  // Quiz state
  static String get practiceId => _prefs.getString(_practiceIdKey) ?? '6';
  static set practiceId(String value) => _prefs.setString(_practiceIdKey, value);
  
  static String get practiceType => _prefs.getString(_practiceTypeKey) ?? 'step';
  static set practiceType(String value) => _prefs.setString(_practiceTypeKey, value);
  
  static String get lastMode => _prefs.getString(_lastModeKey) ?? 'step';
  static set lastMode(String value) => _prefs.setString(_lastModeKey, value);
  
  // Quiz options
  static bool get showText => _prefs.getBool(_showTextKey) ?? true;
  static set showText(bool value) => _prefs.setBool(_showTextKey, value);
  
  static bool get autoPlay => _prefs.getBool(_autoPlayKey) ?? false;
  static set autoPlay(bool value) => _prefs.setBool(_autoPlayKey, value);
  
  static bool get showTransliteration => _prefs.getBool(_showTransliterationKey) ?? true;
  static set showTransliteration(bool value) => _prefs.setBool(_showTransliterationKey, value);
  
  static bool get reverseMode => _prefs.getBool(_reverseModeKey) ?? false;
  static set reverseMode(bool value) => _prefs.setBool(_reverseModeKey, value);
  
  // Practice state
  static String get previewHeader => _prefs.getString(_previewHeaderKey) ?? '';
  static set previewHeader(String value) => _prefs.setString(_previewHeaderKey, value);
  
  // User stats
  static double get level => _prefs.getDouble(_levelKey) ?? 6.0;
  static set level(double value) => _prefs.setDouble(_levelKey, value);
  
  static int get completed => _prefs.getInt(_completedKey) ?? 0;
  static set completed(int value) => _prefs.setInt(_completedKey, value);
  
  static int get remaining => _prefs.getInt(_remainingKey) ?? 0;
  static set remaining(int value) => _prefs.setInt(_remainingKey, value);
  
  static int get accuracy => _prefs.getInt(_accuracyKey) ?? 0;
  static set accuracy(int value) => _prefs.setInt(_accuracyKey, value);
  
  static int get times => _prefs.getInt(_timesKey) ?? 0;
  static set times(int value) => _prefs.setInt(_timesKey, value);
  
  static int get minutes => _prefs.getInt(_minutesKey) ?? 0;
  static set minutes(int value) => _prefs.setInt(_minutesKey, value);
  
  // Legacy properties for backward compatibility
  static int get questionsToday => _prefs.getInt('questions_today') ?? 12;
  static set questionsToday(int value) => _prefs.setInt('questions_today', value);
  
  static int get totalQuestions => _prefs.getInt('total_questions') ?? 234;
  static set totalQuestions(int value) => _prefs.setInt('total_questions', value);
  
  static int get lastQuizScore => _prefs.getInt('last_quiz_score') ?? 3;
  static set lastQuizScore(int value) => _prefs.setInt('last_quiz_score', value);
  
  // Helper methods
  static String getLanguagePair() {
    if (lang.isNotEmpty && toLang.isNotEmpty) {
      return '$lang → $toLang';
    }
    return 'en → fr';
  }
  
  static String getReverseLanguagePair() {
    if (lang.isNotEmpty && toLang.isNotEmpty) {
      return '$toLang → $lang';
    }
    return 'fr → en';
  }
  
  static void clearQuizState() {
    _prefs.remove(_practiceIdKey);
    _prefs.remove(_practiceTypeKey);
    _prefs.remove(_lastModeKey);
  }
  
  // Legacy methods for backward compatibility
  static void incrementQuestionsToday() {
    questionsToday = questionsToday + 1;
  }
  
  static void resetDailyQuestions() {
    questionsToday = 0;
  }
  
  static void clearAll() {
    _prefs.clear();
  }
} 