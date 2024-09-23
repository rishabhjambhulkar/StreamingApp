Here’s a sample `README.md` file that includes both API documentation and user documentation for your application.

```markdown
# Streaming App

## API Documentation

This document provides details on the CRUD endpoints available in the Streaming App.

### Base URL
```
http://localhost:5000
```

### Endpoints

#### 1. **Create Overlay**
- **Endpoint**: `/api/overlay`
- **Method**: `POST`
- **Request Body**: 
```json
{
  "userId": "string",
  "position": {
    "x": "number",
    "y": "number"
  },
  "size": {
    "width": "number",
    "height": "number"
  },
  "content": "string"
}
```
- **Response**:
  - Status: `201 Created`
  - Body: 
```json
{
  "message": "Overlay created!"
}
```

#### 2. **Get Overlays**
- **Endpoint**: `/api/overlays`
- **Method**: `POST`
- **Request Body**:
```json
{
  "userId": "string"
}
```
- **Response**:
  - Status: `200 OK`
  - Body: 
```json
[
  {
    "_id": "string",
    "userId": "string",
    "position": {
      "x": "number",
      "y": "number"
    },
    "size": {
      "width": "number",
      "height": "number"
    },
    "content": "string"
  }
]
```

#### 3. **Update Overlay**
- **Endpoint**: `/api/updateOverlay`
- **Method**: `POST`
- **Request Body**:
```json
{
  "_id": "string",
  "position": {
    "x": "number",
    "y": "number"
  },
  "size": {
    "width": "number",
    "height": "number"
  },
  "content": "string"
}
```
- **Response**:
  - Status: `200 OK`
  - Body: 
```json
{
  "message": "Overlay updated successfully."
}
```
  - Status: `404 Not Found`
  - Body: 
```json
{
  "error": "Overlay not found."
}
```

#### 4. **Delete Overlay**
- **Endpoint**: `/api/delete`
- **Method**: `DELETE`
- **Request Body**:
```json
{
  "overlayId": "string"
}
```
- **Response**:
  - Status: `200 OK`
  - Body: 
```json
{
  "message": "Overlay deleted!"
}
```
  - Status: `404 Not Found`
  - Body: 
```json
{
  "message": "Overlay not found!"
}
```

### Notes
- Ensure that the MongoDB instance is running before using the API.
- The application uses Flask and requires Python 3.x.

## User Documentation

### Setting Up the Application

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` File**
   In the root directory of the project, create a file named `.env` and add the following environment variables:
   ```env
   MONGO_URI=mongodb://127.0.0.1:27017/streamapp
   HLS_OUTPUT_DIR=<your-hls-output-directory>
   RTSP_URL=<your-rtsp-url>
   FFMPEG_PATH=<path-to-ffmpeg>
   FRONTEND_URL=http://localhost:3000
   ```

   - Replace `<your-hls-output-directory>` with the directory where HLS files will be stored.
   - Replace `<your-rtsp-url>` with the RTSP URL you want to stream.
   - Replace `<path-to-ffmpeg>` with the path to your FFmpeg executable.

4. **Run the Application**
   ```bash
   python app.py
   ```

### How to Input the RTSP URL

- The RTSP URL is specified in the `.env` file under the `RTSP_URL` variable. Modify this value to set the desired RTSP stream.

### Managing Overlays

1. **Creating Overlays**
   - Send a `POST` request to `/api/overlay` with the overlay details in the request body.

2. **Retrieving Overlays**
   - Send a `POST` request to `/api/overlays` with the `userId` in the request body to get all overlays for a specific user.

3. **Updating Overlays**
   - Send a `POST` request to `/api/updateOverlay` with the overlay ID and the updated details.

4. **Deleting Overlays**
   - Send a `DELETE` request to `/api/delete` with the overlay ID in the request body to remove an overlay.


