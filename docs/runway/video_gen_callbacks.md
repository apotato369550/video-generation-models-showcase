# AI Video Generation Callbacks

>When you submit a video generation task to the Runway API, you can use the `callBackUrl` parameter to set a callback URL. The system will automatically push the results to your specified address when the task is completed.

## Callback Mechanism Overview

:::note[]
The callback mechanism eliminates the need to poll the API for task status. The system will proactively push task completion results to your server.
:::

### Callback Timing

The system will send callback notifications in the following situations:

- AI video generation task completed successfully
- AI video generation task failed
- Errors occurred during task processing

### Callback Method

- **HTTP Method**: POST
- **Content Type**: application/json
- **Timeout Setting**: 15 seconds

## Callback Request Format

When the task is completed, the system will send a POST request to your `callBackUrl` in the following format:


<Tabs>
<TabItem value="success" label="Success Callback">

```json
{
  "code": 200,
  "msg": "All generated successfully.",
  "data": {
    "task_id": "ee603959-debb-48d1-98c4-a6d1c717eba6",
    "video_id": "485da89c-7fca-4340-8c04-101025b2ae71",
    "video_url": "https://file.com/k/xxxxxxx.mp4",
    "image_url": "https://file.com/m/xxxxxxxx.png"
  }
}
```

</TabItem>
<TabItem value="failure" label="Failure Callback">

```json
{
  "code": 400,
  "msg": "Inappropriate content detected. Please replace the image or video.",
  "data": {
    "task_id": "ee603959-debb-48d1-98c4-a6d1c717eba6",
    "video_id": "",
    "video_url": "",
    "image_url": ""
  }
}
```

</TabItem>
</Tabs>

## Status Code Description

### Parameter Description

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `code` | integer | Yes | Callback status code indicating task processing result |
| `msg` | string | Yes | Status message providing detailed status description |
| `data.task_id` | string | Yes | Task ID, consistent with the taskId returned when you submitted the task |
| `data.video_id` | string | Yes | Generated video ID for identification and tracking |
| `data.video_url` | string | No | Accessible video URL, **valid for 14 days**. Empty on failure |
| `data.image_url` | string | No | Cover image URL of the generated video. Empty on failure |

### Status Code Details

| Status Code | Description |
|-------------|-------------|
| 200 | Success - Video generation completed successfully |
| 400 | Client Error - Inappropriate content, format error, quota limit, or other client-side issues |
| 500 | Server Error - Internal server error during video generation |

### Common Error Messages

Common error messages include:

- "Inappropriate content detected. Please replace the image or video."
- "Incorrect image format."
- "Please try again later. You can upgrade to Standard membership to start generating now."
- "Reached the limit for concurrent generations."
- "Unsupported width or height. Please adjust the size and try again."
- "Your prompt was caught by our AI moderator. Please adjust it and try again!"

## Callback Reception Examples

Here are example codes for receiving callbacks in popular programming languages:

<Tabs>
<TabItem value="javascript" label="Node.js">

```javascript
const express = require('express');
const fs = require('fs');
const https = require('https');
const path = require('path');
const app = express();

app.use(express.json());

app.post('/runway-video-callback', (req, res) => {
  const { code, msg, data } = req.body;
  
  console.log('Received Runway video generation callback:', {
    taskId: data.task_id,
    videoId: data.video_id,
    status: code,
    message: msg
  });
  
  if (code === 200) {
    // Task completed successfully
    console.log('Runway video generation completed successfully');
    
    const { task_id, video_id, video_url, image_url } = data;
    
    console.log(`Video URL: ${video_url}`);
    console.log(`Cover Image URL: ${image_url}`);
    console.log('Note: Video URL is valid for 14 days');
    
    // Download video file
    if (video_url) {
      downloadFile(video_url, `runway_video_${task_id}.mp4`)
        .then(() => console.log('Video downloaded successfully'))
        .catch(err => console.error('Video download failed:', err));
    }
    
    // Download cover image
    if (image_url) {
      downloadFile(image_url, `runway_cover_${task_id}.png`)
        .then(() => console.log('Cover image downloaded successfully'))
        .catch(err => console.error('Cover image download failed:', err));
    }
    
  } else {
    // Task failed
    console.log('Runway video generation failed:', msg);
    
    // Handle specific error types
    if (code === 400) {
      console.log('Client error - check content, format, or quota');
    } else if (code === 500) {
      console.log('Server error - retry may be needed');
    }
  }
  
  // Return 200 status code to confirm callback received
  res.status(200).json({ status: 'received' });
});

// Helper function to download files
function downloadFile(url, filename) {
  return new Promise((resolve, reject) => {
    const file = fs.createWriteStream(filename);
    
    https.get(url, (response) => {
      if (response.statusCode === 200) {
        response.pipe(file);
        file.on('finish', () => {
          file.close();
          resolve();
        });
      } else {
        reject(new Error(`HTTP ${response.statusCode}`));
      }
    }).on('error', reject);
  });
}

app.listen(3000, () => {
  console.log('Callback server running on port 3000');
});
```

