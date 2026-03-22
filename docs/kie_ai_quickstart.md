# Common API Quickstart

> Basic utility APIs for account management and file operations

## Welcome to the Common API

The Common API provides fundamental utility services for managing your kie.ai account and handling generated content. These APIs help you monitor credit usage and efficiently access generated files.

<CardGroup cols={2}>
  <Card title="Check Account Credits" icon="lucide-wallet" href="/common-api/get-account-credits">
    View your current credit balance and monitor usage
  </Card>

  <Card title="Get Download Link" icon="lucide-download" href="/common-api/download-url">
    Generate temporary download links for generated files
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

### Authorization Header

```http
Authorization: Bearer YOUR_API_KEY
```

## Quick Start Guide

### Step 1: Check Credit Balance

Monitor your account credits to ensure you have sufficient balance to continue using the services:

<Tabs>
  <TabItem value="cURL" label="cURL">
    ```bash
    curl -X GET "https://api.kie.ai/api/v1/chat/credit" \
      -H "Authorization: Bearer YOUR_API_KEY"
    ```
  </TabItem>

  <TabItem value="JavaScript" label="JavaScript">
    ```javascript
    const response = await fetch('https://api.kie.ai/api/v1/chat/credit', {
      method: 'GET',
      headers: {
        'Authorization': 'Bearer YOUR_API_KEY'
      }
    });

    const result = await response.json();
    console.log('Current credits:', result.data);
    ```
  </TabItem>

  <TabItem value="Python" label="Python">
    ```python
    import requests

    url = "https://api.kie.ai/api/v1/chat/credit"
    headers = {
        "Authorization": "Bearer YOUR_API_KEY"
    }

    response = requests.get(url, headers=headers)
    result = response.json()

    print(f"Current credits: {result['data']}")
    ```
  </TabItem>
</Tabs>

**Response Example:**

```json
{
  "code": 200,
  "msg": "success",
  "data": 100
}
```

### Step 2: Get Download Link for Generated Files

Convert the URL of a generated file into a temporary downloadable link:

<Tabs>
  <TabItem value="cURL" label="cURL">
    ```bash
    curl -X POST "https://api.kie.ai/api/v1/common/download-url" \
      -H "Authorization: Bearer YOUR_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "url": "https://tempfile.1f6cxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxbd98"
      }'
    ```
  </TabItem>

  <TabItem value="JavaScript" label="JavaScript">
    ```javascript
    const response = await fetch('https://api.kie.ai/api/v1/common/download-url', {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer YOUR_API_KEY',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        url: 'https://tempfile.1f6cxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxbd98'
      })
    });

    const result = await response.json();
    console.log('Download URL:', result.data);
    ```
  </TabItem>

  <TabItem value="Python" label="Python">
    ```python
    import requests

    url = "https://api.kie.ai/api/v1/common/download-url"
    headers = {
        "Authorization": "Bearer YOUR_API_KEY",
        "Content-Type": "application/json"
    }

    payload = {
        "url": "https://tempfile.1f6cxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxbd98"
    }

    response = requests.post(url, json=payload, headers=headers)
    result = response.json()

    print(f"Download URL: {result['data']}")
    ```
  </TabItem>
</Tabs>

**Response Example:**

```json
{
  "code": 200,
  "msg": "success",
  "data": "https://tempfile.1f6cxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxbd98"
}
```

:::warning[]
Download links are valid for **only 20 minutes**. Ensure you download or cache content within this timeframe.
:::

## API Overview

### Check Account Credits

<Card title="GET /api/v1/chat/credit" icon="lucide-wallet">
  **Purpose**: Monitor your account credit balance

  **Features**:

  * Get real-time credit balance
  * No parameters required
  * Immediate response
  * Essential for usage monitoring

  **Use Cases**:

  * Check credits before starting generation tasks
  * Monitor credit consumption patterns
  * Plan for credit top-ups
  * Implement credit threshold alerts
</Card>

### Get Download Link

<Card title="POST /api/v1/common/download-url" icon="lucide-download">
  **Purpose**: Generate temporary download links for generated files

  **Features**:

  * Supports all kie.ai generated file types (images, videos, audio, etc.)
  * 20-minute validity period
  * Secure authenticated access
  * Works only with kie.ai generated URLs

  **Use Cases**:

  * Download generated content to local storage
  * Share temporary links with team members
  * Integrate into external systems
  * Build custom download workflows
</Card>

## Practical Examples

### Credit Monitoring System

Implement an automated credit monitoring system:

