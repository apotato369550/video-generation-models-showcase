# Base64 File Upload

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /api/file-base64-upload:
    post:
      summary: Base64 File Upload
      deprecated: false
      description: >-
        :::info[]
          Uploaded files are temporary and will be automatically deleted after 3 days.
        :::


        ### Features


        * Supports Base64 encoded data and data URL formats

        * Automatically identifies MIME types and file extensions

        * Supports custom filenames or auto-generation (identical filenames will
        overwrite old files, potential caching delays may occur)

        * Returns complete file information and download links

        * Protected by API Key authentication

        * Uploaded files are temporary and will be automatically deleted after 3
        days


        ### Supported Formats


        * **Plain Base64 strings**: `iVBORw0KGgoAAAANSUhEUgAA...`

        * **Data URL format**:
        `data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...`


        ### Usage Recommendations


        * Recommended for small files such as images

        * Large files (>10MB) should use the File Stream Upload API

        * Base64 encoding increases data transmission volume by approximately
        33%
      operationId: upload-file-base64
      tags:
        - docs/en/File Upload API
      parameters: []
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Base64UploadRequest'
            examples:
              with_data_url:
                value:
                  base64Data: >-
                    data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==
                  uploadPath: images/base64
                  fileName: test-image.png
                summary: Using data URL format
              with_pure_base64:
                value:
                  base64Data: >-
                    iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==
                  uploadPath: documents/uploads
                summary: Using pure Base64 string
      responses:
        '200':
          description: File uploaded successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                    description: Whether the request was successful
                  code:
                    type: integer
                    enum:
                      - 200
                      - 400
                      - 401
                      - 405
                      - 500
                    description: >-
                      Response Status Code


                      | Code | Description |

                      |------|-------------|

                      | 200 | Success - Request has been processed successfully
                      |

                      | 400 | Bad Request - Request parameters are incorrect or
                      missing required parameters |

                      | 401 | Unauthorized - Authentication credentials are
                      missing or invalid |

                      | 405 | Method Not Allowed - Request method is not
                      supported |

                      | 500 | Server Error - An unexpected error occurred while
                      processing the request |
                  msg:
                    type: string
                    description: Response message
                    examples:
                      - File uploaded successfully
                  data:
                    $ref: '#/components/schemas/FileUploadResult'
                required:
                  - success
                  - code
                  - msg
                  - data
                x-apidog-orders:
                  - success
                  - code
                  - msg
                  - data
                x-apidog-ignore-properties: []
              example:
                success: true
                code: 200
                msg: File uploaded successfully
                data:
                  fileName: uploaded-image.png
                  filePath: images/user-uploads/uploaded-image.png
                  downloadUrl: >-
                    https://tempfile.redpandaai.co/xxx/images/user-uploads/uploaded-image.png
                  fileSize: 154832
                  mimeType: image/png
                  uploadedAt: '2025-01-01T12:00:00.000Z'
          headers: {}
          x-apidog-name: SuccessResponse
        '400':
          description: Request parameter error
          content:
            application/json:
              schema: &ref_0
                $ref: '#/components/schemas/ApiResponse'
              examples:
                '2':
                  summary: missing_parameter
                  value:
                    success: false
                    code: 400
                    msg: 'Missing required parameter: uploadPath'
                '3':
                  summary: invalid_format
                  value:
                    success: false
                    code: 400
                    msg: 'Base64 decoding failed: Invalid Base64 format'
          headers: {}
          x-apidog-name: BadRequestError
        '401':
          description: Unauthorized access
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ApiResponse1'
              example:
                success: false
                code: 401
                msg: 'Authentication failed: Invalid API Key'
          headers: {}
          x-apidog-name: UnauthorizedError
        '500':
          description: Internal server error
          content:
            application/json:
              schema: *ref_0
              example:
                success: false
                code: 500
                msg: Internal server error
          headers: {}
          x-apidog-name: ServerError
      security:
        - BearerAuth: []
          x-apidog:
            schemeGroups:
              - id: kn8M4YUlc5i0A0179ezwx
                schemeIds:
                  - BearerAuth
            required: true
            use:
              id: kn8M4YUlc5i0A0179ezwx
            scopes:
              kn8M4YUlc5i0A0179ezwx:
                BearerAuth: []
      x-apidog-folder: docs/en/File Upload API
      x-apidog-status: released
      x-run-in-apidog: https://app.apidog.com/web/project/1184766/apis/api-28506191-run
