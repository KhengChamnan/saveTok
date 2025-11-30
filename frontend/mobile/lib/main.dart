import 'package:flutter/material.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(const SaveTokApp());
}

class SaveTokApp extends StatelessWidget {
  const SaveTokApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'SaveTok',
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
