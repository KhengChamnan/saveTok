# SaveTok

A full-stack application to download TikTok videos without watermark. Built with FastAPI backend, React web frontend, and Flutter mobile app.

## Project Structure

```
video_scraper/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py         # Main API endpoints
│   │   └── services/
│   │       └── downloader.py  # yt-dlp wrapper
│   ├── downloads/          # Temporary video storage
│   └── requirements.txt
├── frontend/
│   ├── web/                # React web app
│   │   ├── src/
│   │   └── package.json
│   └── mobile/             # Flutter mobile app
│       ├── lib/
│       └── pubspec.yaml
└── README.md
```

## Prerequisites

- **Python 3.9+** (for backend)
- **Node.js 18+** (for web frontend)
- **Flutter 3.0+** (for mobile app)
- **ffmpeg** (required by yt-dlp for video processing)

### Install ffmpeg on Windows
```powershell
winget install ffmpeg
```

## Backend Setup

1. Navigate to the backend directory:
```powershell
cd backend
```

2. Create a virtual environment:
```powershell
python -m venv venv
.\venv\Scripts\Activate
```

3. Install dependencies:
```powershell
pip install -r requirements.txt
```

4. Run the server:
```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### API Endpoints

- `GET /` - Health check
- `POST /api/info` - Get video info without downloading
- `POST /api/download` - Download video and get download URL
- `GET /api/file/{filename}` - Serve downloaded video file
- `DELETE /api/file/{filename}` - Delete a downloaded file

## Web Frontend Setup

1. Navigate to the web frontend directory:
```powershell
cd frontend\web
```

2. Install dependencies:
```powershell
npm install
```

3. Run the development server:
```powershell
npm run dev
```

The web app will be available at `http://localhost:5173`

## Mobile App Setup (Flutter)

1. Navigate to the mobile directory:
```powershell
cd frontend\mobile
```

2. Get Flutter dependencies:
```powershell
flutter pub get
```

3. **Configure the API URL:**
   Edit `lib/services/api_service.dart` and update `baseUrl`:
   - For Android emulator: `http://10.0.2.2:8000`
   - For iOS simulator: `http://localhost:8000`
   - For physical device: Use your computer's IP (e.g., `http://192.168.1.100:8000`)

4. Run the app:
```powershell
flutter run
```

## Usage

1. Start the backend server first
2. Open either the web app or mobile app
3. Paste a TikTok video URL
4. Click "Download"
5. The video will be downloaded to your device

## Notes

- Downloaded videos are temporarily stored in the `backend/downloads` folder
- The mobile app saves videos to the Downloads folder on Android
- For personal use only - respect content creators' rights
- TikTok may rate-limit requests; avoid excessive downloads

## Troubleshooting

### Backend Issues
- Ensure ffmpeg is installed: `ffmpeg -version`
- Check if yt-dlp is up to date: `pip install --upgrade yt-dlp`

### Mobile App Issues
- For Android: Enable "Install from unknown sources" if needed
- Check storage permissions are granted
- Ensure the backend URL is correctly configured for your device

### Web App Issues
- Check if the backend is running on port 8000
- The Vite proxy should handle API requests automatically
# saveTok
