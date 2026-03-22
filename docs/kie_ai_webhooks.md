# Webhook Security Verification

:::warning[]
To ensure the security of callback requests, it is strongly recommended to enable Webhook HMAC signature verification in production environments to prevent forged requests and replay attacks.
:::

### Algorithm Overview

Kie AI uses the **HMAC-SHA256** algorithm to generate signatures, ensuring the integrity and authenticity of webhook callbacks.

**Signature Generation Process:**

1. **Concatenate the data to sign**: `taskId + "." + timestampSeconds`
   - `taskId`: Task ID from the request body
   - `timestampSeconds`: Unix timestamp in seconds from the `X-Webhook-Timestamp` header

2. **Calculate HMAC-SHA256 signature**:
   ```
   signature = HMAC-SHA256(dataToSign, webhookHmacKey)
   ```

3. **Base64 encode the signature**:
   ```
   finalSignature = Base64.encode(signature)
   ```

### Obtain Webhook HMAC Key

You can generate and view your `webhookHmacKey` on the [Kie AI Settings Page](https://kie.ai/settings).

::: info[]
The `webhookHmacKey` is used to verify that callback requests originate from Kie AI's official servers. Keep this key secure and never expose it or commit it to code repositories.
:::

### Webhook Header Description

When you enable the `webhookHmacKey` feature in the settings page, all callback requests will include the following fields in the HTTP headers:

### `X-Webhook-Timestamp`
- **Type**: Integer
- **Required**: Yes
- **Description**: Unix timestamp (in seconds) when the callback request was sent.

### `X-Webhook-Signature`
- **Type**: String
- **Required**: Yes
- **Description**: Signature generated using the HMAC-SHA256 algorithm with Base64 encoding.

#### Signature generation rule:
```
base64(HMAC-SHA256(taskId + "." + timestamp, webhookHmacKey))
```

Where:
- `taskId` is the task ID from the callback body
- `timestamp` is the value of `X-Webhook-Timestamp`
- `webhookHmacKey` is the key you generated in the console

---

### Webhook Verification Process

Follow these steps to verify the legitimacy of webhook requests:

<Steps>
<Step title="Read Header Fields">
Extract the `X-Webhook-Timestamp` and `X-Webhook-Signature` fields from the HTTP headers.

```javascript
const timestamp = req.headers['x-webhook-timestamp'];
const receivedSignature = req.headers['x-webhook-signature'];
```
</Step>

<Step title="Generate Signature">
Using your locally stored `webhookHmacKey`, generate the HMAC-SHA256 signature following these rules:

1. Extract `task_id` from the request body
2. Concatenate the string: `taskId + "." + timestamp`
3. Generate signature using HMAC-SHA256 algorithm with `webhookHmacKey`
4. Base64 encode the signature result

```javascript
const crypto = require('crypto');

const taskId = req.body.data.task_id;
const message = `${taskId}.${timestamp}`;

const computedSignature = crypto
  .createHmac('sha256', webhookHmacKey)
  .update(message)
  .digest('base64');
```
</Step>

<Step title="Compare Signatures">
Compare the computed signature with `X-Webhook-Signature` using a constant-time comparison algorithm to prevent timing attacks.

```javascript
// Use crypto.timingSafeEqual for constant-time comparison
if (computedSignature.length !== receivedSignature.length) {
  return res.status(401).json({ error: 'Invalid signature' });
}

const isValid = crypto.timingSafeEqual(
  Buffer.from(computedSignature),
  Buffer.from(receivedSignature)
);

if (isValid) {
  // Signature verified, request is legitimate
  console.log('Webhook signature verified');
} else {
  // Signature verification failed, reject request
  return res.status(401).json({ error: 'Invalid signature' });
}
```

<Check>
If the signatures match, the webhook request is confirmed to be from Kie AI's official servers and can be safely processed.
</Check>
</Step>
</Steps>

### Complete Example Code

Here are complete examples of implementing webhook signature verification in popular programming languages:

<Tabs>
<Tab title="Node.js">
```javascript
const express = require('express');
const crypto = require('crypto');
const app = express();

app.use(express.json());

// Read webhookHmacKey from environment variables or configuration
const WEBHOOK_HMAC_KEY = process.env.WEBHOOK_HMAC_KEY;

function generateSignature(taskId, timestampSeconds, secret) {
  // 1. Concatenate the data to sign
  const dataToSign = `${taskId}.${timestampSeconds}`;
  
  // 2. Calculate HMAC-SHA256 signature
  const hmac = crypto.createHmac('sha256', secret);
  hmac.update(dataToSign);
  
  // 3. Base64 encode
  return hmac.digest('base64');
}

function verifySignature(taskId, timestampSeconds, receivedSignature, secret) {
  // Regenerate signature
  const expectedSignature = generateSignature(taskId, timestampSeconds, secret);
  
  // Use secure string comparison
  if (expectedSignature.length !== receivedSignature.length) {
    return false;
  }
  
  return crypto.timingSafeEqual(
    Buffer.from(expectedSignature),
    Buffer.from(receivedSignature)
  );
}

function verifyWebhookSignature(req, res, next) {
  // 1. Read header fields
  const timestamp = req.headers['x-webhook-timestamp'];
  const receivedSignature = req.headers['x-webhook-signature'];

  if (!timestamp || !receivedSignature) {
    return res.status(401).json({ error: 'Missing signature headers' });
  }

  // 2. Verify signature
  const taskId = req.body.data?.task_id;
  if (!taskId) {
    return res.status(400).json({ error: 'Missing task_id' });
  }

  const isValid = verifySignature(taskId, timestamp, receivedSignature, WEBHOOK_HMAC_KEY);
  
  if (!isValid) {
    return res.status(401).json({ error: 'Invalid signature' });
  }

  // Signature verified
  next();
}

// Apply middleware
app.post('/webhook-callback', verifyWebhookSignature, (req, res) => {
  const { code, msg, data } = req.body;
  
  console.log('Received legitimate webhook request:', {
    taskId: data.task_id,
    status: code,
    callbackType: data.callbackType
  });
  
  // Process callback data...
  
  res.status(200).json({ status: 'received' });
});

app.listen(3000, () => {
  console.log('Webhook server running on port 3000');
});
```
</Tab>

<Tab title="Python">
```python
from flask import Flask, request, jsonify
import hmac
import hashlib
import base64
import os

app = Flask(__name__)

# Read webhookHmacKey from environment variables or configuration
WEBHOOK_HMAC_KEY = os.getenv('WEBHOOK_HMAC_KEY', '')

def generate_signature(task_id, timestamp_seconds, secret):
    """Generate Webhook signature"""
    # 1. Concatenate the data to sign
    data_to_sign = f"{task_id}.{timestamp_seconds}"
    
    # 2. Calculate HMAC-SHA256 signature
    signature = hmac.new(
        secret.encode('utf-8'),
        data_to_sign.encode('utf-8'),
        hashlib.sha256
    ).digest()
    
    # 3. Base64 encode
    return base64.b64encode(signature).decode('utf-8')

def verify_signature(task_id, timestamp_seconds, received_signature, secret):
    """Verify Webhook signature"""
    # Regenerate signature
    expected_signature = generate_signature(task_id, timestamp_seconds, secret)
    
    # Use secure string comparison
    return hmac.compare_digest(expected_signature, received_signature)

def verify_webhook_signature():
    # 1. Read header fields
    timestamp = request.headers.get('X-Webhook-Timestamp')
    received_signature = request.headers.get('X-Webhook-Signature')
    
    if not timestamp or not received_signature:
        return False, 'Missing signature headers'
    
    # 2. Verify signature
    data = request.json
    task_id = data.get('data', {}).get('task_id')
    
    if not task_id:
        return False, 'Missing task_id'
    
    is_valid = verify_signature(task_id, timestamp, received_signature, WEBHOOK_HMAC_KEY)
    
    if not is_valid:
        return False, 'Invalid signature'
    
    return True, 'Verified'

@app.route('/webhook-callback', methods=['POST'])
def handle_webhook():
    # Verify signature
    is_valid, message = verify_webhook_signature()
    
    if not is_valid:
        return jsonify({'error': message}), 401
    
    # Signature verified, process callback data
    data = request.json
    code = data.get('code')
    msg = data.get('msg')
    callback_data = data.get('data', {})
    task_id = callback_data.get('task_id')
    callback_type = callback_data.get('callbackType')
    
    print(f"Received legitimate webhook request: {task_id}, status: {code}, type: {callback_type}")
    
    # Process callback data...
    
    return jsonify({'status': 'received'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
```
</Tab>

<Tab title="PHP">
```php
<?php
header('Content-Type: application/json');

// Read webhookHmacKey from environment variables or configuration
$webhookHmacKey = getenv('WEBHOOK_HMAC_KEY');

function generateSignature($taskId, $timestampSeconds, $secret) {
    // 1. Concatenate the data to sign
    $dataToSign = $taskId . '.' . $timestampSeconds;
    
    // 2. Calculate HMAC-SHA256 signature
    $signature = hash_hmac('sha256', $dataToSign, $secret, true);
    
    // 3. Base64 encode
    return base64_encode($signature);
}

function verifySignature($taskId, $timestampSeconds, $receivedSignature, $secret) {
    // Regenerate signature
    $expectedSignature = generateSignature($taskId, $timestampSeconds, $secret);
    
    // Use secure string comparison
    return hash_equals($expectedSignature, $receivedSignature);
}

function verifyWebhookSignature($webhookHmacKey) {
    // 1. Read header fields
    $timestamp = $_SERVER['HTTP_X_WEBHOOK_TIMESTAMP'] ?? null;
    $receivedSignature = $_SERVER['HTTP_X_WEBHOOK_SIGNATURE'] ?? null;
    
    if (!$timestamp || !$receivedSignature) {
        return ['valid' => false, 'error' => 'Missing signature headers'];
    }
    
    // 2. Verify signature
    $input = file_get_contents('php://input');
    $data = json_decode($input, true);
    $taskId = $data['data']['task_id'] ?? null;
    
    if (!$taskId) {
        return ['valid' => false, 'error' => 'Missing task_id'];
    }
    
    $isValid = verifySignature($taskId, $timestamp, $receivedSignature, $webhookHmacKey);
    
    if (!$isValid) {
        return ['valid' => false, 'error' => 'Invalid signature'];
    }
    
    return ['valid' => true, 'data' => $data];
}

// Verify signature
$result = verifyWebhookSignature($webhookHmacKey);

if (!$result['valid']) {
    http_response_code(401);
    echo json_encode(['error' => $result['error']]);
    exit;
}

// Signature verified, process callback data
$data = $result['data'];
$code = $data['code'] ?? null;
$msg = $data['msg'] ?? '';
$callbackData = $data['data'] ?? [];
$taskId = $callbackData['task_id'] ?? '';
$callbackType = $callbackData['callbackType'] ?? '';

error_log("Received legitimate webhook request: $taskId, status: $code, type: $callbackType");

// Process callback data...

// Return success response
http_response_code(200);
echo json_encode(['status' => 'received']);
?>
```
</Tab>

<Tab title="Java">
```java
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.util.Base64;
import java.util.Objects;

public class WebhookVerifier {
    
    public static boolean verifySignature(String taskId, long timestampSeconds, String receivedSignature, String secret) {
        // Regenerate signature
        String expectedSignature = generateSignature(taskId, timestampSeconds, secret);

        // Use secure string comparison
        return constantTimeEquals(expectedSignature, receivedSignature);
    }

    public static String generateSignature(String taskId, long timestampSeconds, String secret) {
        try {
            // 1. Concatenate the data to sign
            String dataToSign = taskId + "." + timestampSeconds;

            // 2. Calculate HMAC-SHA256 signature
            Mac mac = Mac.getInstance("HmacSHA256");
            SecretKeySpec keySpec = new SecretKeySpec(
                    secret.getBytes(StandardCharsets.UTF_8), "HmacSHA256");
            mac.init(keySpec);
            byte[] hash = mac.doFinal(dataToSign.getBytes(StandardCharsets.UTF_8));

            // 3. Base64 encode
            return Base64.getEncoder().encodeToString(hash);
        } catch (NoSuchAlgorithmException | InvalidKeyException e) {
            throw new RuntimeException("Failed to generate webhook signature", e);
        }
    }

    private static boolean constantTimeEquals(String a, String b) {
        if (a == null || b == null) {
            return Objects.equals(a, b);
        }
        if (a.length() != b.length()) {
            return false;
        }
        int result = 0;
        for (int i = 0; i < a.length(); i++) {
            result |= a.charAt(i) ^ b.charAt(i);
        }
        return result == 0;
    }
}
```
</Tab>
</Tabs>

### Example Webhook Request

Here's what a complete webhook request looks like:

```http
POST /your-webhook-endpoint HTTP/1.1
Host: your-server.com
Content-Type: application/json
X-Webhook-Timestamp: 1769670760
X-Webhook-Signature: KxDlpbbq0GDOKqm0+FuJpJWTzY8baHSjhEt4kwElqQI=

{
  "taskId": "ee9c2715375b7837f8bb51d641ff5863",
  "code": 200,
  "msg": "Success",
  "data": {
    "task_id": "ee9c2715375b7837f8bb51d641ff5863",
    "callbackType": "task_completed",
    ...
  }
}
```

