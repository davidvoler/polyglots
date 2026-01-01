class Language {
  final String code;
  final String name;
  final String nativeName;
  final String flag;
  final bool sound;
  final bool rtl;

  const Language({
    required this.code,
    required this.name,
    required this.nativeName,
    required this.flag,
    required this.sound,
    required this.rtl,
  });

  @override
  String toString() => name;

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is Language &&
          runtimeType == other.runtimeType &&
          code == other.code;

  @override
  int get hashCode => code.hashCode;
}

class LanguagePair {
  final Language sourceLanguage;
  final Language targetLanguage;

  const LanguagePair({
    required this.sourceLanguage,
    required this.targetLanguage,
  });

  String get displayName => '${sourceLanguage.name} → ${targetLanguage.name}';
  String get reverseDisplayName => '${targetLanguage.name} → ${sourceLanguage.name}';

  @override
  String toString() => displayName;

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is LanguagePair &&
          runtimeType == other.runtimeType &&
          sourceLanguage == other.sourceLanguage &&
          targetLanguage == other.targetLanguage;

  @override
  int get hashCode => sourceLanguage.hashCode ^ targetLanguage.hashCode;
}

// Predefined list of supported languages
class SupportedLanguages {
  static const List<Language> all = [
    Language(code: 'ar', name: 'Arabic', nativeName: 'العربية', flag: '🇸🇦', sound: false, rtl: true),
    Language(code: 'cs', name: 'Czech', nativeName: 'Čeština', flag: '🇨🇿', sound: true, rtl: false),
    Language(code: 'de', name: 'German', nativeName: 'Deutsch', flag: '🇩🇪', sound: true, rtl: false),
    Language(code: 'el', name: 'Greek', nativeName: 'Ελληνικά', flag: '🇬🇷', sound: true, rtl: false),
    Language(code: 'en', name: 'English', nativeName: 'English', flag: '🇺🇸', sound: true, rtl: false),
    Language(code: 'es', name: 'Spanish', nativeName: 'Español', flag: '🇪🇸', sound: true, rtl: false),
    Language(code: 'fr', name: 'French', nativeName: 'Français', flag: '🇫🇷', sound: true, rtl: false),
    Language(code: 'he', name: 'Hebrew', nativeName: 'עברית', flag: '🇮🇱', sound: true, rtl: true),
    Language(code: 'hi', name: 'Hindi', nativeName: 'Français', flag: '🇮🇳', sound: true, rtl: false),
    Language(code: 'it', name: 'Italian', nativeName: 'Italiano', flag: '🇮🇹', sound: true, rtl: false),
    Language(code: 'ja', name: 'Japanese', nativeName: '日本語', flag: '🇯🇵', sound: true, rtl: false),
    Language(
      code: 'pt',
      name: 'Portuguese Brazil',
      nativeName: 'Português',
      flag: '🇧🇷',
      sound: true,
      rtl: false,
    ),
    Language(
      code: 'pt-PT',
      name: 'Portuguese Portugal',
      nativeName: 'Português',
      flag: '🇵🇹',
      sound: true,
      rtl: false,
    ),
    Language(code: 'ru', name: 'Russian', nativeName: 'Русский', flag: '🇷🇺', sound: true, rtl: false),
    Language(code: 'zh-Hans', name: 'Chinese', nativeName: '中文', flag: '🇨🇳', sound: false, rtl: false),
  ];

  static Language? findByCode(String code) {
    try {
      return all.firstWhere((lang) => lang.code == code);
    } catch (e) {
      return null;
    }
  }

  static Language get defaultSource => all[4]; // English
  static Language get defaultTarget => all[6]; // French
} 