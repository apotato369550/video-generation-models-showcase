# AI Video Extension Callbacks

>When you submit a video extension task to the Runway API, you can set a callback address through the `callBackUrl` parameter. After the task is completed, the system will automatically push the results to your specified address.

## Callback Mechanism Overview

:::note[]
The callback mechanism eliminates the need to poll the API for task status. The system proactively pushes task completion results to your server.
:::

### Callback Timing

The system sends callback notifications in the following situations:

- Video extension task successfully completed
- Video extension task failed
- Errors occurred during task processing

### Callback Method

- **HTTP Method**: POST
- **Content Type**: application/json
- **Timeout**: 15 seconds

## Callback Request Format

After task completion, the system will send a POST request to your `callBackUrl` in the following format:


<Tabs>
<TabItem value="success" label="Success Callback">

```json
{
  "code": 200,
  "msg": "All generated successfully.",
  "data": {
    "image_url": "https://file.com/m/xxxxxxxx.png",
    "task_id": "ee603959-debb-48d1-98c4-a6d1c717eba6",
    "video_id": "485da89c-7fca-4340-8c04-101025b2ae71",
    "video_url": "https://file.com/k/xxxxxxx.mp4"
  }
}
```

</TabItem>
<TabItem value="failure" label="Failure Callback">

```json
{
  "code": 400,
  "msg": "Get image info failed.",
  "data": {
    "task_id": "ee603959-debb-48d1-98c4-a6d1c717eba6"
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
| `data.video_id` | string | No | Video unique identifier (returned only on success) |
| `data.video_url` | string | No | Accessible video URL, valid for 14 days (returned only on success) |
| `data.image_url` | string | No | Cover image URL of the generated video (returned only on success) |

### Status Code Details

| Status Code | Description |
|-------------|-------------|
| 200 | Success - Request has been processed successfully |
| 400 | Client Error - Request parameters are incorrect or content is inappropriate |
| 500 | Server Error - An unexpected error occurred while processing the request |

### Common Error Messages

When code is 400, possible error messages include:

- Get image info failed
- Inappropriate content detected. Please replace the image or video
- Incorrect image format
- Please try again later. You can upgrade to Standard membership to start generating now
- Reached the limit for concurrent generations
- Unsupported width or height. Please adjust the size and try again
- Upload failed due to network reasons, please re-enter
- Your prompt was caught by our AI moderator. Please adjust it and try again!
- Your prompt/negative prompt cannot exceed 2048 characters. Please check if your input is too long
- Your video creation prompt contains NSFW content, which isn't allowed under our policy. Kindly revise your prompt and generate again

## Callback Reception Examples

Here are example codes for receiving callbacks in popular programming languages:

<Tabs>
<TabItem value="javascript" label="Node.js">

```javascript
const express = require('express');
const fs = require('fs');
const https = require('https');
const app = express();

app.use(express.json());

app.post('/runway-extend-callback', (req, res) => {
  const { code, msg, data } = req.body;
  
  console.log('Received Runway video extension callback:', {
    taskId: data.task_id,
    status: code,
    message: msg
  });
  
  if (code === 200) {
    // Video extension successful
    const { task_id, video_id, video_url, image_url } = data;
    
    console.log('Video extension successful!');
    console.log(`Task ID: ${task_id}`);
    console.log(`Video ID: ${video_id}`);
    console.log(`Video URL: ${video_url}`);
    console.log(`Cover URL: ${image_url}`);
    
    // Download video file
    if (video_url) {
      downloadFile(video_url, `runway_extend_${task_id}.mp4`)
        .then(() => console.log('Video download successful'))
        .catch(err => console.error('Video download failed:', err));
    }
    
    // Download cover image
    if (image_url) {
      downloadFile(image_url, `runway_extend_cover_${task_id}.png`)
        .then(() => console.log('Cover download successful'))
        .catch(err => console.error('Cover download failed:', err));
    }
    
  } else {
    // Video extension failed
    console.log('Runway video extension failed:', msg);
    
    // Handle specific error types
    if (code === 400) {
      console.log('Client error - Check input parameters and content');
    } else if (code === 500) {
      console.log('Server error - Please try again later');
    }
  }
  
  // Return 200 status code to confirm callback received
  res.status(200).json({ code: 200, msg: 'success' });
});