components:
  schemas:
    Base64UploadRequest:
      type: object
      properties:
        base64Data:
          type: string
          description: >-
            Base64 encoded file data. Supports pure Base64 strings or data URL
            format
          examples:
            - data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...
        uploadPath:
          type: string
          description: File upload path, without leading or trailing slashes
          examples:
            - images/base64
        fileName:
          type: string
          description: >-
            File name (optional), including file extension. If not provided, a
            random file name will be generated. If the same file name is
            uploaded again, the old file will be overwritten, but changes may
            not take effect immediately due to caching
          examples:
            - my-image.png
      required:
        - base64Data
        - uploadPath
      x-apidog-orders:
        - base64Data
        - uploadPath
        - fileName
      x-apidog-ignore-properties: []
      x-apidog-folder: ''
    FileUploadResult:
      type: object
      properties:
        fileName:
          type: string
          description: File name
          examples:
            - uploaded-image.png
        filePath:
          type: string
          description: Complete file path in storage
          examples:
            - images/user-uploads/uploaded-image.png
        downloadUrl:
          type: string
          format: uri
          description: File download URL
          examples:
            - >-
              https://tempfile.redpandaai.co/xxx/images/user-uploads/uploaded-image.png
        fileSize:
          type: integer
          description: File size in bytes
          examples:
            - 154832
        mimeType:
          type: string
          description: File MIME type
          examples:
            - image/png
        uploadedAt:
          type: string
          format: date-time
          description: Upload timestamp
          examples:
            - '2025-01-01T12:00:00.000Z'
      required:
        - fileName
        - filePath
        - downloadUrl
        - fileSize
        - mimeType
        - uploadedAt
      x-apidog-orders:
        - fileName
        - filePath
        - downloadUrl
        - fileSize
        - mimeType
        - uploadedAt
      x-apidog-ignore-properties: []
      x-apidog-folder: ''
    ApiResponse:
      type: object
      properties:
        success:
          type: boolean
          description: Whether the request was successful
        code:
          type: object
          properties: {}
        msg:
          type: string
          description: Response message
          examples:
            - File uploaded successfully
      required:
        - success
        - code
        - msg
      x-apidog-orders:
        - success
        - code
        - msg
      x-apidog-ignore-properties: []
      x-apidog-folder: ''
    ApiResponse1:
      type: object
      properties:
        code:
          type: integer
          enum:
            - 200
            - 401
            - 402
            - 404
            - 422
            - 429
            - 455
            - 500
            - 501
            - 505
          description: |-
            响应状态码

            - **200**: 成功 - 请求已处理完成
            - **401**: 未授权 - 身份验证凭据缺失或无效
            - **402**: 积分不足 - 账户余额不足以执行该操作
            - **404**: 未找到 - 请求的资源或接口不存在
            - **422**: 参数验证错误 - 请求参数未通过校验
            - **429**: 调用频率超限 - 已超出该资源的请求限制
            - **455**: 服务不可用 - 系统正在维护中
            - **500**: 服务器内部错误 - 处理请求时发生意外故障
            - **501**: 生成失败 - 内容生成任务执行失败
            - **505**: 功能禁用 - 当前请求的功能已被禁用
        msg:
          type: string
          description: 响应消息，请求失败时返回错误描述
          examples:
            - success
        success:
          type: boolean
          description: 是否成功
      x-apidog-orders:
        - code
        - msg
        - success
      required:
        - success
      x-apidog-ignore-properties: []
      x-apidog-folder: ''
  securitySchemes:
    BearerAuth:
      type: bearer
      scheme: bearer
      bearerFormat: API Key
      description: |-
        所有 API 都需要通过 Bearer Token 进行身份验证。

        获取 API Key：
        1. 访问 [API Key 管理页面](https://kie.ai/api-key) 获取您的 API Key

        使用方法：
        在请求头中添加：
        Authorization: Bearer YOUR_API_KEY

        注意事项：
        - 请妥善保管您的 API Key，切勿泄露给他人
        - 若怀疑 API Key 泄露，请立即在管理页面重置
servers:
  - url: https://api.kie.ai
    description: 正式环境
security:
  - BearerAuth: []
    x-apidog:
      schemeGroups:
        - id: kn8M4YUlc5i0A0179ezwx
          schemeIds:
            - BearerAuth
      required: true
      use:
        id: kn8M4YUlc5i0A0179ezwx
      scopes:
        kn8M4YUlc5i0A0179ezwx:
          BearerAuth: []

```