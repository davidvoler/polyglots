class Sentence {
  final String lang;
  final int id;
  final String text;
  final String? source;
  final String? toLang;
  final String? toText;

  Sentence({
    required this.lang,
    required this.id,
    required this.text,
    this.source,
    this.toLang,
    this.toText,
  });

  factory Sentence.fromJson(Map<String, dynamic> json) {
    return Sentence(
      lang: json['lang'] as String,
      id: json['id'] as int,
      text: json['text'] as String,
      source: json['source'] as String?,
      toLang: json['to_lang'] as String?,
      toText: json['to_text'] as String?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'lang': lang,
      'id': id,
      'text': text,
      'source': source,
      'to_lang': toLang,
      'to_text': toText,
    };
  }
}

