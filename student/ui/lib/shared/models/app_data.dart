import 'language_model.dart';
import 'quiz_model.dart';

class AppData {
  // Native languages (languages the user speaks)
  static final List<Language> nativeLanguages = [
    Language(code: 'ar', name: 'Arabic', nativeName: 'العربية', flag: '🇸🇦', sound: false, rtl: true),
    Language(code: 'cs', name: 'Czech', nativeName: 'Čeština', flag: '🇨🇿', sound: true, rtl: false),
    Language(code: 'de', name: 'German', nativeName: 'Deutsch', flag: '🇩🇪', sound: true, rtl: false),
    Language(code: 'el', name: 'Greek', nativeName: 'Ελληνικά', flag: '🇬🇷', sound: true, rtl: false),
    Language(code: 'en', name: 'English', nativeName: 'English', flag: '🇺🇸', sound: true, rtl: false),
    Language(code: 'es', name: 'Spanish', nativeName: 'Español', flag: '🇪🇸', sound: true, rtl: false),
    Language(code: 'fr', name: 'French', nativeName: 'Français', flag: '🇫🇷', sound: true, rtl: false),
    Language(code: 'he', name: 'Hebrew', nativeName: 'עברית', flag: '🇮🇱', sound: true, rtl: true),
    Language(code: 'hi', name: 'Hindi', nativeName: 'Français', flag: '🇮🇳', sound: false, rtl: false),
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

  // Target languages (languages the user wants to learn)
  static final List<Language> targetLanguages = [
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

  // Fallback quiz data for when backend is not available
  static final List<QuizSentence> quizData = [
    QuizSentence(
      sentence: 'Me gusta leer libros en la biblioteca',
      options: [
        QuizOption(sentence: 'أحب قراءة الكتب في المكتبة', correct: true),
        QuizOption(sentence: 'أحتاج إلى شراء كتب من المتجر', correct: false),
        QuizOption(sentence: 'أريد أن أكتب كتباً للأطفال', correct: false),
        QuizOption(sentence: 'أفضل الاستماع إلى الكتب الصوتية', correct: false),
      ],
      words: ['me', 'gusta', 'leer', 'libros'],
      id: 'demo_1',
      translit: 'Me goos-tah le-er lee-brohs en lah bee-blee-oh-te-kah',
      sound: '/demo/me_gusta_leer.mp3',
    ),
    QuizSentence(
      sentence: '¿Cómo estás hoy?',
      options: [
        QuizOption(sentence: 'كيف حالك اليوم؟', correct: true),
        QuizOption(sentence: 'أين تذهب اليوم؟', correct: false),
        QuizOption(sentence: 'ماذا تأكل اليوم؟', correct: false),
        QuizOption(sentence: 'متى تعود إلى البيت؟', correct: false),
      ],
      words: ['cómo', 'estás', 'hoy'],
      id: 'demo_2',
      translit: 'KOH-moh ehs-TAHS oy',
      sound: '/demo/como_estas.mp3',
    ),
    QuizSentence(
      sentence: 'El café está muy caliente',
      options: [
        QuizOption(sentence: 'القهوة ساخنة جداً', correct: true),
        QuizOption(sentence: 'القهوة باردة جداً', correct: false),
        QuizOption(sentence: 'القهوة لذيذة جداً', correct: false),
        QuizOption(sentence: 'القهوة مرة جداً', correct: false),
      ],
      words: ['café', 'está', 'muy', 'caliente'],
      id: 'demo_3',
      translit: 'El kah-FEH ehs-TAH mwee kah-lee-EN-teh',
      sound: '/demo/cafe_caliente.mp3',
    ),
  ];
}