// Helper function: Download file
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

@app.route('/runway-extend-callback', methods=['POST'])
def handle_callback():
    data = request.json
    
    code = data.get('code')
    msg = data.get('msg')
    callback_data = data.get('data', {})
    task_id = callback_data.get('task_id')
    
    print(f"Received Runway video extension callback:")
    print(f"Task ID: {task_id}")
    print(f"Status: {code}, Message: {msg}")
    
    if code == 200:
        # Video extension successful
        video_id = callback_data.get('video_id')
        video_url = callback_data.get('video_url')
        image_url = callback_data.get('image_url')
        
        print("Video extension successful!")
        print(f"Video ID: {video_id}")
        print(f"Video URL: {video_url}")
        print(f"Cover URL: {image_url}")
        
        # Download video file
        if video_url:
            try:
                video_filename = f"runway_extend_{task_id}.mp4"
                download_file(video_url, video_filename)
                print("Video download successful")
            except Exception as e:
                print(f"Video download failed: {e}")
        
        # Download cover image
        if image_url:
            try:
                image_filename = f"runway_extend_cover_{task_id}.png"
                download_file(image_url, image_filename)
                print("Cover download successful")
            except Exception as e:
                print(f"Cover download failed: {e}")
                
    else:
        # Video extension failed
        print(f"Runway video extension failed: {msg}")
        
        # Handle specific error types
        if code == 400:
            print("Client error - Check input parameters and content")
            if 'Inappropriate content' in msg:
                print("Content moderation failed - Please replace image or video")
            elif 'Incorrect image format' in msg:
                print("Format error - Please check image format")
            elif 'concurrent generations' in msg:
                print("Concurrency limit - Please wait or upgrade membership")
            elif 'NSFW content' in msg:
                print("Content violation - Please modify prompt")
        elif code == 500:
            print("Server error - Please try again later")
    
    # Return 200 status code to confirm callback received
    return jsonify({'code': 200, 'msg': 'success'}), 200

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

error_log("Received Runway video extension callback:");
error_log("Task ID: $taskId");
error_log("Status: $code, Message: $msg");

if ($code === 200) {
    // Video extension successful
    $videoId = $callbackData['video_id'] ?? '';
    $videoUrl = $callbackData['video_url'] ?? '';
    $imageUrl = $callbackData['image_url'] ?? '';
    
    error_log("Video extension successful!");
    error_log("Video ID: $videoId");
    error_log("Video URL: $videoUrl");
    error_log("Cover URL: $imageUrl");
    
    // Download video file
    if (!empty($videoUrl)) {
        try {
            $videoFilename = "runway_extend_{$taskId}.mp4";
            downloadFile($videoUrl, $videoFilename);
            error_log("Video download successful");
        } catch (Exception $e) {
            error_log("Video download failed: " . $e->getMessage());
        }
    }
    
    // Download cover image
    if (!empty($imageUrl)) {
        try {
            $imageFilename = "runway_extend_cover_{$taskId}.png";
            downloadFile($imageUrl, $imageFilename);
            error_log("Cover download successful");
        } catch (Exception $e) {
            error_log("Cover download failed: " . $e->getMessage());
        }
    }
    
} else {
    // Video extension failed
    error_log("Runway video extension failed: $msg");
    
    // Handle specific error types
    if ($code === 400) {
        error_log("Client error - Check input parameters and content");
        if (strpos($msg, 'Inappropriate content') !== false) {
            error_log("Content moderation failed - Please replace image or video");
        } elseif (strpos($msg, 'Incorrect image format') !== false) {
            error_log("Format error - Please check image format");
        } elseif (strpos($msg, 'concurrent generations') !== false) {
            error_log("Concurrency limit - Please wait or upgrade membership");
        } elseif (strpos($msg, 'NSFW content') !== false) {
            error_log("Content violation - Please modify prompt");
        }
    } elseif ($code === 500) {
        error_log("Server error - Please try again later");
    }
}

