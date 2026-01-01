import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// Theme state class
class ThemeState {
  final bool isDarkMode;
  final int selectedThemeIndex;

  const ThemeState({
    required this.isDarkMode,
    required this.selectedThemeIndex,
  });

  ThemeState copyWith({
    bool? isDarkMode,
    int? selectedThemeIndex,
  }) {
    return ThemeState(
      isDarkMode: isDarkMode ?? this.isDarkMode,
      selectedThemeIndex: selectedThemeIndex ?? this.selectedThemeIndex,
    );
  }
}

/// Theme provider using Riverpod
class ThemeNotifier extends StateNotifier<ThemeState> {
  static const String _darkModeKey = 'is_dark_mode';
  static const String _themeIndexKey = 'selected_theme_index';

  ThemeNotifier() : super(const ThemeState(isDarkMode: false, selectedThemeIndex: 0)) {
    _loadPreferences();
  }

  /// Load saved preferences
  Future<void> _loadPreferences() async {
    final prefs = await SharedPreferences.getInstance();
    final isDarkMode = prefs.getBool(_darkModeKey) ?? false;
    final selectedThemeIndex = prefs.getInt(_themeIndexKey) ?? 0;
    
    state = state.copyWith(
      isDarkMode: isDarkMode,
      selectedThemeIndex: selectedThemeIndex,
    );
  }

  /// Toggle dark mode
  Future<void> toggleDarkMode() async {
    final prefs = await SharedPreferences.getInstance();
    final newDarkMode = !state.isDarkMode;
    
    await prefs.setBool(_darkModeKey, newDarkMode);
    state = state.copyWith(isDarkMode: newDarkMode);
  }

  /// Change theme
  Future<void> changeTheme(int themeIndex) async {
    final prefs = await SharedPreferences.getInstance();
    
    await prefs.setInt(_themeIndexKey, themeIndex);
    state = state.copyWith(selectedThemeIndex: themeIndex);
  }
}

/// Provider for theme state
final themeProvider = StateNotifierProvider<ThemeNotifier, ThemeState>((ref) {
  return ThemeNotifier();
}); 