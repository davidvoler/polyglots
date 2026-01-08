import 'package:flutter/material.dart';

import '../../../../core/services/course_service.dart';
import '../../../../shared/models/course_model.dart';

class CourseDetailPage extends StatelessWidget {
  final int courseId;
  final Course? initialCourse;

  const CourseDetailPage({
    super.key,
    required this.courseId,
    this.initialCourse,
  });

  Future<Course> _loadCourse() {
    if (initialCourse != null && initialCourse!.modules.isNotEmpty) {
      return Future.value(initialCourse!);
    }
    return CourseService.fetchCourseById(courseId);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Course details'),
      ),
      body: FutureBuilder<Course>(
        future: _loadCourse(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }

          if (snapshot.hasError) {
            return _buildError(snapshot.error);
          }

          final course = snapshot.data ?? initialCourse;
          if (course == null) {
            return _buildError('Course not found');
          }

          if (course.modules.isEmpty) {
            return _buildEmptyModules(course);
          }

          return ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: course.modules.length,
            itemBuilder: (context, index) {
              final module = course.modules[index];
              return Card(
                margin: const EdgeInsets.only(bottom: 12),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
                elevation: 1,
                child: ExpansionTile(
                  leading: const Icon(Icons.folder),
                  title: Text(
                    module.name,
                    style: const TextStyle(
                      fontWeight: FontWeight.w700,
                    ),
                  ),
                  subtitle: Text(
                    module.description.isNotEmpty
                        ? module.description
                        : 'Module ${index + 1}',
                  ),
                  children: [
                    if (module.lessons.isEmpty)
                      Padding(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 16,
                          vertical: 12,
                        ),
                        child: Text(
                          'No lessons yet.',
                          style: TextStyle(color: Colors.grey.shade600),
                        ),
                      )
                    else
                      ...module.lessons.map(
                        (lesson) => ListTile(
                          leading: const Icon(Icons.menu_book_outlined),
                          title: Text(lesson.name),
                          subtitle: lesson.description.isNotEmpty
                              ? Text(lesson.description)
                              : null,
                        ),
                      ),
                  ],
                ),
              );
            },
          );
        },
      ),
    );
  }

  Widget _buildError(Object? error) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(Icons.error_outline, size: 64, color: Colors.red.shade300),
          const SizedBox(height: 12),
          Text(
            'Failed to load course',
            style: TextStyle(
              fontSize: 16,
              color: Colors.red.shade400,
              fontWeight: FontWeight.w600,
            ),
          ),
          const SizedBox(height: 8),
          Text(
            error?.toString() ?? 'Unknown error',
            textAlign: TextAlign.center,
            style: TextStyle(
              fontSize: 14,
              color: Colors.grey.shade600,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildEmptyModules(Course course) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.layers_clear, size: 64, color: Colors.grey.shade400),
            const SizedBox(height: 12),
            Text(
              course.name,
              style: const TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              'No modules available for this course yet.',
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 14,
                color: Colors.grey.shade600,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