<Tabs>
  <TabItem value="JavaScript" label="JavaScript">
    ```javascript
    class KieAIClient {
      constructor(apiKey) {
        this.apiKey = apiKey;
        this.baseUrl = 'https://api.kie.ai';
      }
      
      async getCredits() {
        const response = await fetch(`${this.baseUrl}/api/v1/chat/credit`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${this.apiKey}`
          }
        });
        
        if (!response.ok) {
          throw new Error(`Failed to get credits: ${response.statusText}`);
        }
        
        const result = await response.json();
        return result.data;
      }
      
      async getDownloadUrl(fileUrl) {
        const response = await fetch(`${this.baseUrl}/api/v1/common/download-url`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${this.apiKey}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ url: fileUrl })
        });
        
        if (!response.ok) {
          throw new Error(`Failed to get download URL: ${response.statusText}`);
        }
        
        const result = await response.json();
        return result.data;
      }
      
      async downloadFile(fileUrl, outputPath) {
        // Get download link
        const downloadUrl = await this.getDownloadUrl(fileUrl);
        
        // Download file
        const response = await fetch(downloadUrl);
        const buffer = await response.arrayBuffer();
        
        // Save to file (Node.js)
        const fs = require('fs');
        fs.writeFileSync(outputPath, Buffer.from(buffer));
        
        console.log(`File downloaded to: ${outputPath}`);
      }
      
      async checkCreditsAndWarn(threshold = 10) {
        const credits = await this.getCredits();
        
        if (credits < threshold) {
          console.warn(`⚠️  Low credits warning: ${credits} credits remaining`);
          return false;
        }
        
        console.log(`✓ Credits available: ${credits}`);
        return true;
      }
    }

    // Usage Example
    const client = new KieAIClient('YOUR_API_KEY');

    // Monitor credits before operations
    async function runWithCreditCheck() {
      const hasEnoughCredits = await client.checkCreditsAndWarn(20);
      
      if (!hasEnoughCredits) {
        console.error('Insufficient credits. Please recharge your account.');
        return;
      }
      
      // Credits verified, proceed with operations
      console.log('Credits verified. Proceeding with operations...');
    }

    // Download generated files
    async function downloadGeneratedFiles(fileUrls) {
      for (let i = 0; i < fileUrls.length; i++) {
        try {
          await client.downloadFile(
            fileUrls[i],
            `./downloads/file-${i + 1}.mp4`
          );
          console.log(`✓ Downloaded file ${i + 1}/${fileUrls.length}`);
        } catch (error) {
          console.error(`✗ Failed to download file ${i + 1}:`, error.message);
        }
      }
    }

    // Periodic credit monitoring
    async function monitorCredits(intervalMinutes = 60) {
      setInterval(async () => {
        try {
          const credits = await client.getCredits();
          console.log(`[${new Date().toISOString()}] Current credits: ${credits}`);
          
          if (credits < 50) {
            // Send alerts (email, webhook, etc.)
            console.warn('ALERT: Credits below 50!');
          }
        } catch (error) {
          console.error('Credit check failed:', error.message);
        }
      }, intervalMinutes * 60 * 1000);
    }
    ```
  </TabItem>

  <TabItem value="Python" label="Python">
    ```python
    import requests
    import time
    import os
    from datetime import datetime
    from typing import Optional

    class KieAIClient:
        def __init__(self, api_key: str):
            self.api_key = api_key
            self.base_url = 'https://api.kie.ai'
            self.headers = {
                'Authorization': f'Bearer {api_key}'
            }
        
        def get_credits(self) -> int:
            """Get current account credits"""
            response = requests.get(
                f'{self.base_url}/api/v1/chat/credit',
                headers=self.headers
            )
            
            if not response.ok:
                raise Exception(f'Failed to get credits: {response.text}')
            
            result = response.json()
            return result['data']
        
        def get_download_url(self, file_url: str) -> str:
            """Get temporary download link for generated file"""
            response = requests.post(
                f'{self.base_url}/api/v1/common/download-url',
                headers={**self.headers, 'Content-Type': 'application/json'},
                json={'url': file_url}
            )
            
            if not response.ok:
                raise Exception(f'Failed to get download URL: {response.text}')
            
            result = response.json()
            return result['data']
        
        def download_file(self, file_url: str, output_path: str) -> None:
            """Download file from kie.ai URL"""
            # Get download link
            download_url = self.get_download_url(file_url)
            
            # Download file
            response = requests.get(download_url)
            
            if not response.ok:
                raise Exception(f'Failed to download file: {response.text}')
            
            # Save to file
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            print(f'File downloaded to: {output_path}')
        
        def check_credits_and_warn(self, threshold: int = 10) -> bool:
            """Check credits and warn if below threshold"""
            credits = self.get_credits()
            
            if credits < threshold:
                print(f'⚠️  Low credits warning: {credits} credits remaining')
                return False
            
            print(f'✓ Credits available: {credits}')
            return True

    # Usage Example
    def main():
        client = KieAIClient('YOUR_API_KEY')
        
        # Monitor credits before operations
        def run_with_credit_check():
            has_enough_credits = client.check_credits_and_warn(threshold=20)
            
            if not has_enough_credits:
                print('Insufficient credits. Please recharge your account.')
                return
            
            print('Credits verified. Proceeding with operations...')
        
        # Download generated files
        def download_generated_files(file_urls: list):
            for i, file_url in enumerate(file_urls):
                try:
                    client.download_file(
                        file_url,
                        f'./downloads/file-{i + 1}.mp4'
                    )
                    print(f'✓ Downloaded file {i + 1}/{len(file_urls)}')
                except Exception as e:
                    print(f'✗ Failed to download file {i + 1}: {e}')
        
        # Periodic credit monitoring
        def monitor_credits(interval_minutes: int = 60):
            while True:
                try:
                    credits = client.get_credits()
                    timestamp = datetime.now().isoformat()
                    print(f'[{timestamp}] Current credits: {credits}')
                    
                    if credits < 50:
                        # Send alerts (email, webhook, etc.)
                        print('ALERT: Credits below 50!')
                except Exception as e:
                    print(f'Credit check failed: {e}')
                
                time.sleep(interval_minutes * 60)
        
        # Example execution
        print('Checking credits...')
        run_with_credit_check()
        
        print('\nDownloading files...')
        file_urls = [
            'https://tempfile.1f6cxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxbd98',
            'https://tempfile.2f7dxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxcd99'
        ]
        download_generated_files(file_urls)

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
  <summary>422 Validation Error (Download Link)</summary>

  ```javascript
  // Only kie.ai generated URLs are supported
  if (response.status === 422) {
    const error = await response.json();
    console.error('Invalid URL:', error.msg);
    // Ensure you're using a kie.ai generated file URL
    // External URLs are not supported
  }
  ```
