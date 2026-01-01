class Lesson {
  final int id;
  final String name;
  final String description;
  final String image;

  Lesson({
    required this.id,
    required this.name,
    this.description = '',
    this.image = '',
  });

  factory Lesson.fromJson(Map<String, dynamic> json) {
    return Lesson(
      id: json['id'] ?? 0,
      name: json['name'] ?? '',
      description: json['description'] ?? '',
      image: json['image'] ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'description': description,
      'image': image,
    };
  }
}

class Module {
  final int id;
  final String name;
  final String description;
  final String image;
  final List<Lesson> lessons;

  Module({
    required this.id,
    required this.name,
    this.description = '',
    this.image = '',
    this.lessons = const [],
  });

  factory Module.fromJson(Map<String, dynamic> json) {
    final lessonsJson = json['lessons'] as List<dynamic>? ?? [];

    return Module(
      id: json['id'] ?? 0,
      name: json['name'] ?? '',
      description: json['description'] ?? '',
      image: json['image'] ?? '',
      lessons: lessonsJson
          .map((lesson) => Lesson.fromJson(lesson as Map<String, dynamic>))
          .toList(),
    );
  }

  int get lessonsCount => lessons.length;

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'description': description,
      'image': image,
      'lessons': lessons.map((lesson) => lesson.toJson()).toList(),
    };
  }
}

class Course {
  final int id;
  final String lang;
  final String toLang;
  final String name;
  final String description;
  final String image;
  final List<Module> modules;
  final int modulesCount;
  final int lessonsCount;

  Course({
    required this.id,
    required this.lang,
    required this.toLang,
    required this.name,
    this.description = '',
    this.image = '',
    this.modules = const [],
    this.modulesCount = 0,
    this.lessonsCount = 0,
  });

  factory Course.fromJson(Map<String, dynamic> json) {
    final modulesJson = json['modules'] as List<dynamic>? ?? [];
    final modules = modulesJson
        .map((module) => Module.fromJson(module as Map<String, dynamic>))
        .toList();

    final computedLessonsCount = modules.fold<int>(
      0,
      (sum, module) => sum + module.lessonsCount,
    );

    return Course(
      id: json['id'] ?? 0,
      lang: json['lang'] ?? '',
      toLang: json['to_lang'] ?? '',
      name: json['name'] ?? '',
      description: json['description'] ?? '',
      image: json['image'] ?? '',
      modules: modules,
      modulesCount: json['modules_count'] ?? modules.length,
      lessonsCount: json['lessons_count'] ?? computedLessonsCount,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'lang': lang,
      'to_lang': toLang,
      'name': name,
      'description': description,
      'image': image,
      'modules': modules.map((module) => module.toJson()).toList(),
      'modules_count': modulesCount,
      'lessons_count': lessonsCount,
    };
  }
}