</TabItem>
<TabItem value="python" label="Python">

```python
from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/runway-video-callback', methods=['POST'])
def handle_callback():
    data = request.json
    
    code = data.get('code')
    msg = data.get('msg')
    callback_data = data.get('data', {})
    task_id = callback_data.get('task_id')
    video_id = callback_data.get('video_id')
    video_url = callback_data.get('video_url')
    image_url = callback_data.get('image_url')
    
    print(f"Received Runway video generation callback:")
    print(f"Task ID: {task_id}, Video ID: {video_id}")
    print(f"Status: {code}, Message: {msg}")
    
    if code == 200:
        # Task completed successfully
        print("Runway video generation completed successfully")
        
        print(f"Video URL: {video_url}")
        print(f"Cover Image URL: {image_url}")
        print("Note: Video URL is valid for 14 days")
        
        # Download video file
        if video_url:
            try:
                video_filename = f"runway_video_{task_id}.mp4"
                download_file(video_url, video_filename)
                print(f"Video downloaded as {video_filename}")
            except Exception as e:
                print(f"Video download failed: {e}")
        
        # Download cover image
        if image_url:
            try:
                image_filename = f"runway_cover_{task_id}.png"
                download_file(image_url, image_filename)
                print(f"Cover image downloaded as {image_filename}")
            except Exception as e:
                print(f"Cover image download failed: {e}")
                
    else:
        # Task failed
        print(f"Runway video generation failed: {msg}")
        
        # Handle specific error types
        if code == 400:
            print("Client error - check content, format, or quota")
        elif code == 500:
            print("Server error - retry may be needed")
    
    # Return 200 status code to confirm callback received
    return jsonify({'status': 'received'}), 200

def download_file(url, filename):
    """Download file from URL and save locally"""
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    os.makedirs('downloads', exist_ok=True)
    filepath = os.path.join('downloads', filename)
    
    with open(filepath, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
```

</TabItem>
<TabItem value="php" label="PHP">

