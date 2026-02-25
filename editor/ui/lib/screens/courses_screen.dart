import 'package:flutter/material.dart';
import 'create_course_screen.dart';
import 'editor_flow_screen.dart';
// TODO: Create course_module_editor_screen.dart
// import 'course_module_editor_screen.dart';

class CoursesScreen extends StatelessWidget {
  const CoursesScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Courses'),
        automaticallyImplyLeading: false,
        actions: [
          IconButton(
            icon: const Icon(Icons.add),
            tooltip: 'Create New Course',
            onPressed: () {
              Navigator.of(context).push(
                MaterialPageRoute(
                  builder: (context) => const CreateCourseScreen(),
                ),
              );
            },
          ),
        ],
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(
              Icons.school,
              size: 64,
              color: Colors.grey,
            ),
            const SizedBox(height: 16),
            const Text(
              'Courses Management',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: Colors.grey,
              ),
            ),
            const SizedBox(height: 32),
            ElevatedButton.icon(
              onPressed: () {
                Navigator.of(context).push(
                  MaterialPageRoute(
                    builder: (context) => const EditorCreateCourseScreen(),
                  ),
                );
              },
              icon: const Icon(Icons.auto_awesome),
              label: const Text('Create Course'),
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(
                  horizontal: 24,
                  vertical: 12,
                ),
                backgroundColor: Colors.deepPurple,
                foregroundColor: Colors.white,
              ),
            ),
            const SizedBox(height: 16),
            ElevatedButton.icon(
              onPressed: () {
                Navigator.of(context).push(
                  MaterialPageRoute(
                    builder: (context) => const CreateCourseScreen(),
                  ),
                );
              },
              icon: const Icon(Icons.add),
              label: const Text('Create Course (legacy)'),
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(
                  horizontal: 24,
                  vertical: 12,
                ),
              ),
            ),
            // TODO: Uncomment when course_module_editor_screen.dart is created
            // const SizedBox(height: 16),
            // ElevatedButton.icon(
            //   onPressed: () {
            //     // TODO: Replace with actual course selection
            //     Navigator.of(context).push(
            //       MaterialPageRoute(
            //         builder: (context) => const CourseModuleEditorScreen(
            //           courseName: 'Sample Course',
            //         ),
            //       ),
            //     );
            //   },
            //   icon: const Icon(Icons.edit),
            //   label: const Text('Edit Course Modules (Demo)'),
            //   style: ElevatedButton.styleFrom(
            //     padding: const EdgeInsets.symmetric(
            //       horizontal: 24,
            //       vertical: 12,
            //     ),
            //   ),
            // ),
          ],
        ),
      ),
    );
  }
}
