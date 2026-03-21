# Aleph Video Generation Callbacks

>Handle webhook notifications for Runway Alpeh video generation completion

## Overview

Callbacks provide an efficient way to receive notifications when your Runway Alpeh video generation tasks complete. Instead of repeatedly polling the API, your application can receive instant notifications via webhooks when videos are ready.

:::note[]
Callbacks are the recommended approach for production applications as they reduce API calls, improve response times, and provide immediate notification of task completion.
:::

## How Callbacks Work

### Workflow Steps

1. **Submit Generation Request**

   Include a `callBackUrl` parameter in your video generation request:

   ```json
   {
     "prompt": "Transform into a dreamy watercolor painting style with soft flowing movements",
     "videoUrl": "https://example.com/input-video.mp4",
     "callBackUrl": "https://your-app.com/webhook/aleph-callback"
   }
   ```

2. **Receive Task ID**

   The API immediately returns a task ID while processing begins:

   ```json
   {
     "code": 200,
     "msg": "success",
     "data": {
       "taskId": "ee603959-debb-48d1-98c4-a6d1c717eba6"
     }
   }
   ```

3. **Process Callback**

   When generation completes, our system sends a POST request to your callback URL with the results.

## Callback Payload

When video generation completes, you'll receive a POST request with the following payload:

### Success Callback

```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "result_video_url": "https://file.com/k/xxxxxxx.mp4",
    "result_image_url": "https://file.com/m/xxxxxxxx.png"
  },
  "taskId": "ee603959-debb-48d1-98c4-a6d1c717eba6"
}
```

### Parameter Description

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `code` | integer | Yes | Status code indicating the result |
| `msg` | string | Yes | Human-readable message describing the result |
| `data.result_video_url` | string | Yes | URL to access and download the generated video (valid for 14 days) |
| `data.result_image_url` | string | Yes | URL of a thumbnail image from the generated video |
| `taskId` | string | Yes | The original task ID from your generation request |

### Status Code Details

| Status Code | Description |
|-------------|-------------|
| 200 | Video generated successfully |
| 400 | Generation failed due to content policy or technical issues |

### Error Callback

```json
{
  "code": 400,
  "msg": "Your prompt was caught by our AI moderator. Please adjust it and try again!",
  "data": null,
  "taskId": "ee603959-debb-48d1-98c4-a6d1c717eba6"
}
```

## Implementing Callback Endpoints

Here are example implementations in popular programming languages:


<Tabs>
<TabItem value="javascript" label="Node.js/Express">

```javascript
const express = require('express');
const app = express();

// Middleware to parse JSON
app.use(express.json());

// Callback endpoint for Aleph video generation
app.post('/webhook/aleph-callback', (req, res) => {
  try {
    const { code, msg, data, taskId } = req.body;
    
    console.log(`Received callback for task: ${taskId}`);
    
    if (code === 200) {
      // Success - video generated
      console.log('Video generated successfully!');
      console.log('Video URL:', data.result_video_url);
      console.log('Thumbnail URL:', data.result_image_url);
      
      // Process the successful generation
      handleSuccessfulGeneration(taskId, data);
      
    } else {
      // Error occurred during generation
      console.error('Generation failed:', msg);
      
      // Handle the error
      handleGenerationError(taskId, msg);
    }
    
    // Always respond with 200 to acknowledge receipt
    res.status(200).json({ 
      code: 200, 
      msg: 'Callback received successfully' 
    });
    
  } catch (error) {
    console.error('Error processing callback:', error);
    res.status(500).json({ 
      code: 500, 
      msg: 'Error processing callback' 
    });
  }
});

async function handleSuccessfulGeneration(data) {
  try {
    // Update database with video information
    await updateTaskStatus(data.task_id, 'completed', {
      videoUrl: data.video_url,
      thumbnailUrl: data.image_url,
      videoId: data.video_id
    });
    
    // Optionally download and store the video
    await downloadAndStoreVideo(data.video_url, data.task_id);
    
    // Notify user or trigger next step in workflow
    await notifyUser(data.task_id, 'Video generation completed!');
    
  } catch (error) {
    console.error('Error handling successful generation:', error);
  }
}

async function handleGenerationError(taskId, errorMessage) {
  try {
    // Update database with error status
    await updateTaskStatus(taskId, 'failed', { error: errorMessage });
    
    // Notify user of the failure
    await notifyUser(taskId, `Video generation failed: ${errorMessage}`);
    
  } catch (error) {
    console.error('Error handling generation error:', error);
  }
}

app.listen(3000, () => {
  console.log('Webhook server listening on port 3000');
});
```

