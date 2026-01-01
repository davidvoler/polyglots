import 'package:flutter/material.dart';
import '../models/language_model.dart';

class LanguageDropdown extends StatelessWidget {
  final String value;
  final List<Language> items;
  final ValueChanged<String> onChanged;
  final String label;

  const LanguageDropdown({
    super.key,
    required this.value,
    required this.items,
    required this.onChanged,
    required this.label,
  });

  @override
  Widget build(BuildContext context) {
    print('🔍 LanguageDropdown - value: $value, items count: ${items.length}');
    print('🔍 LanguageDropdown - available items: ${items.map((item) => '${item.code}:${item.name}').join(', ')}');
    
    final selectedItem = items.firstWhere(
      (item) => item.code == value,
      orElse: () {
        print('⚠️ LanguageDropdown - value "$value" not found, using fallback');
        return items.isNotEmpty ? items.first : Language(code: 'en', name: 'English', nativeName: 'English', flag: '🇺🇸', sound: true, rtl: false);
      },
    );
    
    print('🔍 LanguageDropdown - selected item: ${selectedItem.code}:${selectedItem.name}');
    
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          label,
          style: TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.w600,
            color: Colors.grey.shade700,
          ),
        ),
        SizedBox(height: 8),
        Container(
          decoration: BoxDecoration(
            border: Border.all(color: Colors.grey.shade300),
            borderRadius: BorderRadius.circular(8),
          ),
          child: DropdownButton<String>(
            value: selectedItem.code,
            isExpanded: true,
            underline: SizedBox(),
            padding: EdgeInsets.symmetric(horizontal: 12),
            items: items.map((Language item) {
              return DropdownMenuItem<String>(
                value: item.code,
                child: Row(
                  children: [
                    Text(item.flag, style: TextStyle(fontSize: 20)),
                    SizedBox(width: 8),
                    Expanded(
                      child: Text(
                        item.name,
                        style: TextStyle(
                          fontSize: 16,
                          color: Colors.grey.shade800,
                        ),
                      ),
                    ),
                  ],
                ),
              );
            }).toList(),
            onChanged: (String? newValue) {
              if (newValue != null) {
                onChanged(newValue);
              }
            },
          ),
        ),
      ],
    );
  }
} 