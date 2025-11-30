import 'dart:io';
import 'package:dio/dio.dart';
import 'package:path_provider/path_provider.dart';
import 'package:image_gallery_saver/image_gallery_saver.dart';

class ApiService {
  // Change this to your backend URL
  // For Android emulator use: http://10.0.2.2:8000
  // For iOS simulator use: http://localhost:8000
  // For physical device use your computer's IP: http://192.168.x.x:8000
  static const String baseUrl = 'https://savetok-service.onrender.com';

  final Dio _dio = Dio(
    BaseOptions(
      baseUrl: baseUrl,
      connectTimeout: const Duration(seconds: 30),
      receiveTimeout: const Duration(seconds: 60),
    ),
  );

  Future<Map<String, dynamic>> getVideoInfo(String url) async {
    try {
      final response = await _dio.post('/api/info', data: {'url': url});
      return response.data;
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<Map<String, dynamic>> requestDownload(String url) async {
    try {
      final response = await _dio.post('/api/download', data: {'url': url});
      return response.data;
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<String> downloadFile(
    String downloadPath,
    String filename, {
    Function(int, int)? onProgress,
  }) async {
    try {
      final directory = await getApplicationDocumentsDirectory();
      final savePath = '${directory.path}/$filename';

      await _dio.download(
        '$baseUrl$downloadPath',
        savePath,
        onReceiveProgress: onProgress,
      );

      return savePath;
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<Map<String, dynamic>> downloadToDownloads(
    String downloadPath,
    String filename, {
    Function(int, int)? onProgress,
  }) async {
    try {
      Directory? directory;
      String savePath;

      if (Platform.isAndroid) {
        // Android: Save to Downloads folder
        directory = Directory('/storage/emulated/0/Download');
        if (!await directory.exists()) {
          directory = await getExternalStorageDirectory();
        }
        savePath = '${directory!.path}/TikTok_$filename';

        await _dio.download(
          '$baseUrl$downloadPath',
          savePath,
          onReceiveProgress: onProgress,
        );

        return {'path': savePath, 'savedToPhotos': false};
      } else {
        // iOS: Download to temp directory first, then save to Photos
        final tempDir = await getTemporaryDirectory();
        savePath = '${tempDir.path}/TikTok_$filename';

        await _dio.download(
          '$baseUrl$downloadPath',
          savePath,
          onReceiveProgress: onProgress,
        );

        // Save to Photos library
        final result = await ImageGallerySaver.saveFile(
          savePath,
          name: 'TikTok_$filename',
        );

        // Delete temp file
        final tempFile = File(savePath);
        if (await tempFile.exists()) {
          await tempFile.delete();
        }

        if (result['isSuccess'] == true) {
          return {'path': 'Photos Library', 'savedToPhotos': true};
        } else {
          throw 'Failed to save video to Photos library';
        }
      }
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  String _handleError(DioException e) {
    if (e.response != null) {
      final data = e.response?.data;
      if (data is Map && data.containsKey('detail')) {
        return data['detail'];
      }
      return 'Server error: ${e.response?.statusCode}';
    }
    if (e.type == DioExceptionType.connectionTimeout) {
      return 'Connection timeout. Please check your internet connection.';
    }
    if (e.type == DioExceptionType.connectionError) {
      return 'Cannot connect to server. Make sure the backend is running.';
    }
    return 'Network error: ${e.message}';
  }
}
