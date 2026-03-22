# File Upload API Quickstart

> Start using the File Upload API in minutes with multiple upload methods

## Welcome to the File Upload API

The File Upload API provides flexible and efficient file upload services with multiple upload methods to meet various business needs. Whether it's remote file migration, large file transfers, or quick small file uploads, our API offers the best solutions for you.

<CardGroup cols={3}>
  <Card title="Base64 Upload" icon="lucide-code" href="/file-upload-api/upload-file-base-64">
    Base64 encoded file upload, suitable for small files
  </Card>

  <Card title="File Stream Upload" icon="lucide-upload" href="/file-upload-api/upload-file-stream">
    Efficient binary file stream upload, suitable for large files
  </Card>

  <Card title="URL File Upload" icon="lucide-link" href="/file-upload-api/upload-file-url">
    Automatically download and upload files from remote URLs
  </Card>
</CardGroup>

:::info[**File uploads are free**]
Uploading files to our service incurs no charges. You can upload files confidently without worrying about upload costs or fees.
:::

:::warning[**Important Reminder**]
Uploaded files are temporary and will be automatically deleted after **3 days**. Please download or migrate important files promptly.
:::

## Authentication

All API requests require authentication using a Bearer token. Please obtain your API key from the [API Key Management page](https://kie.ai/api-key).

:::warning[]
Please keep your API key secure and never share it publicly. If you suspect your key has been compromised, reset it immediately.
:::

### API Base URL

```
https://kieai.redpandaai.co
```

### Authentication Header

```http
Authorization: Bearer YOUR_API_KEY
```

## Quick Start Guide

### Step 1: Choose Upload Method

Select the appropriate upload method based on your needs:

<Tabs>
  <TabItem value="url-upload" label="URL File Upload">
    Suitable for downloading and uploading files from remote servers:

    <Tabs groupId="programming-language">
      <TabItem value="bash" label="cURL">
        ```bash
        curl -X POST "https://kieai.redpandaai.co/api/file-url-upload" \
          -H "Authorization: Bearer YOUR_API_KEY" \
          -H "Content-Type: application/json" \
          -d '{
            "fileUrl": "https://example.com/sample-image.jpg",
            "uploadPath": "images",
            "fileName": "my-image.jpg"
          }'
        ```
      </TabItem>

      <TabItem value="javascript" label="JavaScript">
        ```javascript
        const response = await fetch('https://kieai.redpandaai.co/api/file-url-upload', {
          method: 'POST',
          headers: {
            'Authorization': 'Bearer YOUR_API_KEY',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            fileUrl: 'https://example.com/sample-image.jpg',
            uploadPath: 'images',
            fileName: 'my-image.jpg'
          })
        });

        const result = await response.json();
        console.log('Upload successful:', result);
        ```
      </TabItem>

      <TabItem value="python" label="Python">
        ```python
        import requests

        url = "https://kieai.redpandaai.co/api/file-url-upload"
        headers = {
            "Authorization": "Bearer YOUR_API_KEY",
            "Content-Type": "application/json"
        }

        payload = {
            "fileUrl": "https://example.com/sample-image.jpg",
            "uploadPath": "images",
            "fileName": "my-image.jpg"
        }

        response = requests.post(url, json=payload, headers=headers)
        result = response.json()

        print(f"Upload successful: {result}")
        ```
      </TabItem>
    </Tabs>
  </TabItem>

  <TabItem value="stream-upload" label="File Stream Upload">
    Suitable for directly uploading local files, especially large files:

    <Tabs groupId="programming-language">
      <TabItem value="bash" label="cURL">
        ```bash
        curl -X POST "https://kieai.redpandaai.co/api/file-stream-upload" \
          -H "Authorization: Bearer YOUR_API_KEY" \
          -F "file=@/path/to/your-file.jpg" \
          -F "uploadPath=images/user-uploads" \
          -F "fileName=custom-name.jpg"
        ```
      </TabItem>

      <TabItem value="javascript" label="JavaScript">
        ```javascript
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        formData.append('uploadPath', 'images/user-uploads');
        formData.append('fileName', 'custom-name.jpg');

        const response = await fetch('https://kieai.redpandaai.co/api/file-stream-upload', {
          method: 'POST',
          headers: {
            'Authorization': 'Bearer YOUR_API_KEY'
          },
          body: formData
        });

        const result = await response.json();
        console.log('Upload successful:', result);
        ```
      </TabItem>

      <TabItem value="python" label="Python">
        ```python
        import requests

        url = "https://kieai.redpandaai.co/api/file-stream-upload"
        headers = {
            "Authorization": "Bearer YOUR_API_KEY"
        }

        files = {
            'file': ('your-file.jpg', open('/path/to/your-file.jpg', 'rb')),
            'uploadPath': (None, 'images/user-uploads'),
            'fileName': (None, 'custom-name.jpg')
        }

        response = requests.post(url, headers=headers, files=files)
        result = response.json()

        print(f"Upload successful: {result}")
        ```
      </TabItem>
    </Tabs>
  </TabItem>

  <TabItem value="base64-upload" label="Base64 Upload">
    Suitable for Base64 encoded file data:

    <Tabs groupId="programming-language">
      <TabItem value="bash" label="cURL">
        ```bash
        curl -X POST "https://kieai.redpandaai.co/api/file-base64-upload" \
          -H "Authorization: Bearer YOUR_API_KEY" \
          -H "Content-Type: application/json" \
          -d '{
            "base64Data": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
            "uploadPath": "images",
            "fileName": "base64-image.png"
          }'
        ```
      </TabItem>

      <TabItem value="javascript" label="JavaScript">
        ```javascript
        const response = await fetch('https://kieai.redpandaai.co/api/file-base64-upload', {
          method: 'POST',
          headers: {
            'Authorization': 'Bearer YOUR_API_KEY',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            base64Data: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...',
            uploadPath: 'images',
            fileName: 'base64-image.png'
          })
        });

        const result = await response.json();
        console.log('Upload successful:', result);
        ```
      </TabItem>

      <TabItem value="python" label="Python">
        ```python
        import requests
        import base64

        # Read file and convert to base64
        with open('/path/to/your-file.jpg', 'rb') as f:
            file_data = base64.b64encode(f.read()).decode('utf-8')
            base64_data = f'data:image/jpeg;base64,{file_data}'

        url = "https://kieai.redpandaai.co/api/file-base64-upload"
        headers = {
            "Authorization": "Bearer YOUR_API_KEY",
            "Content-Type": "application/json"
        }

        payload = {
            "base64Data": base64_data,
            "uploadPath": "images",
            "fileName": "base64-image.jpg"
        }

        response = requests.post(url, json=payload, headers=headers)
        result = response.json()

        print(f"Upload successful: {result}")
        ```
      </TabItem>
    </Tabs>
  </TabItem>
</Tabs>

### Additional Step 1: fileName Parameter Explanation

:::info[]
The `fileName` parameter is optional across all upload methods, with the following behavior:
:::

#### `fileName` (string, optional)

**Filename behavior description:**

*   If no filename is provided, a random filename will be automatically generated
*   If the new uploaded filename matches an existing one, the old file will be overwritten
*   Due to caching, this change may not take effect immediately when overwriting files

**Examples:**

```javascript
// No fileName provided - auto-generate random filename
{ uploadPath: "images" } // → generates "abc123.jpg"

// Provide fileName - use specified filename
{ uploadPath: "images", fileName: "my-photo.jpg" }

// Overwrite file - replace existing file (with caching delay)
{ uploadPath: "images", fileName: "my-photo.jpg" } // Overwrites previous file
```

### Step 2: Handle Response

After successful upload, you'll receive a response containing file information:

```json
{
  "success": true,
  "code": 200,
  "msg": "File upload successful",
  "data": {
    "fileId": "file_abc123456",
    "fileName": "my-image.jpg",
    "originalName": "sample-image.jpg",
    "fileSize": 245760,
    "mimeType": "image/jpeg",
    "uploadPath": "images",
    "fileUrl": "https://kieai.redpandaai.co/files/images/my-image.jpg",
    "downloadUrl": "https://kieai.redpandaai.co/download/file_abc123456",
    "uploadTime": "2025-01-15T10:30:00Z",
    "expiresAt": "2025-01-18T10:30:00Z"
  }
}
```

## Upload Method Comparison

Choose the upload method best suited to your needs:

<CardGroup cols={3}>
  <Card title="URL File Upload" icon="lucide-link">
    **Best for**: File migration, batch processing

    **Advantages**:

    * No local file required
    * Automatic download processing
    * Supports remote resources

    **Limitations**:

    * Requires publicly accessible URL
    * 30-second download timeout
    * Recommended ≤100MB
  </Card>

  <Card title="File Stream Upload" icon="lucide-upload">
    **Best for**: Large files, local files

    **Advantages**:

    * High transfer efficiency
    * Supports large files
    * Binary transmission

    **Limitations**:

    * Requires local file
    * Server processing time
  </Card>

  <Card title="Base64 Upload" icon="lucide-code">
    **Best for**: Small files, API integration

    **Advantages**:

    * JSON format transmission
    * Easy integration
    * Supports Data URLs

    **Limitations**:

    * Data size increases by 33%
    * Not suitable for large files
    * Recommended ≤10MB
  </Card>
</CardGroup>

## Practical Examples

### Batch File Upload

Process multiple files using file stream upload:

<Tabs groupId="programming-language">
  <TabItem value="javascript" label="JavaScript">
    ```javascript
    class FileUploadAPI {
      constructor(apiKey) {
        this.apiKey = apiKey;
        this.baseUrl = 'https://kieai.redpandaai.co';
      }
      
      async uploadFile(file, uploadPath = '', fileName = null) {
        const formData = new FormData();
        formData.append('file', file);
        if (uploadPath) formData.append('uploadPath', uploadPath);
        if (fileName) formData.append('fileName', fileName);
        
        const response = await fetch(`${this.baseUrl}/api/file-stream-upload`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${this.apiKey}`
          },
          body: formData
        });
        
        if (!response.ok) {
          throw new Error(`Upload failed: ${response.statusText}`);
        }
        
        return response.json();
      }
      
      async uploadFromUrl(fileUrl, uploadPath = '', fileName = null) {
        const response = await fetch(`${this.baseUrl}/api/file-url-upload`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${this.apiKey}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            fileUrl,
            uploadPath,
            fileName
          })
        });
        
        if (!response.ok) {
          throw new Error(`Upload failed: ${response.statusText}`);
        }
        
        return response.json();
      }
      
      async uploadBase64(base64Data, uploadPath = '', fileName = null) {
        const response = await fetch(`${this.baseUrl}/api/file-base64-upload`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${this.apiKey}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            base64Data,
            uploadPath,
            fileName
          })
        });
        
        if (!response.ok) {
          throw new Error(`Upload failed: ${response.statusText}`);
        }
        
        return response.json();
      }
    }

    // Usage example
    const uploader = new FileUploadAPI('YOUR_API_KEY');

    // Batch upload files
    async function uploadMultipleFiles(files) {
      const results = [];
      
      for (let i = 0; i < files.length; i++) {
        try {
          const result = await uploader.uploadFile(
            files[i], 
            'user-uploads', 
            `file-${i + 1}-${files[i].name}`
          );
          results.push(result);
          console.log(`File ${i + 1} upload successful:`, result.data.fileUrl);
        } catch (error) {
          console.error(`File ${i + 1} upload failed:`, error.message);
        }
      }
      
      return results;
    }

    // Batch upload from URLs
    async function uploadFromUrls(urls) {
      const results = [];
      
      for (let i = 0; i < urls.length; i++) {
        try {
          const result = await uploader.uploadFromUrl(
            urls[i], 
            'downloads', 
            `download-${i + 1}.jpg`
          );
          results.push(result);
          console.log(`URL ${i + 1} upload successful:`, result.data.fileUrl);
        } catch (error) {
          console.error(`URL ${i + 1} upload failed:`, error.message);
        }
      }
      
      return results;
    }
    ```
  </TabItem>

  <TabItem value="python" label="Python">
    ```python
    import requests
    import base64
    import os
    from typing import List, Optional

    class FileUploadAPI:
        def __init__(self, api_key: str):
            self.api_key = api_key
            self.base_url = 'https://kieai.redpandaai.co'
            self.headers = {
                'Authorization': f'Bearer {api_key}'
            }
        
        def upload_file(self, file_path: str, upload_path: str = '', 
                       file_name: Optional[str] = None) -> dict:
            """File stream upload"""
            files = {
                'file': (os.path.basename(file_path), open(file_path, 'rb'))
            }
            
            data = {}
            if upload_path:
                data['uploadPath'] = upload_path
            if file_name:
                data['fileName'] = file_name
            
            response = requests.post(
                f'{self.base_url}/api/file-stream-upload',
                headers=self.headers,
                files=files,
                data=data
            )
            
            if not response.ok:
                raise Exception(f'Upload failed: {response.text}')
            
            return response.json()
        
        def upload_from_url(self, file_url: str, upload_path: str = '', 
                           file_name: Optional[str] = None) -> dict:
            """URL file upload"""
            payload = {
                'fileUrl': file_url,
                'uploadPath': upload_path,
                'fileName': file_name
            }
            
            response = requests.post(
                f'{self.base_url}/api/file-url-upload',
                headers={**self.headers, 'Content-Type': 'application/json'},
                json=payload
            )
            
            if not response.ok:
                raise Exception(f'Upload failed: {response.text}')
            
            return response.json()
        
        def upload_base64(self, base64_data: str, upload_path: str = '', 
                         file_name: Optional[str] = None) -> dict:
            """Base64 file upload"""
            payload = {
                'base64Data': base64_data,
                'uploadPath': upload_path,
                'fileName': file_name
            }
            
            response = requests.post(
                f'{self.base_url}/api/file-base64-upload',
                headers={**self.headers, 'Content-Type': 'application/json'},
                json=payload
            )
            
            if not response.ok:
                raise Exception(f'Upload failed: {response.text}')
            
            return response.json()

    # Usage example
    def main():
        uploader = FileUploadAPI('YOUR_API_KEY')
        
        # Batch upload local files
        file_paths = [
            '/path/to/file1.jpg',
            '/path/to/file2.png',
            '/path/to/document.pdf'
        ]
        
        print("Starting batch file upload...")
        for i, file_path in enumerate(file_paths):
            try:
                result = uploader.upload_file(
                    file_path, 
                    'user-uploads', 
                    f'file-{i + 1}-{os.path.basename(file_path)}'
                )
                print(f"File {i + 1} upload successful: {result['data']['fileUrl']}")
            except Exception as e:
                print(f"File {i + 1} upload failed: {e}")
        
        # Batch upload from URLs
        urls = [
            'https://example.com/image1.jpg',
            'https://example.com/image2.png'
        ]
        
        print("\nStarting batch URL upload...")
        for i, url in enumerate(urls):
            try:
                result = uploader.upload_from_url(
                    url, 
                    'downloads', 
                    f'download-{i + 1}.jpg'
                )
                print(f"URL {i + 1} upload successful: {result['data']['fileUrl']}")
            except Exception as e:
                print(f"URL {i + 1} upload failed: {e}")

    if __name__ == '__main__':
        main()
    ```
  </TabItem>
</Tabs>

## Error Handling

Common errors and how to handle them:

<details>
  <summary>401 Unauthorized</summary>

  ```javascript
  // Check if API key is correct
  if (response.status === 401) {
    console.error('Invalid API key, please check Authorization header');
    // Re-obtain or update API key
  }
  ```
</details>

<details>
  <summary>400 Bad Request</summary>

  ```javascript
  // Check request parameters
  if (response.status === 400) {
    const error = await response.json();
    console.error('Request parameter error:', error.msg);
    // Check if required parameters are provided
    // Check if file format is supported
    // Check if URL is accessible
  }
  ```
</details>

<details>
  <summary>500 Server Error</summary>

  ```javascript
  // Implement retry mechanism
  async function uploadWithRetry(uploadFunction, maxRetries = 3) {
    for (let i = 0; i < maxRetries; i++) {
      try {
        return await uploadFunction();
      } catch (error) {
        if (i === maxRetries - 1) throw error;
        
        // Exponential backoff
        const delay = Math.pow(2, i) * 1000;
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }
  }
  ```
</details>

## Best Practices

<details>
  <summary>File Size Optimization</summary>
  * **Small files** (≤1MB): Recommended to use Base64 upload
  * **Medium files** (1MB-10MB): Recommended to use file stream upload
  * **Large files** (>10MB): Must use file stream upload
  * **Remote files**: Use URL upload, note 100MB limit
</details>

<details>
  <summary>Performance Optimization</summary>
  * Implement concurrency control to avoid uploading too many files simultaneously
  * Consider chunked upload strategy for large files
  * Use appropriate retry mechanisms for network issues
  * Monitor upload progress and provide user feedback
</details>

<details>
  <summary>Security Considerations</summary>
  * Keep API keys secure and rotate regularly
  * Validate file types and sizes
  * Consider encrypted transmission for sensitive files
  * Download important files promptly to avoid deletion after 3 days
</details>

<details>
  <summary>Error Handling</summary>
  * Implement comprehensive error handling logic
  * Maintain upload logs for troubleshooting
  * Provide user-friendly error messages
  * Offer retry options for failed uploads
</details>

## File Storage Information

:::warning[**Important Reminder**]
All uploaded files are temporary and will be automatically deleted **3 days** after upload.
:::

* Files are accessible and downloadable immediately after upload
* File URLs remain valid for 3 days
* The system provides an `expiresAt` field in the response indicating expiration time
* Recommended to download or migrate important files before expiration
* Use the `downloadUrl` field to get direct download links

## Status Codes

*   **200** (Success): Request successfully processed, file upload completed
*   **400** (Bad Request): Incorrect request parameters or missing required parameters
*   **401** (Unauthorized): Missing authentication credentials or invalid credentials
*   **405** (Method Not Allowed): Unsupported request method, check HTTP method
*   **500** (Server Error): Unexpected error occurred while processing request, please retry or contact support

## Next Steps

<CardGroup cols={3}>
  <Card title="URL File Upload" icon="lucide-link" href="/file-upload-api/upload-file-url">
    Learn how to upload files from remote URLs
  </Card>

  <Card title="File Stream Upload" icon="lucide-upload" href="/file-upload-api/upload-file-stream">
    Learn efficient file stream upload methods
  </Card>

  <Card title="Base64 Upload" icon="lucide-code" href="/file-upload-api/upload-file-base-64">
    Master Base64 encoded file upload
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

Ready to start uploading files? [Get your API key](https://kie.ai/api-key) and begin using the file upload service now!