import 'package:flutter/material.dart';
import '../utils/languages.dart';

/// A reusable language dropdown widget
class LanguageDropdown extends StatelessWidget {
  final String? value;
  final ValueChanged<String?>? onChanged;
  final String? labelText;
  final String? hintText;
  final bool isRequired;
  final String? Function(String?)? validator;

  const LanguageDropdown({
    super.key,
    this.value,
    this.onChanged,
    this.labelText,
    this.hintText,
    this.isRequired = false,
    this.validator,
  });

  @override
  Widget build(BuildContext context) {
    return DropdownButtonFormField<String>(
      value: value,
      decoration: InputDecoration(
        labelText: labelText ?? 'Language',
        hintText: hintText ?? 'Select a language',
        border: const OutlineInputBorder(),
        filled: true,
        fillColor: Colors.white,
      ),
      items: supportedLanguages.map((Language language) {
        return DropdownMenuItem<String>(
          value: language.code,
          child: Text('${language.displayName} (${language.code})'),
        );
      }).toList(),
      onChanged: onChanged,
      validator: validator ??
          (isRequired
              ? (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please select a language';
                  }
                  return null;
                }
              : null),
    );
  }
}
