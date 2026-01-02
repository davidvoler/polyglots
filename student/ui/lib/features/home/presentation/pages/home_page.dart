import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../shared/models/app_data.dart';
import '../../../../shared/models/language_model.dart';
import '../../../../shared/providers/settings_provider.dart';
import '../../../../shared/providers/progress_provider.dart';
import '../../../../shared/widgets/language_dropdown.dart';
import '../../../../shared/widgets/settings_toggle.dart';
import '../../../quiz/presentation/pages/quiz_page.dart';
import '../../../quiz/presentation/pages/question_types_demo_page.dart';

class HomePage extends ConsumerWidget {
  const HomePage({super.key});

  Language? _getCurrentTargetLanguage(String selectedLanguage) {
    try {
      return AppData.targetLanguages.firstWhere((lang) => lang.code == selectedLanguage);
    } catch (e) {
      // Return first available language if the selected language is not found
      return AppData.targetLanguages.isNotEmpty ? AppData.targetLanguages.first : null;
    }
  }

  Language? _getCurrentNativeLanguage(String nativeLanguage) {
    try {
      return AppData.nativeLanguages.firstWhere((lang) => lang.code == nativeLanguage);
    } catch (e) {
      // Return first available language if the native language is not found
      return AppData.nativeLanguages.isNotEmpty ? AppData.nativeLanguages.first : null;
    }
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final settings = ref.watch(settingsProvider);
    final questionsToday = ref.watch(questionsTodayProvider);
    final progressPercentage = ref.watch(progressPercentageProvider);
    
    return Container(
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [Colors.blue.shade50, Colors.indigo.shade100],
        ),
      ),
      child: SafeArea(
        child: SingleChildScrollView(
          padding: EdgeInsets.all(24.0),
          child: Column(
            children: [
              // Header
              _buildHeader(),
              SizedBox(height: 32),
              
              // Main Language Card
              _buildMainLanguageCard(context, settings, progressPercentage),
              SizedBox(height: 24),
              
              // Questions Today Card
              _buildQuestionsTodayCard(questionsToday),
              SizedBox(height: 24),
              
              // Learning Options
              _buildLearningOptions(context, settings, ref),
              SizedBox(height: 24), // Bottom padding for scroll

              // Demo question types
              SizedBox(
                width: double.infinity,
                child: OutlinedButton.icon(
                  icon: Icon(Icons.play_circle_fill),
                  label: Text('See question type demos'),
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => const QuestionTypesDemoPage(),
                      ),
                    );
                  },
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildHeader() {
    return Column(
      children: [
        Text(
          'Listen & Learn',
          style: TextStyle(
            fontSize: 32,
            fontWeight: FontWeight.bold,
            color: Colors.grey.shade800,
          ),
        ),
        SizedBox(height: 8),
        Text(
          'Improve language through understanding',
          style: TextStyle(
            fontSize: 16,
            color: Colors.grey.shade600,
          ),
        ),
      ],
    );
  }

  Widget _buildMainLanguageCard(BuildContext context, SettingsState settings, double progressPercentage) {
    final targetLang = _getCurrentTargetLanguage(settings.lang);
    final nativeLang = _getCurrentNativeLanguage(settings.toLang);
    
    // Show loading or error state if languages are not available
    if (targetLang == null || nativeLang == null) {
      return Container(
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(16),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.1),
              blurRadius: 10,
              offset: Offset(0, 4),
            ),
          ],
        ),
        padding: EdgeInsets.all(24),
        child: Column(
          children: [
            Icon(
              Icons.language,
              size: 48,
              color: Colors.grey.shade400,
            ),
            SizedBox(height: 16),
            Text(
              'Loading language settings...',
              style: TextStyle(
                fontSize: 16,
                color: Colors.grey.shade600,
              ),
            ),
          ],
        ),
      );
    }
    
    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.1),
            blurRadius: 10,
            offset: Offset(0, 4),
          ),
        ],
      ),
      padding: EdgeInsets.all(24),
      child: Column(
        children: [
          // Language Display
          Row(
            children: [
              Row(
                children: [
                  Text(
                    targetLang.flag,
                    style: TextStyle(fontSize: 32),
                  ),
                  SizedBox(width: 12),
                  Text(
                    '→',
                    style: TextStyle(fontSize: 24, color: Colors.grey.shade400),
                  ),
                  SizedBox(width: 12),
                  Text(
                    nativeLang.flag,
                    style: TextStyle(fontSize: 24),
                  ),
                ],
              ),
              SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      '${targetLang.name} → ${nativeLang.name}',
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.w600,
                        color: Colors.grey.shade800,
                      ),
                    ),
                    Text(
                      '${(progressPercentage * 100).round()}% progress',
                      style: TextStyle(
                        fontSize: 14,
                        color: Colors.grey.shade500,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
          SizedBox(height: 16),
          
          // Progress Bar
          Column(
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    'Progress',
                    style: TextStyle(
                      fontSize: 14,
                      color: Colors.grey.shade600,
                    ),
                  ),
                  Text(
                    '45%',
                    style: TextStyle(
                      fontSize: 14,
                      color: Colors.grey.shade600,
                    ),
                  ),
                ],
              ),
              SizedBox(height: 8),
              LinearProgressIndicator(
                value: progressPercentage,
                backgroundColor: Colors.grey.shade200,
                valueColor: AlwaysStoppedAnimation<Color>(Colors.blue.shade600),
                minHeight: 8,
              ),
            ],
          ),
          SizedBox(height: 24),
          
          // Start Learning Button
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => QuizPage(
                      selectedLanguage: settings.lang,
                      nativeLanguage: settings.toLang,
                      showText: settings.showText,
                      autoPlaySound: settings.autoPlay,
                      showTransliteration: settings.showTranslit,
                    ),
                  ),
                );
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.blue.shade600,
                foregroundColor: Colors.white,
                padding: EdgeInsets.symmetric(vertical: 16),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
              child: Text(
                'Start Learning',
                style: TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.w600,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildQuestionsTodayCard(int questionsToday) {
    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 8,
            offset: Offset(0, 2),
          ),
        ],
      ),
      padding: EdgeInsets.all(16),
      child: Column(
        children: [
          Text(
            '$questionsToday',
            style: TextStyle(
              fontSize: 32,
              fontWeight: FontWeight.bold,
              color: Colors.blue.shade600,
            ),
          ),
          Text(
            'Questions Today',
            style: TextStyle(
              fontSize: 14,
              color: Colors.grey.shade600,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildLearningOptions(BuildContext context, SettingsState settings, WidgetRef ref) {
    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.1),
            blurRadius: 10,
            offset: Offset(0, 4),
          ),
        ],
      ),
      padding: EdgeInsets.all(24),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Learning Options',
            style: TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.w600,
              color: Colors.grey.shade800,
            ),
          ),
          SizedBox(height: 16),
          
          // Language Dropdowns
          _buildLanguageDropdowns(settings, ref),
          
          Divider(height: 32),
          
          // Settings Toggles
          _buildSettingsToggles(settings, ref),
        ],
      ),
    );
  }

  List<Language> _getAvailableTargetLanguages(String currentToLang) {
    // Remove the restriction that prevents same language selection
    // Allow users to select the same language for both native and target
    return AppData.targetLanguages;
  }

  Widget _buildLanguageDropdowns(SettingsState settings, WidgetRef ref) {
    return Column(
      children: [
        // Target Language Dropdown
        LanguageDropdown(
          label: 'Target Language',
          value: settings.lang,
          items: _getAvailableTargetLanguages(settings.toLang),
          onChanged: (value) {
            ref.read(settingsProvider.notifier).updateLang(value);
          },
        ),
        SizedBox(height: 16),
        
        // Native Language Dropdown
        LanguageDropdown(
          label: 'Your Native Language',
          value: settings.toLang,
          items: AppData.nativeLanguages,
          onChanged: (value) {
            ref.read(settingsProvider.notifier).updateToLang(value);
          },
        ),
      ],
    );
  }

  Widget _buildSettingsToggles(SettingsState settings, WidgetRef ref) {
    return Column(
      children: [
        SettingsToggle(
          icon: Icons.visibility,
          title: 'Show Text',
          subtitle: 'Display written text with audio',
          value: settings.showText,
          onChanged: (value) {
            ref.read(settingsProvider.notifier).toggleShowText();
          },
          color: Colors.blue,
        ),
        SizedBox(height: 16),
        SettingsToggle(
          icon: Icons.volume_up,
          title: 'Auto Play',
          subtitle: 'Play audio automatically',
          value: settings.autoPlay,
          onChanged: (value) {
            ref.read(settingsProvider.notifier).toggleAutoPlay();
          },
          color: Colors.green,
        ),
        SizedBox(height: 16),
        SettingsToggle(
          icon: Icons.text_fields,
          title: 'Transliteration',
          subtitle: 'Show pronunciation guide',
          value: settings.showTranslit,
          onChanged: (value) {
            ref.read(settingsProvider.notifier).toggleShowTranslit();
          },
          color: Colors.purple,
        ),
      ],
    );
  }
} 