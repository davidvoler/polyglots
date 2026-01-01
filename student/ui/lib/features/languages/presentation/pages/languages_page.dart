import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../shared/models/language_model.dart';
import '../../../../shared/providers/language_provider.dart';

class LanguagesPage extends ConsumerStatefulWidget {
  final String selectedLanguage;
  final String nativeLanguage;
  final Function(String) onLanguageChanged;

  const LanguagesPage({
    Key? key,
    required this.selectedLanguage,
    required this.nativeLanguage,
    required this.onLanguageChanged,
  }) : super(key: key);

  @override
  ConsumerState<LanguagesPage> createState() => _LanguagesPageState();
}

class _LanguagesPageState extends ConsumerState<LanguagesPage> {
  late String selectedLanguage;
  late String nativeLanguage;

  @override
  void initState() {
    super.initState();
    selectedLanguage = widget.selectedLanguage;
    nativeLanguage = widget.nativeLanguage;
  }

  @override
  Widget build(BuildContext context) {
    final languageState = ref.watch(languageProvider);
    
    return Container(
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [Colors.purple.shade50, Colors.green.shade100],
        ),
      ),
      child: SafeArea(
        child: Column(
          children: [
            // Fixed header
            Padding(
              padding: EdgeInsets.all(24.0),
              child: Text(
                'Language Settings',
                style: TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                  color: Colors.grey.shade800,
                ),
              ),
            ),
            
            // Loading indicator
            if (languageState.isLoading)
              Padding(
                padding: EdgeInsets.all(16.0),
                child: CircularProgressIndicator(),
              ),
            
            // Error message
            if (languageState.error != null)
              Padding(
                padding: EdgeInsets.all(16.0),
                child: Container(
                  padding: EdgeInsets.all(12.0),
                  decoration: BoxDecoration(
                    color: Colors.red.shade50,
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(color: Colors.red.shade200),
                  ),
                  child: Row(
                    children: [
                      Icon(Icons.error_outline, color: Colors.red.shade600),
                      SizedBox(width: 8),
                      Expanded(
                        child: Text(
                          languageState.error!,
                          style: TextStyle(color: Colors.red.shade700),
                        ),
                      ),
                      IconButton(
                        icon: Icon(Icons.refresh, color: Colors.red.shade600),
                        onPressed: () {
                          ref.read(languageProvider.notifier).refresh();
                        },
                      ),
                    ],
                  ),
                ),
              ),
            
            // Scrollable content
            Expanded(
              child: languageState.hasLanguages
                  ? SingleChildScrollView(
                      padding: EdgeInsets.symmetric(horizontal: 24.0),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          // Native Language Section
                          _buildLanguageSection(
                            title: 'Your Native Language',
                            languages: languageState.languages,
                            selectedId: nativeLanguage,
                            onSelect: (id) {
                              setState(() {
                                nativeLanguage = id;
                              });
                              widget.onLanguageChanged(id);
                            },
                            showProgress: false,
                          ),
                          SizedBox(height: 24),
                          
                          // Target Language Section
                          _buildLanguageSection(
                            title: 'Choose Target Language',
                            languages: languageState.languages
                                .where((lang) => lang.code != nativeLanguage)
                                .toList(),
                            selectedId: selectedLanguage,
                            onSelect: (id) {
                              setState(() {
                                selectedLanguage = id;
                              });
                              widget.onLanguageChanged(id);
                            },
                            showProgress: true,
                          ),
                          SizedBox(height: 24), // Bottom padding
                        ],
                      ),
                    )
                  : Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(Icons.language, size: 64, color: Colors.grey.shade400),
                          SizedBox(height: 16),
                          Text(
                            'No languages available',
                            style: TextStyle(
                              fontSize: 18,
                              color: Colors.grey.shade600,
                            ),
                          ),
                          SizedBox(height: 8),
                          ElevatedButton(
                            onPressed: () {
                              ref.read(languageProvider.notifier).refresh();
                            },
                            child: Text('Retry'),
                          ),
                        ],
                      ),
                    ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildLanguageSection({
    required String title,
    required List<Language> languages,
    required String selectedId,
    required Function(String) onSelect,
    required bool showProgress,
  }) {
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
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(
            title,
            style: TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.w600,
              color: Colors.grey.shade800,
            ),
          ),
          SizedBox(height: 12),
          if (!showProgress)
            // Grid layout for native languages - constrain height
            Container(
              constraints: BoxConstraints(
                maxHeight: 200, // Limit the height
              ),
              child: GridView.builder(
                shrinkWrap: true,
                physics: NeverScrollableScrollPhysics(),
                gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 2,
                  childAspectRatio: 3,
                  crossAxisSpacing: 8,
                  mainAxisSpacing: 8,
                ),
                itemCount: languages.length,
                itemBuilder: (context, index) {
                  final lang = languages[index];
                  final isSelected = lang.code == selectedId;
                  
                  return GestureDetector(
                    onTap: () => onSelect(lang.code),
                    child: Container(
                      decoration: BoxDecoration(
                        color: isSelected ? Colors.purple.shade100 : Colors.grey.shade50,
                        border: Border.all(
                          color: isSelected ? Colors.purple.shade500 : Colors.transparent,
                          width: 2,
                        ),
                        borderRadius: BorderRadius.circular(8),
                      ),
                      padding: EdgeInsets.all(8),
                      child: Row(
                        children: [
                          Text(
                            lang.flag,
                            style: TextStyle(fontSize: 18),
                          ),
                          SizedBox(width: 8),
                          Expanded(
                            child: Text(
                              lang.name,
                              style: TextStyle(
                                fontSize: 12,
                                fontWeight: FontWeight.w500,
                              ),
                              overflow: TextOverflow.ellipsis,
                            ),
                          ),
                        ],
                      ),
                    ),
                  );
                },
              ),
            )
          else
            // List layout for target languages - constrain height and make scrollable
            Container(
              constraints: BoxConstraints(
                maxHeight: 300, // Limit the height
              ),
              child: ListView.builder(
                shrinkWrap: true,
                itemCount: languages.length,
                itemBuilder: (context, index) {
                  final lang = languages[index];
                  final isSelected = lang.code == selectedId;
                  
                  return Container(
                    margin: EdgeInsets.only(bottom: 8),
                    child: GestureDetector(
                      onTap: () => onSelect(lang.code),
                      child: Container(
                        decoration: BoxDecoration(
                          color: isSelected ? Colors.purple.shade50 : Colors.grey.shade50,
                          border: Border.all(
                            color: isSelected ? Colors.purple.shade500 : Colors.transparent,
                            width: 2,
                          ),
                          borderRadius: BorderRadius.circular(12),
                        ),
                        padding: EdgeInsets.all(16),
                        child: Row(
                          children: [
                            Text(
                              lang.flag,
                              style: TextStyle(fontSize: 24),
                            ),
                            SizedBox(width: 12),
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    lang.name,
                                    style: TextStyle(
                                      fontWeight: FontWeight.w600,
                                      color: Colors.grey.shade800,
                                    ),
                                  ),
                                  Text(
                                    '234 questions',
                                    style: TextStyle(
                                      fontSize: 14,
                                      color: Colors.grey.shade500,
                                    ),
                                  ),
                                ],
                              ),
                            ),
                            Column(
                              crossAxisAlignment: CrossAxisAlignment.end,
                              children: [
                                Text(
                                  '45%',
                                  style: TextStyle(
                                    fontSize: 14,
                                    fontWeight: FontWeight.w500,
                                    color: Colors.grey.shade700,
                                  ),
                                ),
                                SizedBox(height: 4),
                                Container(
                                  width: 48,
                                  height: 4,
                                  decoration: BoxDecoration(
                                    color: Colors.grey.shade200,
                                    borderRadius: BorderRadius.circular(2),
                                  ),
                                  child: FractionallySizedBox(
                                    alignment: Alignment.centerLeft,
                                    widthFactor: 0.45,
                                    child: Container(
                                      decoration: BoxDecoration(
                                        color: Colors.purple.shade600,
                                        borderRadius: BorderRadius.circular(2),
                                      ),
                                    ),
                                  ),
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),
                    ),
                  );
                },
              ),
            ),
        ],
      ),
    );
  }
} 