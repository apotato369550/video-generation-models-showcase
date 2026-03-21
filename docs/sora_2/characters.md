# Sora2 - Characters

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /api/v1/jobs/createTask:
    post:
      summary: Sora2 - Characters
      deprecated: false
      description: >-
        Create dynamic character animations powered by Sora-2-characters'
        advanced AI model


        ## File Upload Requirements


        Before using the Character Animation API, you need to upload your
        character videos:


        ### Step 1: Upload Character Videos


        Visit our [File Upload API](/file-upload-api/upload-file-url) to upload
        your character videos.


        **Requirements:**

        - **File Type**: MP4, WebM, or AVI format

        - **Duration**: Between 1-4 seconds per video

        - **Max File Size**: 10MB per file

        - **Content**: Character movements or actions you want to animate


        Only one character video can be uploaded per animation task.


        ### Step 2: Get Upload URLs


        After successful upload, you'll receive file URLs that can be used in
        the `character_file_url` parameter.


        ### Step 3: Submit Animation Task


        Use the obtained URLs in your API request to generate character
        animations with the new parameters.


        ## Additional Parameters


        Besides the character video URL, you can provide additional parameters
        to enhance your character animation:


        - **`character_prompt`**: Description of the character and desired
        animation style (Max 5000 characters)

        - **`safety_instruction`**: Safety guidelines and content restrictions
        for the animation (Max 5000 characters)


        Both parameters are optional but recommended for better control over the
        animation output.


        :::warning[File Storage Notice:]

        Files uploaded through our File Upload API are stored temporarily for
        only 14 days. After this period, the character URLs will become invalid
        and cause errors when using the Character Animation API. We recommend
        using third-party permanent storage solutions (such as AWS S3, Google
        Cloud Storage, or other cloud storage services) to ensure long-term
        availability of your character video files.

        :::


        ::: tip[]

        For production use, we recommend using the `callBackUrl` parameter to
        receive automatic notifications when generation completes, rather than
        polling the status endpoint.

        :::


        ## Query Task Status


        After submitting a task, use the unified query endpoint to check
        progress and retrieve results:


        <Card title="Get Task Details" icon="lucide-search"
        href="/market/common/get-task-detail">
           Learn how to query task status and retrieve generation results
        </Card>


        ### Task Query Response Format


        When the task is completed successfully (`state: "success"`), the
        `resultJson` field contains:

        ```

        {
          "character_id": "example_123456789"
        }

        ```


        :::tip[]

        For production use, we recommend using the callBackUrl parameter to
        receive automatic notifications when generation completes, rather than
        polling the status endpoint.

        :::


        ## Related Resources


        <CardGroup cols={3}>
          <Card title="Market Overview" icon="lucide-store" href="/market/quickstart">
            Explore all available models
          </Card>
          <Card title="File Upload API" icon="lucide-upload" href="/file-upload-api/upload-file-url">
            Learn how to upload your character videos
          </Card>
          <Card title="Common API" icon="lucide-cog" href="/common-api/get-account-credits">
            Check credits and account usage
          </Card>
        </CardGroup>
      operationId: sora-2-characters
      tags:
        - docs/en/Market/Video Models/Sora2
      parameters: []
      requestBody:
        content:
          application/json:
            schema:
              type: object
              required:
                - model
              properties:
                model:
                  type: string
                  enum:
                    - sora-2-characters
                  default: sora-2-characters
                  description: |-
                    The model name to use for generation. Required field.

                    - Must be `sora-2-characters` for this endpoint
                  examples:
                    - sora-2-characters
                callBackUrl:
                  type: string
                  format: uri
                  description: >-
                    The URL to receive generation task completion updates.
                    Optional but recommended for production use.


                    - System will POST task status and results to this URL when
                    generation completes

                    - Callback includes generated content URLs and task
                    information

                    - Your callback endpoint should accept POST requests with
                    JSON payload containing results

                    - Alternatively, use the Get Task Details endpoint to poll
                    task status

                    - To ensure callback security, see [Webhook Verification
                    Guide](/common-api/webhook-verification) for signature
                    verification implementation
                  examples:
                    - https://your-domain.com/api/callback
                input:
                  type: object
                  description: Input parameters for the generation task
                  properties:
                    character_file_url:
                      description: >-
                        Array of character video URLs to use as input for
                        character animation. Only one video URL is allowed. The
                        video must be between 1-4 seconds in duration. (File URL
                        after upload, not file content; Accepted types:
                        video/mp4, video/webm, video/avi; Max size: 10.0MB per
                        file; Duration: 1-4 seconds)
                      type: array
                      items:
                        type: string
                        format: uri
                      minItems: 1
                      maxItems: 1
                      examples:
                        - - >-
                            https://static.aiquickdraw.com/tools/example/character1.mp4
                    character_prompt:
                      description: >-
                        Description of the character and desired animation style
                        (Max length: 5000 characters)
                      type: string
                      maxLength: 5000
                      examples:
                        - >-
                          A friendly cartoon character with expressive eyes and
                          fluid movements
                    safety_instruction:
                      description: >-
                        Safety guidelines and content restrictions for the
                        animation (Max length: 5000 characters)
                      type: string
                      maxLength: 5000
                      examples:
                        - >-
                          Ensure the animation is family-friendly and contains
                          no violent or inappropriate content
                  required:
                    - character_file_url
                  x-apidog-orders:
                    - character_file_url
                    - character_prompt
                    - safety_instruction
                  x-apidog-ignore-properties: []
              x-apidog-orders:
                - model
                - callBackUrl
                - input
              x-apidog-ignore-properties: []
            example:
              model: sora-2-characters
              callBackUrl: https://your-domain.com/api/callback
              input:
                character_file_url:
                  - https://static.aiquickdraw.com/tools/example/character1.mp4
                character_prompt: >-
                  A friendly cartoon character with expressive eyes and fluid
                  movements
                safety_instruction: >-
                  Ensure the animation is family-friendly and contains no
                  violent or inappropriate content
      responses:
        '200':
          description: Request successful
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/ApiResponse'
              example:
                code: 200
                msg: success
                data:
                  taskId: task_sora-2-characters_1765174270120
          headers: {}
          x-apidog-name: ''
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
      x-apidog-folder: docs/en/Market/Video Models/Sora2
      x-apidog-status: released
      x-run-in-apidog: https://app.apidog.com/web/project/1184766/apis/api-28506409-run
components:
  schemas:
    ApiResponse:
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
            - **402**: 积分不足 - 账户积分不足以执行该操作
            - **404**: 未找到 - 请求的资源或端点不存在
            - **422**: 验证错误 - 请求参数未通过校验
            - **429**: 速率限制 - 已超出该资源的请求频次限制
            - **455**: 服务不可用 - 系统正在维护中
            - **500**: 服务器错误 - 处理请求时发生意外故障
            - **501**: 生成失败 - 内容生成任务执行失败
            - **505**: 功能禁用 - 当前请求的功能暂未开放
        msg:
          type: string
          description: 响应消息，请求失败时为错误描述
          examples:
            - success
      x-apidog-orders:
        - code
        - msg
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