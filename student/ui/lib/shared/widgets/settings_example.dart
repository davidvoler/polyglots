import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../providers/settings_provider.dart';

/// Example widget showing how to use the settings provider
/// This demonstrates how settings are automatically saved to shared_preferences
class SettingsExample extends ConsumerWidget {
  const SettingsExample({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final settings = ref.watch(settingsProvider);
    
    return Scaffold(
      appBar: AppBar(
        title: const Text('Settings Example'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Current Settings (saved in shared_preferences):',
              style: Theme.of(context).textTheme.headlineSmall,
            ),
            const SizedBox(height: 16),
            
            // Display current settings
            _buildSettingCard(
              context,
              'Source Language (lang)',
              settings.lang,
              () => ref.read(settingsProvider.notifier).updateLang('french'),
            ),
            
            _buildSettingCard(
              context,
              'Target Language (toLang)',
              settings.toLang,
              () => ref.read(settingsProvider.notifier).updateToLang('german'),
            ),
            
            _buildToggleCard(
              context,
              'Show Text (showText)',
              settings.showText,
              () => ref.read(settingsProvider.notifier).toggleShowText(),
            ),
            
            _buildToggleCard(
              context,
              'Auto Play (autoPlay)',
              settings.autoPlay,
              () => ref.read(settingsProvider.notifier).toggleAutoPlay(),
            ),
            
            _buildToggleCard(
              context,
              'Show Transliteration (showTranslit)',
              settings.showTranslit,
              () => ref.read(settingsProvider.notifier).toggleShowTranslit(),
            ),
            
            const SizedBox(height: 24),
            
            const SizedBox(height: 16),
            
            // Instructions
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.blue.shade50,
                borderRadius: BorderRadius.circular(8),
              ),
              child: const Text(
                '💡 All settings are automatically saved to shared_preferences!\n\n'
                '• Tap the language cards to change languages\n'
                '• Toggle the switches to change boolean settings\n'
                '• Settings persist between app restarts\n'
                '• Settings are saved only to local storage',
                style: TextStyle(fontSize: 14),
              ),
            ),
          ],
        ),
      ),
    );
  }
  
  Widget _buildSettingCard(BuildContext context, String title, String value, VoidCallback onTap) {
    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: ListTile(
        title: Text(title),
        subtitle: Text('Current: $value'),
        trailing: const Icon(Icons.edit),
        onTap: onTap,
      ),
    );
  }
  
  Widget _buildToggleCard(BuildContext context, String title, bool value, VoidCallback onTap) {
    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: ListTile(
        title: Text(title),
        subtitle: Text('Current: ${value ? "ON" : "OFF"}'),
        trailing: Switch(
          value: value,
          onChanged: (_) => onTap(),
        ),
        onTap: onTap,
      ),
    );
  }
} 