class DashboardContent {
  final String corpus;
  final String lang;
  final int cnt;

  DashboardContent({
    required this.corpus,
    required this.lang,
    required this.cnt,
  });

  factory DashboardContent.fromJson(Map<String, dynamic> json) {
    return DashboardContent(
      corpus: json['corpus'] as String? ?? '',
      lang: json['lang'] as String? ?? '',
      cnt: json['cnt'] as int? ?? 0,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'corpus': corpus,
      'lang': lang,
      'cnt': cnt,
    };
  }
}

class DashboardContentElements {
  final String lang;
  final int cnt;

  DashboardContentElements({
    required this.lang,
    required this.cnt,
  });

  factory DashboardContentElements.fromJson(Map<String, dynamic> json) {
    return DashboardContentElements(
      lang: json['lang'] as String? ?? '',
      cnt: json['cnt'] as int? ?? 0,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'lang': lang,
      'cnt': cnt,
    };
  }
}

class DashboardAudio {
  final String audioEngine;
  final String voice;
  final String lang;
  final int cnt;

  DashboardAudio({
    required this.audioEngine,
    required this.voice,
    required this.lang,
    required this.cnt,
  });

  factory DashboardAudio.fromJson(Map<String, dynamic> json) {
    return DashboardAudio(
      audioEngine: json['audio_engine'] as String? ?? '',
      voice: json['voice'] as String? ?? '',
      lang: json['lang'] as String? ?? '',
      cnt: json['cnt'] as int? ?? 0,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'audio_engine': audioEngine,
      'voice': voice,
      'lang': lang,
      'cnt': cnt,
    };
  }
}

class DashboardResponse {
  final List<DashboardContent> content;
  final List<DashboardContentElements> contentElements;
  final List<DashboardAudio> audio;

  DashboardResponse({
    required this.content,
    required this.contentElements,
    required this.audio,
  });

  factory DashboardResponse.fromJson(Map<String, dynamic> json) {
    return DashboardResponse(
      content: (json['content'] as List<dynamic>?)
              ?.map((item) => DashboardContent.fromJson(item as Map<String, dynamic>))
              .toList() ??
          [],
      contentElements: (json['content_elements'] as List<dynamic>?)
              ?.map((item) => DashboardContentElements.fromJson(item as Map<String, dynamic>))
              .toList() ??
          [],
      audio: (json['audio'] as List<dynamic>?)
              ?.map((item) => DashboardAudio.fromJson(item as Map<String, dynamic>))
              .toList() ??
          [],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'content': content.map((item) => item.toJson()).toList(),
      'content_elements': contentElements.map((item) => item.toJson()).toList(),
      'audio': audio.map((item) => item.toJson()).toList(),
    };
  }
}

