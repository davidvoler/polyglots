class Corpus {
  final String name;
  final int sentenceCount;
  final String? url;
  final String? description;

  Corpus({
    required this.name,
    required this.sentenceCount,
    this.url,
    this.description,
  });

  factory Corpus.fromJson(Map<String, dynamic> json) {
    return Corpus(
      name: json['corpus'] as String,
      sentenceCount: json['sentence_count'] as int? ?? 0,
      url: json['url'] as String?,
      description: json['description'] as String?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'corpus': name,
      'sentence_count': sentenceCount,
      'url': url,
      'description': description,
    };
  }
}