// Return 200 status code to confirm callback received
http_response_code(200);
echo json_encode(['code' => 200, 'msg' => 'success']);

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

1. **Use HTTPS**: Ensure callback URL uses HTTPS protocol for secure data transmission
2. **Verify Source**: Verify the legitimacy of the request source in callback processing
3. **Idempotent Processing**: The same task_id may receive multiple callbacks, ensure processing logic is idempotent
4. **Quick Response**: Callback processing should return 200 status code promptly to avoid timeout
5. **Asynchronous Processing**: Complex business logic should be processed asynchronously to avoid blocking callback response
6. **Timely Download**: Video URLs are valid for only 14 days, please download and save promptly
7. **Extension Management**: Properly manage extended video files and cover images

:::

:::caution Important Reminders

- Callback URL must be publicly accessible
- Server must respond within 15 seconds, otherwise it will be considered timeout
- After 3 consecutive retry failures, the system will stop sending callbacks
- **Video URLs are valid for only 14 days**, please download and save to your storage system promptly
- Ensure the stability of callback processing logic to avoid callback failures due to exceptions
- Properly handle content moderation errors to ensure input content complies with platform policies
- Extended videos are usually longer than original videos
- Pay attention to concurrent generation limits to avoid submitting too many tasks simultaneously

:::

## Troubleshooting

If you don't receive callback notifications, please check the following:

<AccordionGroup>
<Accordion title="Network Connection Issues">

- Confirm that the callback URL is accessible from the public internet
- Check firewall settings to ensure inbound requests are not blocked
- Verify domain name resolution is correct

</Accordion>
<Accordion title="Server Response Issues">

- Ensure server returns HTTP 200 status code within 15 seconds
- Check server logs for error messages
- Verify interface path and HTTP method are correct

</Accordion>
<Accordion title="Content Format Issues">

- Confirm that the received POST request body is in JSON format
- Check if Content-Type is application/json
- Verify JSON parsing is correct

</Accordion>
<Accordion title="Video Processing Issues">

- Confirm that video URL is accessible
- Check video download permissions and network connection
- Verify video save path and permissions
- Note the 14-day validity period limitation of video URLs
- Backup videos to long-term storage system promptly

</Accordion>
<Accordion title="Content Moderation Issues">

- Review content moderation error messages
- Ensure input images or videos do not contain inappropriate content
- Check if prompts comply with platform policies
- Avoid using NSFW-related descriptive words
- Ensure image format is correct and dimensions are appropriate

</Accordion>
<Accordion title="Concurrency Limit Issues">

- Monitor current concurrent task count
- Implement appropriate task queue mechanism
- Consider upgrading to Standard membership for higher concurrency limits
- Reasonably schedule task submission times

</Accordion>
<Accordion title="Extension Quality Issues">

- Check coherence of extended videos
- Verify if video duration meets expectations
- Evaluate quality and style consistency of extended portions
- Ensure extended videos transition naturally

</Accordion>
</AccordionGroup>

## Extension-Specific Considerations

:::note AI Video Extension Features

AI video extension functionality continues generation based on existing videos with the following characteristics:

1. **Duration Increase**: Extended videos will be longer than original videos
2. **Style Continuation**: The system tries to maintain the visual style and motion patterns of the original video
3. **Smooth Transition**: Extended portions will naturally connect with the original video
4. **Quality Preservation**: Extended video quality should be comparable to the original video
5. **Motion Coherence**: Object movement and scene changes will maintain logical coherence
6. **URL Validity**: Generated video URLs are valid for only 14 days

:::

## Alternative Approach

If you cannot use the callback mechanism, you can also use polling:


<Card
  title="Poll Query Results"
  icon="lucide-radar"
  href="/runway-api/get-ai-video-details"
>
  Use the Get AI Video Details interface to periodically query task status, recommended every 30 seconds.
</Card>