</TabItem>
<TabItem value="python" label="Python/Flask">

```python
from flask import Flask, request, jsonify
import logging
import requests
from datetime import datetime

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/webhook/aleph-callback', methods=['POST'])
def aleph_callback():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'code': 400, 'msg': 'Invalid JSON payload'}), 400
        
        code = data.get('code')
        msg = data.get('msg', '')
        callback_data = data.get('data', {})
        task_id = data.get('taskId')
        
        logging.info(f"Received callback for task: {task_id}")
        
        if code == 200:
            # Success - video generated
            video_url = callback_data.get('result_video_url')
            image_url = callback_data.get('result_image_url')
            
            logging.info(f"Video generated successfully: {video_url}")
            
            # Process successful generation
            handle_successful_generation(task_id, callback_data)
            
        else:
            # Error occurred during generation
            logging.error(f"Generation failed for task {task_id}: {msg}")
            handle_generation_error(task_id, msg)
        
        # Always return 200 to acknowledge receipt
        return jsonify({'code': 200, 'msg': 'Callback received successfully'})
        
    except Exception as e:
        logging.error(f"Error processing callback: {str(e)}")
        return jsonify({'code': 500, 'msg': 'Error processing callback'}), 500

def handle_successful_generation(task_id, data):
    """Handle successful video generation"""
    try:
        # Update database
        update_task_status(task_id, 'completed', {
            'video_url': data['result_video_url'],
            'image_url': data['result_image_url'],
            'completed_at': datetime.utcnow()
        })
        
        # Download video if needed
        # download_video(video_url, task_id)
        
        # Send notification
        notify_user(task_id, 'Your Aleph video is ready!')
        
    except Exception as e:
        logging.error(f"Error handling successful generation: {str(e)}")

def handle_generation_error(task_id, error_message):
    """Handle generation error"""
    try:
        # Update database
        update_task_status(task_id, 'failed', {
            'error_message': error_message,
            'failed_at': datetime.utcnow()
        })
        
        # Send error notification
        notify_user(task_id, f'Video generation failed: {error_message}')
        
    except Exception as e:
        logging.error(f"Error handling generation error: {str(e)}")

def update_task_status(task_id, status, additional_data=None):
    """Update task status in database"""
    # Implement your database update logic here
    logging.info(f"Updating task {task_id} status to {status}")

def notify_user(task_id, message):
    """Send notification to user"""
    # Implement your notification logic here
    logging.info(f"Notifying user for task {task_id}: {message}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
```

</TabItem>
<TabItem value="php" label="PHP">

