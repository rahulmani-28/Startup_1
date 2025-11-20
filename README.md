## Travel Buddy (Chariot Testing)

Monorepo for a smart travel companion app.

### Structure
- `backend`: FastAPI + MongoDB Atlas
- `frontend`: React Native app
- `infra`: infra/config placeholders
- `scripts`: helper scripts

### Backend (Phase 1)
1. Create `backend/.env` with:
   - `MONGODB_URI=mongodb://localhost:27017` (or your Atlas URI)
   - `DATABASE_NAME=travel_buddy`
   - `APP_NAME=Travel Buddy (Chariot Testing) Backend`
   - `CORS_ORIGINS=*`
2. Create venv, install requirements, and run:
   - `cd backend`
   - `python -m venv .venv`
   - `./.venv/Scripts/pip install -r requirements.txt`
   - `./.venv/Scripts/python -m uvicorn app.main:app --reload --port 8000`
3. Endpoints (Phase 1):
   - `POST /journey/start`
   - `POST /journey/track`
   - `POST /journey/stop`

### Frontend
Lives in `frontend/` (React Native 0.75).

Run:
- `cd frontend`
- `npm install`
- `npm start`
- Android: `npm run android` (emulator or device). The app calls backend at `http://10.0.2.2:8000` on Android and `http://localhost:8000` on iOS.

Permissions:
- Android: Location permissions added in `android/app/src/main/AndroidManifest.xml`.
- iOS: Location usage strings added in `ios/TravelBuddyChariot/Info.plist`.

Phase 1 UI:
- Home shows Start/Stop, speed, distance, ETA (computed from backend response).