</details>

<details>
  <summary>402 Insufficient Credits</summary>

  ```javascript
  // Credits exhausted, need to recharge
  if (response.status === 402) {
    console.error('Insufficient credits. Please recharge your account.');
    // Redirect to credit purchase page
    // Or send notification to administrator
  }
  ```
</details>

<details>
  <summary>500 Server Error</summary>

  ```javascript
  // Implement retry mechanism
  async function apiCallWithRetry(apiFunction, maxRetries = 3) {
    for (let i = 0; i < maxRetries; i++) {
      try {
        return await apiFunction();
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
  <summary>Credit Management</summary>
  * **Regular Monitoring**: Check credits before starting bulk operations
  * **Set Alerts**: Implement automated alerts when credits fall below thresholds
  * **Budget Planning**: Track credit consumption patterns for better planning
  * **Graceful Degradation**: Handle insufficient credits appropriately
</details>

<details>
  <summary>Download Link Usage</summary>
  * **Time Sensitivity**: Download links expire after 20 minutes
  * **Proper Caching**: Save files immediately after obtaining download links
  * **Batch Downloads**: Efficiently process multiple files within time limits
  * **Error Handling**: Implement retry logic for failed downloads
</details>

<details>
  <summary>Performance Optimization</summary>
  * **Parallel Processing**: Download multiple files concurrently (respect rate limits)
  * **Connection Pooling**: Reuse HTTP connections for multiple requests
  * **Timeout Settings**: Set reasonable timeouts for download operations
  * **Progress Tracking**: Implement progress indicators for long-running operations
</details>

<details>
  <summary>Security Considerations</summary>
  * **API Key Protection**: Never expose API keys in client-side code
  * **HTTPS Only**: Always use HTTPS for API requests
  * **Key Rotation**: Periodically rotate API keys for security
  * **Access Logging**: Maintain API usage logs for auditing
</details>

## Important Notes

:::warning[**Download Link Expiry**]
Temporary download links are valid for **only 20 minutes**. Please ensure:
* Download files immediately after obtaining the URL
* Implement error handling for expired URLs
* Cache downloaded content for future use
:::

:::info[**Credit Balance**]
Service access will be restricted when credits are exhausted. Be sure to:
* Regularly monitor credit balance
* Set low-credit warnings
* Plan credit top-ups in advance
* Implement graceful degradation when credits are low
:::

:::note[**Supported URLs**]
The download link endpoint only supports files generated by kie.ai services. External file URLs will result in a 422 validation error.
:::

## Next Steps

<CardGroup cols={2}>
  <Card title="Check Account Credits" icon="lucide-wallet" href="/common-api/get-account-credits">
    Learn how to check and monitor your credit balance
  </Card>

  <Card title="Get Download Link" icon="lucide-download" href="/common-api/download-url">
    Master the method for generating file download URLs
  </Card>
</CardGroup>

## Integration Examples

<CardGroup cols={2}>
  <Card title="Marketplace API" icon="lucide-store" href="/market/quickstart">
    Explore AI model marketplace APIs
  </Card>

  <Card title="File Upload API" icon="lucide-upload" href="/file-upload-api/quickstart">
    Upload files for processing
  </Card>
</CardGroup>

## Technical Support

:::info[]
Need help? Our technical support team is here for you.

* **Email**: [support@kie.ai](mailto:support@kie.ai)
* **Documentation**: [docs.kie.ai](https://docs.kie.ai)
* **API Status**: Check our status page for real-time API health
:::

***

Ready to get started? [Get your API key](https://kie.ai/api-key) and begin using the Common API services now!