```php
<?php
header('Content-Type: application/json');

// Get POST data
$input = file_get_contents('php://input');
$data = json_decode($input, true);

$code = $data['code'] ?? null;
$msg = $data['msg'] ?? '';
$callbackData = $data['data'] ?? [];
$taskId = $callbackData['task_id'] ?? '';
$videoId = $callbackData['video_id'] ?? '';
$videoUrl = $callbackData['video_url'] ?? '';
$imageUrl = $callbackData['image_url'] ?? '';

error_log("Received Runway video generation callback:");
error_log("Task ID: $taskId, Video ID: $videoId");
error_log("Status: $code, Message: $msg");

if ($code === 200) {
    // Task completed successfully
    error_log("Runway video generation completed successfully");
    
    error_log("Video URL: $videoUrl");
    error_log("Cover Image URL: $imageUrl");
    error_log("Note: Video URL is valid for 14 days");
    
    // Download video file
    if (!empty($videoUrl)) {
        try {
            $videoFilename = "runway_video_{$taskId}.mp4";
            downloadFile($videoUrl, $videoFilename);
            error_log("Video downloaded as $videoFilename");
        } catch (Exception $e) {
            error_log("Video download failed: " . $e->getMessage());
        }
    }
    
    // Download cover image
    if (!empty($imageUrl)) {
        try {
            $imageFilename = "runway_cover_{$taskId}.png";
            downloadFile($imageUrl, $imageFilename);
            error_log("Cover image downloaded as $imageFilename");
        } catch (Exception $e) {
            error_log("Cover image download failed: " . $e->getMessage());
        }
    }
    
} else {
    // Task failed
    error_log("Runway video generation failed: $msg");
    
    // Handle specific error types
    if ($code === 400) {
        error_log("Client error - check content, format, or quota");
    } elseif ($code === 500) {
        error_log("Server error - retry may be needed");
    }
}

// Return 200 status code to confirm callback received
http_response_code(200);
echo json_encode(['status' => 'received']);

function downloadFile($url, $filename) {
    $downloadDir = 'downloads';
    if (!is_dir($downloadDir)) {
        mkdir($downloadDir, 0755, true);
    }
    
    $filepath = $downloadDir . '/' . $filename;
    
    $fileContent = file_get_contents($url);
    if ($fileContent === false) {
        throw new Exception("Failed to download file from URL");
    }
    
    $result = file_put_contents($filepath, $fileContent);
    if ($result === false) {
        throw new Exception("Failed to save file locally");
    }
}
?>
```

</TabItem>
</Tabs>

## Best Practices

:::tip Callback URL Configuration Recommendations

1. **Use HTTPS**: Ensure your callback URL uses HTTPS protocol for secure data transmission
2. **Verify Source**: Verify the legitimacy of the request source in callback processing
3. **Idempotent Processing**: The same task_id may receive multiple callbacks, ensure processing logic is idempotent
4. **Quick Response**: Callback processing should return a 200 status code as quickly as possible to avoid timeout
5. **Asynchronous Processing**: Complex business logic should be processed asynchronously to avoid blocking callback response
6. **Immediate Download**: Video URLs are valid for only 14 days, download and save files immediately upon success

:::

:::caution Important Reminders

- Callback URL must be a publicly accessible address
- Server must respond within 15 seconds, otherwise it will be considered a timeout
- If 3 consecutive retries fail, the system will stop sending callbacks
- **Video URLs expire after 14 days** - download immediately upon receiving callback
- Please ensure the stability of callback processing logic to avoid callback failures due to exceptions
- Handle both video_url and image_url fields for complete media management
- Pay attention to error messages for specific failure reasons (content moderation, format issues, quotas)

:::

## Troubleshooting

If you do not receive callback notifications, please check the following:


<AccordionGroup>
<Accordion title="Network Connection Issues">

- Confirm that the callback URL is accessible from the public network
- Check firewall settings to ensure inbound requests are not blocked
- Verify that domain name resolution is correct

</Accordion>
<Accordion title="Server Response Issues">

- Ensure the server returns HTTP 200 status code within 15 seconds
- Check server logs for error messages
- Verify that the interface path and HTTP method are correct

</Accordion>
<Accordion title="Content Format Issues">

- Confirm that the received POST request body is in JSON format
- Check that Content-Type is application/json
- Verify that JSON parsing is correct

</Accordion>
<Accordion title="Video Processing Issues">

- Confirm that video URLs are accessible
- Check video download permissions and network connections
- Verify video save paths and permissions
- **Note the 14-day URL expiration** - implement immediate download logic
- Handle both video and cover image downloads

</Accordion>
<Accordion title="Content Moderation Issues">

- Review error messages for content policy violations
- Adjust prompts if flagged by AI moderator
- Ensure uploaded images/videos meet content guidelines
- Check for inappropriate content detection messages

</Accordion>
</AccordionGroup>

## Alternative Solution

If you cannot use the callback mechanism, you can also use polling:

<Card
  title="Poll Query Results"
  icon="lucide-radar"
  href="/runway-api/get-ai-video-details"
>
  Use the get AI video details endpoint to regularly query task status. We recommend querying every 30 seconds.
</Card>