```php
<?php
header('Content-Type: application/json');

// Enable error logging
error_reporting(E_ALL);
ini_set('log_errors', 1);
ini_set('error_log', 'callback_errors.log');

try {
    // Get JSON input
    $input = file_get_contents('php://input');
    $data = json_decode($input, true);
    
    if (!$data) {
        http_response_code(400);
        echo json_encode(['code' => 400, 'msg' => 'Invalid JSON payload']);
        exit;
    }
    
    $code = $data['code'] ?? null;
    $msg = $data['msg'] ?? '';
    $callbackData = $data['data'] ?? [];
    $taskId = $callbackData['task_id'] ?? null;
    
    error_log("Received callback for task: " . $taskId);
    
    if ($code === 200) {
        // Success - video generated
        $videoUrl = $callbackData['video_url'] ?? '';
        $imageUrl = $callbackData['image_url'] ?? '';
        $videoId = $callbackData['video_id'] ?? '';
        
        error_log("Video generated successfully: " . $videoUrl);
        
        handleSuccessfulGeneration($taskId, $videoUrl, $imageUrl, $videoId);
        
    } else {
        // Error occurred
        error_log("Generation failed for task $taskId: " . $msg);
        handleGenerationError($taskId, $msg);
    }
    
    // Always return 200 to acknowledge receipt
    http_response_code(200);
    echo json_encode(['code' => 200, 'msg' => 'Callback received successfully']);
    
} catch (Exception $e) {
    error_log("Error processing callback: " . $e->getMessage());
    http_response_code(500);
    echo json_encode(['code' => 500, 'msg' => 'Error processing callback']);
}

function handleSuccessfulGeneration($taskId, $videoUrl, $imageUrl, $videoId) {
    try {
        // Update database
        updateTaskStatus($taskId, 'completed', [
            'video_url' => $videoUrl,
            'image_url' => $imageUrl,
            'video_id' => $videoId,
            'completed_at' => date('Y-m-d H:i:s')
        ]);
        
        // Send notification
        notifyUser($taskId, 'Your Aleph video is ready!');
        
    } catch (Exception $e) {
        error_log("Error handling successful generation: " . $e->getMessage());
    }
}

function handleGenerationError($taskId, $errorMessage) {
    try {
        // Update database
        updateTaskStatus($taskId, 'failed', [
            'error_message' => $errorMessage,
            'failed_at' => date('Y-m-d H:i:s')
        ]);
        
        // Send notification
        notifyUser($taskId, "Video generation failed: $errorMessage");
        
    } catch (Exception $e) {
        error_log("Error handling generation error: " . $e->getMessage());
    }
}

function updateTaskStatus($taskId, $status, $additionalData = []) {
    // Implement your database update logic here
    error_log("Updating task $taskId status to $status");
    
    // Example using PDO:
    /*
    $pdo = new PDO($dsn, $username, $password);
    $stmt = $pdo->prepare("UPDATE tasks SET status = ?, updated_at = NOW() WHERE task_id = ?");
    $stmt->execute([$status, $taskId]);
    */
}

function notifyUser($taskId, $message) {
    // Implement your notification logic here
    error_log("Notifying user for task $taskId: $message");
    
    // Example: Send email, push notification, etc.
}
?>
```

</TabItem>
</Tabs>

## Security Best Practices


<AccordionGroup>
<Accordion title="Validate Callback Source">

**Verify Request Origin:**

- Check the `User-Agent` header for requests from kie.ai
- Consider implementing IP whitelist for additional security
- Validate the callback payload structure before processing

```javascript
// Example: Basic validation
app.post('/webhook/aleph-callback', (req, res) => {
  // Validate required fields
  const { code, data } = req.body;
  
  if (typeof code !== 'number' || !data || !data.task_id) {
    return res.status(400).json({ 
      code: 400, 
      msg: 'Invalid callback payload' 
    });
  }
  
  // Process valid callback
  // ...
});
```

</Accordion>
<Accordion title="Handle Duplicate Callbacks">

**Implement Idempotency:**

- Track processed task IDs to avoid duplicate processing
- Use database constraints or caching to prevent race conditions

```javascript
const processedTasks = new Set();

app.post('/webhook/aleph-callback', (req, res) => {
  const taskId = req.body.data?.task_id;
  
  if (processedTasks.has(taskId)) {
    console.log(`Task ${taskId} already processed, skipping`);
    return res.status(200).json({ code: 200, msg: 'Already processed' });
  }
  
  // Process callback
  processCallback(req.body);
  processedTasks.add(taskId);
  
  res.status(200).json({ code: 200, msg: 'Processed successfully' });
});
```

