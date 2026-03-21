# Runway API Quickstart

> Start generating stunning AI videos with the Runway API in minutes

## Welcome to the Runway API

The Runway API gives you access to the powerful capabilities of Runway's advanced AI models to generate high-quality AI videos. Whether you're building applications, automating workflows, or creating dynamic content, our API provides simple and reliable access to AI video generation.

<CardGroup cols={2}>
  <Card title="Text-to-Video" icon="lucide-video" href="/runway-api/generate-ai-video">
    Transform text prompts into dynamic video content
  </Card>

  <Card title="Image-to-Video" icon="lucide-play" href="/runway-api/generate-ai-video">
    Animate existing images into engaging videos
  </Card>

  <Card title="Video Extension" icon="lucide-plus" href="/runway-api/extend-ai-video">
    Extend videos to create longer sequences
  </Card>

  <Card title="Task Management" icon="lucide-list-checks" href="/runway-api/get-ai-video-details">
    Track and monitor your video generation tasks
  </Card>
</CardGroup>

## Authentication

All API requests require authentication using a Bearer token. Please obtain your API key from the [API Key Management page](https://kie.ai/api-key).

:::warning[]
Please keep your API key secure and never share it publicly. If you suspect your key has been compromised, reset it immediately.
:::

### API Base URL

```
https://api.kie.ai
```

### Authentication Header

```http
Authorization: Bearer YOUR_API_KEY
```

## Quick Start Guide

### Step 1: Generate Your First Video

Start with a simple text-to-video generation request:

<Tabs groupId="programming-language">
  <TabItem value="javascript" label="Node.js">
    ```javascript
    async function generateVideo() {
      try {
        const response = await fetch('https://api.kie.ai/api/v1/runway/generate', {
          method: 'POST',
          headers: {
            'Authorization': 'Bearer YOUR_API_KEY',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            prompt: 'A fluffy orange kitten dancing energetically in a colorful room with disco lights',
            duration: 5,
            quality: '720p',
            aspectRatio: '16:9',
            waterMark: ''
          })
        });
        
        const data = await response.json();
        
        if (response.ok && data.code === 200) {
          console.log('Task submitted:', data);
          console.log('Task ID:', data.data.taskId);
          return data.data.taskId;
        } else {
          console.error('Request failed:', data.msg || 'Unknown error');
          return null;
        }
      } catch (error) {
        console.error('Error:', error.message);
        return null;
      }
    }

    generateVideo();
    ```
  </TabItem>

  <TabItem value="python" label="Python">
    ```python
    import requests

    def generate_video():
        url = "https://api.kie.ai/api/v1/runway/generate"
        headers = {
            "Authorization": "Bearer YOUR_API_KEY",
            "Content-Type": "application/json"
        }
        
        payload = {
            "prompt": "A fluffy orange kitten dancing energetically in a colorful room with disco lights",
            "duration": 5,
            "quality": "720p",
            "aspectRatio": "16:9",
            "waterMark": ""
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            result = response.json()
            
            if response.ok and result.get('code') == 200:
                print(f"Task submitted: {result}")
                print(f"Task ID: {result['data']['taskId']}")
                return result['data']['taskId']
            else:
                print(f"Request failed: {result.get('msg', 'Unknown error')}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    generate_video()
    ```
  </TabItem>

  <TabItem value="curl" label="cURL">
    ```bash
    curl -X POST "https://api.kie.ai/api/v1/runway/generate" \
      -H "Authorization: Bearer YOUR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "prompt": "A fluffy orange kitten dancing energetically in a colorful room with disco lights",
        "duration": 5,
        "quality": "720p",
        "aspectRatio": "16:9",
        "waterMark": ""
      }'
    ```
  </TabItem>
</Tabs>

### Step 2: Check Task Status

Use the returned task ID to check generation status:

<Tabs groupId="programming-language">
  <TabItem value="javascript" label="Node.js">
    ```javascript
    async function checkTaskStatus(taskId) {
      try {
        const response = await fetch(`https://api.kie.ai/api/v1/runway/record-detail?taskId=${taskId}`, {
          method: 'GET',
          headers: {
            'Authorization': 'Bearer YOUR_API_KEY'
          }
        });
        
        const result = await response.json();
        
        if (response.ok && result.code === 200) {
          const taskData = result.data;
          
          switch (taskData.state) {
            case 'wait':
              console.log('Task waiting...');
              console.log('Creation time:', taskData.generateTime);
              return taskData;
              
            case 'queueing':
              console.log('Task queuing...');
              console.log('Creation time:', taskData.generateTime);
              return taskData;
              
            case 'generating':
              console.log('Task generating...');
              console.log('Creation time:', taskData.generateTime);
              return taskData;
              
            case 'success':
              console.log('Task generation successful!');
              console.log('Video URL:', taskData.videoInfo.videoUrl);
              console.log('Thumbnail URL:', taskData.videoInfo.imageUrl);
              console.log('Generation time:', taskData.generateTime);
              console.log('Expiration status:', taskData.expireFlag === 0 ? 'Valid' : 'Expired');
              return taskData;
              
            case 'fail':
              console.log('Task generation failed');
              if (taskData.failMsg) {
                console.error('Failure reason:', taskData.failMsg);
              }
              console.log('Generation time:', taskData.generateTime);
              return taskData;
              
            default:
              console.log('Unknown status:', taskData.state);
              if (taskData.failMsg) {
                console.error('Error message:', taskData.failMsg);
              }
              return taskData;
          }
        } else {
          console.error('Query failed:', result.msg || 'Unknown error');
          return null;
        }
      } catch (error) {
        console.error('Failed to query status:', error.message);
        return null;
      }
    }

    // How to use
    const status = await checkTaskStatus('YOUR_TASK_ID');
    ```
  </TabItem>

  <TabItem value="python" label="Python">
    ```python
    import requests
    import time

    def check_task_status(task_id, api_key):
        url = f"https://api.kie.ai/api/v1/runway/record-detail?taskId={task_id}"
        headers = {"Authorization": f"Bearer {api_key}"}
        
        try:
            response = requests.get(url, headers=headers)
            result = response.json()
            
            if response.ok and result.get('code') == 200:
                task_data = result['data']
                state = task_data['state']
                
                if state == 'wait':
                    print("Task waiting...")
                    print(f"Creation time: {task_data.get('generateTime', '')}")
                    return task_data
                elif state == 'queueing':
                    print("Task queuing...")
                    print(f"Creation time: {task_data.get('generateTime', '')}")
                    return task_data
                elif state == 'generating':
                    print("Task generating...")
                    print(f"Creation time: {task_data.get('generateTime', '')}")
                    return task_data
                elif state == 'success':
                    print("Task generation successful!")
                    video_info = task_data.get('videoInfo', {})
                    print(f"Video URL: {video_info.get('videoUrl', '')}")
                    print(f"Thumbnail URL: {video_info.get('imageUrl', '')}")
                    print(f"Generation time: {task_data.get('generateTime', '')}")
                    expire_flag = task_data.get('expireFlag', 0)
                    print(f"Expiration status: {'Valid' if expire_flag == 0 else 'Expired'}")
                    return task_data
                elif state == 'fail':
                    print("Task generation failed")
                    if task_data.get('failMsg'):
                        print(f"Failure reason: {task_data['failMsg']}")
                    print(f"Generation time: {task_data.get('generateTime', '')}")
                    return task_data
                else:
                    print(f"Unknown status: {state}")
                    if task_data.get('failMsg'):
                        print(f"Error message: {task_data['failMsg']}")
                    return task_data
            else:
                print(f"Query failed: {result.get('msg', 'Unknown error')}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Failed to query status: {e}")
            return None

    # Poll until completion
    def wait_for_completion(task_id, api_key):
        while True:
            result = check_task_status(task_id, api_key)
            if result and result.get('state') in ['success', 'fail']:  # Final states
                return result
            time.sleep(30)  # Wait 30 seconds before checking again
    ```
  </TabItem>

  <TabItem value="curl" label="cURL">
    ```bash
    curl -X GET "https://api.kie.ai/api/v1/runway/record-detail?taskId=YOUR_TASK_ID" \
      -H "Authorization: Bearer YOUR_API_KEY"
    ```
  </TabItem>
</Tabs>

### Response Format

**Success Response:**

```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "taskId": "ee603959-debb-48d1-98c4-a6d1c717eba6"
  }
}
```

**Task Status Response:**

```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "taskId": "ee603959-debb-48d1-98c4-a6d1c717eba6",
    "state": "success",
    "generateTime": "2023-08-15 14:30:45",
    "videoInfo": {
      "videoId": "485da89c-7fca-4340-8c04-101025b2ae71",
      "videoUrl": "https://file.com/k/xxxxxxx.mp4",
      "imageUrl": "https://file.com/m/xxxxxxxx.png"
    },
    "expireFlag": 0
  }
}
```

## Generation Types

<Tabs>
  <TabItem value="text-to-video" label="Text-to-Video">
    Generate video from text description:

    ```json
    {
      "prompt": "A majestic eagle soaring through mountain clouds at sunset",
      "duration": 5,
      "quality": "720p",
      "aspectRatio": "16:9"
    }
    ```
  </TabItem>

  <TabItem value="image-to-video" label="Image-to-Video">
    Animate existing images with text prompts:

    ```json
    {
      "prompt": "The character starts walking forward confidently",
      "imageUrl": "https://example.com/character-image.jpg",
      "duration": 5,
      "quality": "720p",
      "aspectRatio": "16:9"
    }
    ```
  </TabItem>

  <TabItem value="extend-video" label="Video Extension">
    Extend existing video to create longer sequences:

    ```json
    {
      "taskId": "ee603959-debb-48d1-98c4-a6d1c717eba6",
      "prompt": "The kitten continues dancing even more energetically and spinning",
      "quality": "720p"
    }
    ```
  </TabItem>
</Tabs>

## Video Quality Options

Choose the right quality for your needs:

<CardGroup cols={2}>
  <Card title="720p HD" icon="lucide-video">
    **Standard Quality**

    Balanced file size and quality, suitable for most applications

    Compatible with both 5s and 10s durations
  </Card>

  <Card title="1080p Full HD" icon="lucide-video">
    **Premium Quality**

    Higher resolution for professional content

    Only available for 5-second videos
  </Card>
</CardGroup>

## Key Parameters

#### `prompt` (string, required)
Text description of the desired video content. Be specific about actions, movements, and visual style.

**Tips for better prompts:**

* Describe specific actions and movements (e.g., "walking slowly", "spinning quickly")
* Include visual style descriptors (e.g., "cinematic", "animated", "realistic")
* Specify camera angles when relevant (e.g., "close-up", "wide shot", "tracking shot")
* Add lighting and atmosphere details (e.g., "golden hour lighting", "dramatic shadows")

#### `duration` (number, required)
Video duration in seconds. Options:

* `5` - 5-second video (compatible with 720p and 1080p)
* `10` - 10-second video (compatible only with 720p)

#### `quality` (string, required)
Video resolution quality:

* `720p` - High definition quality, compatible with all durations
* `1080p` - Full high definition quality, only for 5-second videos

#### `aspectRatio` (string, required)
Video aspect ratio. Options:

* `16:9` - Widescreen (recommended for landscape content)
* `9:16` - Vertical (perfect for mobile and social media)
* `1:1` - Square (social media posts)
* `4:3` - Traditional format
* `3:4` - Portrait orientation

#### `imageUrl` (string)
Optional reference image URL to animate. When provided, the AI will create a video based on this image.

#### `waterMark` (string)
Optional watermark text. Leave empty for no watermark, or provide text to display in the bottom right corner.

## Complete Workflow Example

Here's a complete example of generating a video and waiting for completion:

<Tabs groupId="programming-language">
  <TabItem value="javascript" label="JavaScript">
    ```javascript
    class RunwayAPI {
      constructor(apiKey) {
        this.apiKey = apiKey;
        this.baseUrl = 'https://api.kie.ai/api/v1/runway';
      }
      
      async generateVideo(options) {
        const response = await fetch(`${this.baseUrl}/generate`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${this.apiKey}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(options)
        });
        
        const result = await response.json();
        if (!response.ok || result.code !== 200) {
          throw new Error(`Generation failed: ${result.msg || 'Unknown error'}`);
        }
        
        return result.data.taskId;
      }
      
      async waitForCompletion(taskId, maxWaitTime = 600000) { // Maximum wait 10 minutes
        const startTime = Date.now();
        
        while (Date.now() - startTime < maxWaitTime) {
          const status = await this.getTaskStatus(taskId);
          
          switch (status.state) {
            case 'wait':
              console.log('Task waiting, continue waiting...');
              break;
              
            case 'queueing':
              console.log('Task queuing, continue waiting...');
              break;
              
            case 'generating':
              console.log('Task generating, continue waiting...');
              break;
              
            case 'success':
              console.log('Generation completed successfully!');
              return status;
              
            case 'fail':
              const error = status.failMsg || 'Task generation failed';
              console.error('Task generation failed:', error);
              throw new Error(error);
              
            default:
              console.log(`Unknown status: ${status.state}`);
              if (status.failMsg) {
                console.error('Error message:', status.failMsg);
              }
              break;
          }
          
          // Wait 30 seconds before checking again
          await new Promise(resolve => setTimeout(resolve, 30000));
        }
        
        throw new Error('Generation timeout');
      }
      
      async getTaskStatus(taskId) {
        const response = await fetch(`${this.baseUrl}/record-detail?taskId=${taskId}`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${this.apiKey}`
          }
        });
        
        const result = await response.json();
        if (!response.ok || result.code !== 200) {
          throw new Error(`Failed to query status: ${result.msg || 'Unknown error'}`);
        }
        
        return result.data;
      }
      
      async extendVideo(taskId, prompt, quality = '720p') {
        const response = await fetch(`${this.baseUrl}/extend`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${this.apiKey}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            taskId,
            prompt,
            quality
          })
        });
        
        const result = await response.json();
        if (!response.ok || result.code !== 200) {
          throw new Error(`Extension failed: ${result.msg || 'Unknown error'}`);
        }
        
        return result.data.taskId;
      }
    }

    // Usage Example
    async function main() {
      const api = new RunwayAPI('YOUR_API_KEY');
      
      try {
        // Text-to-video generation
        console.log('Starting video generation...');
        const taskId = await api.generateVideo({
          prompt: 'A fluffy orange kitten dancing energetically in a colorful room with disco lights',
          duration: 5,
          quality: '720p',
          aspectRatio: '16:9',
          waterMark: ''
        });
        
        // Wait for completion
        console.log(`Task ID: ${taskId}. Waiting for completion...`);
        const result = await api.waitForCompletion(taskId);
        
        console.log('Video generation successful!');
        console.log('Video URL:', result.videoInfo.videoUrl);
        console.log('Thumbnail URL:', result.videoInfo.imageUrl);
        
        // Extend video
        console.log('\nStarting video extension...');
        const extendTaskId = await api.extendVideo(taskId, 'The kitten spins, with increasing energy and excitement', '720p');
        
        const extendResult = await api.waitForCompletion(extendTaskId);
        console.log('Video extension successful!');
        console.log('Extended video URL:', extendResult.videoInfo.videoUrl);
        
      } catch (error) {
        console.error('Error:', error.message);
      }
    }

    main();
    ```
  </TabItem>

  <TabItem value="python" label="Python">
    ```python
    import requests
    import time

    class RunwayAPI:
        def __init__(self, api_key):
            self.api_key = api_key
            self.base_url = 'https://api.kie.ai/api/v1/runway'
            self.headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
        
        def generate_video(self, **options):
            response = requests.post(f'{self.base_url}/generate', 
                                   headers=self.headers, json=options)
            result = response.json()
            
            if not response.ok or result.get('code') != 200:
                raise Exception(f"Generation failed: {result.get('msg', 'Unknown error')}")
            
            return result['data']['taskId']
        
        def wait_for_completion(self, task_id, max_wait_time=600):
            start_time = time.time()
            
            while time.time() - start_time < max_wait_time:
                status = self.get_task_status(task_id)
                state = status['state']
                
                if state == 'wait':
                    print("Task waiting, continue waiting...")
                elif state == 'queueing':
                    print("Task queuing, continue waiting...")
                elif state == 'generating':
                    print("Task generating, continue waiting...")
                elif state == 'success':
                    print("Generation completed successfully!")
                    return status
                elif state == 'fail':
                    error = status.get('failMsg', 'Task generation failed')
                    print(f"Task generation failed: {error}")
                    raise Exception(error)
                else:
                    print(f"Unknown status: {state}")
                    if status.get('failMsg'):
                        print(f"Error message: {status['failMsg']}")
                
                time.sleep(30)  # Wait 30 seconds
            
            raise Exception('Generation timeout')
        
        def get_task_status(self, task_id):
            response = requests.get(f'{self.base_url}/record-detail?taskId={task_id}',
                                  headers={'Authorization': f'Bearer {self.api_key}'})
            result = response.json()
            
            if not response.ok or result.get('code') != 200:
                raise Exception(f"Failed to query status: {result.get('msg', 'Unknown error')}")
            
            return result['data']
        
        def extend_video(self, task_id, prompt, quality='720p'):
            data = {
                'taskId': task_id,
                'prompt': prompt,
                'quality': quality
            }
            
            response = requests.post(f'{self.base_url}/extend', 
                                   headers=self.headers, json=data)
            result = response.json()
            
            if not response.ok or result.get('code') != 200:
                raise Exception(f"Extension failed: {result.get('msg', 'Unknown error')}")
            
            return result['data']['taskId']

    # Usage Example
    def main():
        api = RunwayAPI('YOUR_API_KEY')
        
        try:
            # Text-to-video generation
            print('Starting video generation...')
            task_id = api.generate_video(
                prompt='A fluffy orange kitten dancing energetically in a colorful room with disco lights',
                duration=5,
                quality='720p',
                aspectRatio='16:9',
                waterMark=''
            )
            
            # Wait for completion
            print(f'Task ID: {task_id}. Waiting for completion...')
            result = api.wait_for_completion(task_id)
            
            print('Video generation successful!')
            print(f'Video URL: {result["videoInfo"]["videoUrl"]}')
            print(f'Thumbnail URL: {result["videoInfo"]["imageUrl"]}')
            
            # Extend video
            print('\nStarting video extension...')
            extend_task_id = api.extend_video(task_id, 'The kitten spins, with increasing energy and excitement', '720p')
            
            extend_result = api.wait_for_completion(extend_task_id)
            print('Video extension successful!')
            print(f'Extended video URL: {extend_result["videoInfo"]["videoUrl"]}')
            
        except Exception as error:
            print(f'Error: {error}')

    if __name__ == '__main__':
        main()
    ```
  </TabItem>
</Tabs>

## Asynchronous Processing with Callbacks

For production applications, use callbacks instead of polling:

```json
{
  "prompt": "A peaceful garden with cherry blossoms swaying in a gentle breeze",
  "duration": 5,
  "quality": "720p",
  "aspectRatio": "16:9",
  "callBackUrl": "https://your-app.com/webhook/runway-callback"
}
```

When generation completes, the system will POST the results to your callback URL.

<Card title="Learn more about callbacks" icon="lucide-webhook" href="/runway-api/generate-ai-video-callbacks">
  Complete guide to implementing and handling Runway API callbacks
</Card>

## Video Extension Workflow

Create longer video sequences by extending existing videos:

1. **Generate initial video**: Create a base video using text or image input
2. **Check completion status**: Wait for initial video to complete successfully
3. **Extend video**: Create an extension using the original task ID
4. **Chain extensions**: Repeat this process to create longer sequences

```javascript
// Step 1: Generate initial video
const initialResponse = await generateVideo({
  prompt: "A cat starts dancing in a colorful room",
  duration: 5,
  quality: "720p",
  aspectRatio: "16:9"
});

// Step 2: Wait for completion and extend
const extendResponse = await extendVideo({
  taskId: initialResponse.data.taskId,
  prompt: "The kitten spins, with increasing energy and excitement",
  quality: "720p"
});
```

## Best Practices

<details>
  <summary>Video Prompt Engineering</summary>
  * Focus on actions and movements rather than static descriptions
  * Include temporal elements (e.g., "gradually", "suddenly", "slowly")
  * Describe camera movement when relevant (e.g., "zooming in", "panning left")
  * Maintain consistency in subject and style across extensions
</details>

<details>
  <summary>Performance Optimization</summary>
  * Use callbacks instead of frequent polling
  * Implement proper error handling and retry logic
  * Consider trade-offs between video duration and quality
  * Cache results and implement efficient storage solutions
</details>

<details>
  <summary>Quality and Duration Selection</summary>
  * Choose 720p for longer videos (10s) or when file size matters
  * Use 1080p for high-quality short videos (5s only)
  * Consider requirements of target platforms (social media, web, etc.)
  * Test different combinations to find the optimal setup for your use case
</details>

<details>
  <summary>Error Handling</summary>
  * Always check response status codes
  * Implement exponential backoff for retries
  * Handle rate limiting gracefully
  * Monitor task status and handle failures appropriately
</details>

## Status Codes

#### `200` (Success)
Task creation successful or request completed

#### `400` (Bad Request)
Invalid request parameters or malformed JSON

#### `401` (Unauthorized)
Missing or invalid API key

#### `402` (Insufficient Credits)
Account doesn't have enough credits for the operation

#### `422` (Validation Error)
Request parameters failed validation checks

#### `429` (Rate Limited)
Too many requests - implement backoff strategy

#### `500` (Server Error)
Internal server error - contact support if persistent

## Task Status Explanation

#### `state: wait` (Waiting)
Task created, waiting to be processed

#### `state: queueing` (Queueing)
Task queued and waiting to be processed

#### `state: generating` (Generating)
Task currently being processed

#### `state: success` (Success)
Task completed successfully

#### `state: fail` (Failed)
Task generation failed

## Video Storage and Expiration

:::warning[]
Generated videos are stored for **14 days** before automatic deletion. Please download and save your videos within this timeframe.
:::

* Video URLs remain accessible for 14 days after generation
* `expireFlag` in the response indicates if video is expired (0 = active, 1 = expired)
* Plan your workflow to download or process videos before expiration
* Consider implementing automatic download systems for production use

## Next Steps

<CardGroup cols={2}>
  <Card title="Generate Video" icon="lucide-video" href="/runway-api/generate-ai-video">
    Complete API reference for video generation
  </Card>

  <Card title="Extend Video" icon="lucide-plus" href="/runway-api/extend-ai-video">
    Learn how to extend videos to create longer sequences
  </Card>

  <Card title="Callback Setup" icon="lucide-webhook" href="/runway-api/generate-ai-video-callbacks">
    Implement webhooks for asynchronous processing
  </Card>

  <Card title="Task Details" icon="lucide-search" href="/runway-api/get-ai-video-details">
    Query and monitor task status
  </Card>
</CardGroup>

## Support

:::info[]
Need help? Our technical support team is here for you.

* **Email**: [support@kie.ai](mailto:support@kie.ai)
* **Documentation**: [docs.kie.ai](https://docs.kie.ai)
* **API Status**: Check our status page for real-time API health
:::

***

Ready to start generating amazing AI videos? [Get your API key](https://kie.ai/api-key) and start creating today!