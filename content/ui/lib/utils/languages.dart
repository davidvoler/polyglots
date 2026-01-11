/// Language codes and their display names
/// Matches the languages from Python LANG2COUNTY dictionary
class Language {
  final String code;
  final String displayName;
  final String countryCode;

  const Language({
    required this.code,
    required this.displayName,
    required this.countryCode,
  });
}

/// List of supported languages matching Python LANG2COUNTY
final List<Language> supportedLanguages = [
  const Language(code: 'ar', displayName: 'Arabic', countryCode: 'ar-'),
  const Language(code: 'cs', displayName: 'Czech', countryCode: 'cs-CZ'),
  const Language(code: 'de', displayName: 'German', countryCode: 'de-DE'),
  const Language(code: 'el', displayName: 'Greek', countryCode: 'el-GR'),
  const Language(code: 'en', displayName: 'English', countryCode: 'en-US'),
  const Language(code: 'es', displayName: 'Spanish', countryCode: 'es-ES'),
  const Language(code: 'fr', displayName: 'French', countryCode: 'fr-FR'),
  const Language(code: 'he', displayName: 'Hebrew', countryCode: 'he-IL'),
  const Language(code: 'hi', displayName: 'Hindi', countryCode: 'hi-IN'),
  const Language(code: 'it', displayName: 'Italian', countryCode: 'it-IT'),
  const Language(code: 'ja', displayName: 'Japanese', countryCode: 'ja-JP'),
  const Language(code: 'pt', displayName: 'Portuguese', countryCode: 'pt-PT'),
  const Language(code: 'pt-BR', displayName: 'Portuguese (Brazil)', countryCode: 'pt-BR'),
  const Language(code: 'ru', displayName: 'Russian', countryCode: 'ru-RU'),
  const Language(code: 'zh-Hans', displayName: 'Chinese (Simplified)', countryCode: 'zh-CN'),
];

/// Get language by code
Language? getLanguageByCode(String code) {
  try {
    return supportedLanguages.firstWhere(
      (lang) => lang.code == code,
    );
  } catch (e) {
    return null;
  }
}

/// Get language code list
List<String> getLanguageCodes() {
  return supportedLanguages.map((lang) => lang.code).toList();
}

/// Get display name for a language code
String getLanguageDisplayName(String code) {
  final lang = getLanguageByCode(code);
  return lang?.displayName ?? code;
}
