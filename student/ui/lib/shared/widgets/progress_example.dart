import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../providers/progress_provider.dart';

/// Example widget showing how to use the progress provider
/// This demonstrates how progress data is fetched from the backend API
class ProgressExample extends ConsumerWidget {
  const ProgressExample({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final progressState = ref.watch(progressProvider);
    final questionsToday = ref.watch(questionsTodayProvider);
    final totalQuestions = ref.watch(totalQuestionsProvider);
    final lastQuizScore = ref.watch(lastQuizScoreProvider);
    final progressPercentage = ref.watch(progressPercentageProvider);
    
    return Scaffold(
      appBar: AppBar(
        title: const Text('Progress Example'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () => ref.read(progressProvider.notifier).refresh(),
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Progress Data (from API):',
              style: Theme.of(context).textTheme.headlineSmall,
            ),
            const SizedBox(height: 16),
            
            // Loading state
            if (progressState.isLoading)
              const Center(child: CircularProgressIndicator()),
              
            // Error state
            if (progressState.error != null)
              Container(
                padding: const EdgeInsets.all(8),
                color: Colors.red.shade100,
                child: Text(
                  'Error: ${progressState.error}',
                  style: TextStyle(color: Colors.red.shade800),
                ),
              ),
              
            // Progress data
            if (progressState.data != null) ...[
              _buildProgressCard(
                context,
                'Questions Today',
                '$questionsToday',
                Icons.question_answer,
                Colors.blue,
              ),
              
              _buildProgressCard(
                context,
                'Total Questions',
                '$totalQuestions',
                Icons.quiz,
                Colors.green,
              ),
              
              _buildProgressCard(
                context,
                'Last Quiz Score',
                '$lastQuizScore',
                Icons.star,
                Colors.orange,
              ),
              
              _buildProgressCard(
                context,
                'Progress Percentage',
                '${(progressPercentage * 100).round()}%',
                Icons.trending_up,
                Colors.purple,
              ),
              
              const SizedBox(height: 16),
              
              // Progress bar
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(12),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withOpacity(0.1),
                      blurRadius: 8,
                      offset: const Offset(0, 2),
                    ),
                  ],
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Overall Progress',
                      style: Theme.of(context).textTheme.titleMedium,
                    ),
                    const SizedBox(height: 8),
                    LinearProgressIndicator(
                      value: progressPercentage,
                      backgroundColor: Colors.grey.shade200,
                      valueColor: AlwaysStoppedAnimation<Color>(Colors.blue.shade600),
                      minHeight: 12,
                    ),
                    const SizedBox(height: 8),
                    Text(
                      '${(progressPercentage * 100).round()}% complete',
                      style: TextStyle(
                        fontSize: 14,
                        color: Colors.grey.shade600,
                      ),
                    ),
                  ],
                ),
              ),
              
              const SizedBox(height: 16),
              
              // Last updated info
              if (progressState.lastUpdated != null)
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.blue.shade50,
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Text(
                    'Last updated: ${progressState.lastUpdated!.toString().substring(0, 19)}',
                    style: TextStyle(
                      fontSize: 12,
                      color: Colors.blue.shade700,
                    ),
                  ),
                ),
            ],
            
            const SizedBox(height: 24),
            
            // Instructions
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.blue.shade50,
                borderRadius: BorderRadius.circular(8),
              ),
              child: const Text(
                '💡 This data is fetched from the backend API!\n\n'
                '• Tap the refresh button to reload data\n'
                '• Data is automatically loaded when the app starts\n'
                '• Falls back to default data if API fails\n'
                '• Shows loading and error states',
                style: TextStyle(fontSize: 14),
              ),
            ),
          ],
        ),
      ),
    );
  }
  
  Widget _buildProgressCard(
    BuildContext context,
    String title,
    String value,
    IconData icon,
    Color color,
  ) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.1),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: color.withOpacity(0.1),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Icon(
              icon,
              color: color,
              size: 24,
            ),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.grey.shade600,
                  ),
                ),
                Text(
                  value,
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                    color: Colors.grey.shade800,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
} 