</Accordion>
<Accordion title="Error Handling and Retry Logic">

**Robust Error Handling:**

- Always return HTTP 200 for successful callback receipt
- Log errors for debugging but don't expose internal details
- Implement retry logic for critical operations

```javascript
app.post('/webhook/aleph-callback', async (req, res) => {
  try {
    await processCallbackWithRetry(req.body);
    res.status(200).json({ code: 200, msg: 'Success' });
  } catch (error) {
    // Log error but still return 200 to prevent retries
    console.error('Callback processing error:', error);
    res.status(200).json({ code: 200, msg: 'Received' });
  }
});

async function processCallbackWithRetry(data, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      await processCallback(data);
      return; // Success
    } catch (error) {
      if (attempt === maxRetries) throw error;
      
      const delay = Math.pow(2, attempt) * 1000; // Exponential backoff
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
}
```

</Accordion>
</AccordionGroup>

## Testing Callbacks

### Local Development

For local testing, use tools like ngrok to expose your local server:

```bash
# Install ngrok
npm install -g ngrok

# Expose local port 3000
ngrok http 3000

# Use the provided HTTPS URL as your callback URL
# Example: https://abc123.ngrok.io/webhook/aleph-callback
```

### Webhook Testing Tools

<CardGroup cols={2}>
  <Card
    title="Webhook.site"
    icon="globe"
    href="https://webhook.site"
  >
    Generate temporary URLs to test callback payloads
  </Card>

  <Card
    title="RequestBin"
    icon="inbox"
    href="https://requestbin.com"
  >
    Inspect and debug webhook requests
  </Card>
</CardGroup>

## Troubleshooting

<AccordionGroup>
<Accordion title="Callbacks Not Received">

**Common Issues:**

- Callback URL is not publicly accessible
- Server is returning non-200 status codes
- Firewall blocking incoming requests
- SSL certificate issues with HTTPS URLs

**Solutions:**

- Test your callback URL with tools like curl or Postman
- Ensure your server responds with HTTP 200 status
- Check server logs for incoming requests
- Verify SSL certificate is valid

</Accordion>
<Accordion title="Duplicate or Missing Callbacks">

**Callback Delivery:**

- Our system retries failed callbacks up to 3 times
- Callbacks are sent only once per task completion
- If your server is down, callbacks may be lost

**Best Practices:**

- Implement idempotency to handle potential duplicates
- Use polling as a backup for critical tasks
- Monitor callback receipt and alert on missing notifications

</Accordion>
<Accordion title="Callback Payload Issues">

**Data Validation:**

- Always validate the callback payload structure
- Handle missing or unexpected fields gracefully
- Log payload contents for debugging

```javascript
function validateCallback(payload) {
  const required = ['code', 'msg', 'data'];
  const missing = required.filter(field => !(field in payload));
  
  if (missing.length > 0) {
    throw new Error(`Missing required fields: ${missing.join(', ')}`);
  }
  
  if (payload.code === 200 && payload.data) {
    const dataRequired = ['task_id', 'video_url', 'image_url'];
    const dataMissing = dataRequired.filter(field => !(field in payload.data));
    
    if (dataMissing.length > 0) {
      throw new Error(`Missing data fields: ${dataMissing.join(', ')}`);
    }
  }
}
```

</Accordion>
</AccordionGroup>

## Related Documentation

<CardGroup cols={2}>
  <Card
    title="Generate Aleph Video"
    icon="lucide-video"
    href="/runway-api/generate-aleph-video"
  >
    Learn how to create video generation requests with callbacks
  </Card>

  <Card
    title="Get Task Details"
    icon="lucide-search"
    href="/runway-api/get-aleph-video-details"
  >
    Alternative polling method for checking task status
  </Card>
</CardGroup>

---

:::note Need Help
Contact our support team at [support@kie.ai](mailto:support@kie.ai) for assistance with callback implementation.
:::