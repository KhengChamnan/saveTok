import 'package:flutter/material.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(const TikTokDownloaderApp());
}

class TikTokDownloaderApp extends StatelessWidget {
  const TikTokDownloaderApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'TikTok Downloader',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFFFE2C55),
          brightness: Brightness.light,
        ),
        useMaterial3: true,
      ),
      home: const HomeScreen(),
    );
  }
}
