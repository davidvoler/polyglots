class AddCorpusRequest {
  final String corpus;
  final String? description;
  final String? url;

  AddCorpusRequest({
    required this.corpus,
    this.description,
    this.url,
  });

  Map<String, dynamic> toJson() {
    return {
      'corpus': corpus,
      'description': description,
      'url': url,
    };
  }
}

class TranslateRequest {
  final String operation;
  final String source;
  final String lang;
  final String toLang;
  final bool review;
  final int limit;
  final int offset;

  TranslateRequest({
    this.operation = 'translate',
    required this.source,
    required this.lang,
    required this.toLang,
    this.review = true,
    this.limit = -1,
    this.offset = 0,
  });

  Map<String, dynamic> toJson() {
    return {
      'operation': operation,
      'source': source,
      'lang': lang,
      'to_lang': toLang,
      'review': review,
      'limit': limit,
      'offset': offset,
    };
  }
}

class AnalyzeRequest {
  final String operation;
  final String source;
  final String lang;
  final bool review;
  final int limit;
  final int offset;

  AnalyzeRequest({
    this.operation = 'analyze',
    required this.source,
    required this.lang,
    this.review = true,
    this.limit = -1,
    this.offset = 0,
  });

  Map<String, dynamic> toJson() {
    return {
      'operation': operation,
      'source': source,
      'lang': lang,
      'review': review,
      'limit': limit,
      'offset': offset,
    };
  }
}

class ReviewRequest {
  final String operation;
  final String source;
  final String lang;
  final bool review;
  final int limit;
  final int offset;

  ReviewRequest({
    required this.operation,
    required this.source,
    required this.lang,
    this.review = true,
    this.limit = 300,
    this.offset = 0,
  });

  Map<String, dynamic> toJson() {
    return {
      'operation': operation,
      'source': source,
      'lang': lang,
      'review': review,
      'limit': limit,
      'offset': offset,
    };
  }
}

class TransliterateRequest {
  final String operation;
  final String source;
  final String lang;
  final bool review;
  final int limit;
  final int offset;

  TransliterateRequest({
    this.operation = 'transliterate',
    required this.source,
    required this.lang,
    this.review = true,
    this.limit = -1,
    this.offset = 0,
  });

  Map<String, dynamic> toJson() {
    return {
      'operation': operation,
      'source': source,
      'lang': lang,
      'review': review,
      'limit': limit,
      'offset': offset,
    };
  }
}

class LoadCsvRequest {
  final String filePath;
  final String corpus;
  final String lang;
  final Map<String, dynamic>? options;

  LoadCsvRequest({
    required this.filePath,
    required this.corpus,
    required this.lang,
    this.options,
  });

  Map<String, dynamic> toJson() {
    return {
      'file_path': filePath,
      'corpus': corpus,
      'lang': lang,
      if (options != null) 'options': options,
    };
  }
}

class GenerateContentRequest {
  final String operation;
  final String source;
  final String lang;
  final String? toLang;
  final bool review;
  final int limit;
  final int offset;
  final Map<String, dynamic>? options;

  GenerateContentRequest({
    this.operation = 'generate',
    required this.source,
    required this.lang,
    this.toLang,
    this.review = true,
    this.limit = -1,
    this.offset = 0,
    this.options,
  });

  Map<String, dynamic> toJson() {
    return {
      'operation': operation,
      'source': source,
      'lang': lang,
      if (toLang != null) 'to_lang': toLang,
      'review': review,
      'limit': limit,
      'offset': offset,
      if (options != null) 'options': options,
    };
  }
}

class GroupSentencesRequest {
  final String operation;
  final String source;
  final String lang;
  final bool review;
  final int limit;
  final int offset;
  final Map<String, dynamic>? options;

  GroupSentencesRequest({
    this.operation = 'group',
    required this.source,
    required this.lang,
    this.review = true,
    this.limit = -1,
    this.offset = 0,
    this.options,
  });

  Map<String, dynamic> toJson() {
    return {
      'operation': operation,
      'source': source,
      'lang': lang,
      'review': review,
      'limit': limit,
      'offset': offset,
      if (options != null) 'options': options,
    };
  }
}

