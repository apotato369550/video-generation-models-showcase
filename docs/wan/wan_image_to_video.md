# Wan - Image to Video

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
      summary: Wan - Image to Video
      deprecated: false
      description: >-
        Transform images into dynamic videos powered by Wan's advanced AI model


        ## Query Task Status


        After submitting a task, use the unified query endpoint to check
        progress and retrieve results:


        <Card title="Get Task Details" icon="lucide-search"
        href="/market/common/get-task-detail">
           Learn how to query task status and retrieve generation results
        </Card>


        ::: tip[]

        For production use, we recommend using the `callBackUrl` parameter to
        receive automatic notifications when generation completes, rather than
        polling the status endpoint.

        :::


        ## Related Resources


        <CardGroup cols={2}>
          <Card title="Market Overview" icon="lucide-store" href="/market/quickstart">
            Explore all available models
          </Card>
          <Card title="Common API" icon="lucide-cog" href="/common-api/get-account-credits">
            Check credits and account usage
          </Card>
        </CardGroup>
      operationId: wan-2-2-a14b-image-to-video-turbo
      tags:
        - docs/en/Market/Video Models/Wan
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
                    - wan/2-2-a14b-image-to-video-turbo
                  default: wan/2-2-a14b-image-to-video-turbo
                  description: >-
                    The model name to use for generation. Required field.


                    - Must be `wan/2-2-a14b-image-to-video-turbo` for this
                    endpoint
                  examples:
                    - wan/2-2-a14b-image-to-video-turbo
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
                    image_url:
                      description: >-
                        URL of the input image. If the input image does not
                        match the chosen aspect ratio, it is resized and center
                        cropped. (File URL after upload, not file content;
                        Accepted types: image/jpeg, image/png, image/webp; Max
                        size: 10.0MB)
                      type: string
                      examples:
                        - >-
                          https://file.aiquickdraw.com/custom-page/akr/section-images/1755166042585gtf2mlrk.png
                    prompt:
                      description: >-
                        The text prompt to guide video generation. (Max length:
                        5000 characters)
                      type: string
                      maxLength: 5000
                      examples:
                        - >-
                          Overcast lighting, medium lens, soft lighting, low
                          contrast lighting, edge lighting, low angle shot,
                          desaturated colors, medium close-up shot, clean single
                          shot, cool colors, center composition.The camera
                          captures a low-angle close-up of a Western man
                          outdoors, sharply dressed in a black coat over a gray
                          sweater, white shirt, and black tie. His gaze is fixed
                          on the lens as he advances. In the background, a brown
                          building looms, its windows glowing with warm, yellow
                          light above a dark doorway. As the camera pushes in, a
                          blurred black object on the right side of the frame
                          drifts back and forth, partially obscuring the view
                          against a dark, nighttime background.
                    resolution:
                      description: >-
                        Resolution of the generated video (480p or 720p).
                        Default value: "720p"
                      type: string
                      enum:
                        - 480p
                        - 720p
                      default: 720p
                      examples:
                        - 720p
                    enable_prompt_expansion:
                      description: >-
                        Whether to enable prompt expansion. This will use a
                        large language model to expand the prompt with
                        additional details while maintaining the original
                        meaning. (Boolean value (true/false))
                      type: boolean
                      examples:
                        - false
                    seed:
                      description: >-
                        Random seed for reproducibility. If None, a random seed
                        is chosen. (Min: 0, Max: 2147483647, Step: 1) (step: 1)
                      type: number
                      minimum: 0
                      maximum: 2147483647
                      default: 0
                      examples:
                        - 0
                    acceleration:
                      description: >-
                        Acceleration level to use. The more acceleration, the
                        faster the generation, but with lower quality. The
                        recommended value is 'none'. Default value: "none"
                      type: string
                      enum:
                        - none
                        - regular
                      default: none
                      examples:
                        - none
                    nsfw_checker:
                      type: boolean
                      description: >-
                        Enabled by default in Playground. For API calls, you can
                        turn it on or off based on your needs.
                  required:
                    - image_url
                    - prompt
                  x-apidog-orders:
                    - image_url
                    - prompt
                    - resolution
                    - enable_prompt_expansion
                    - seed
                    - acceleration
                    - nsfw_checker
                  x-apidog-ignore-properties: []
              x-apidog-orders:
                - model
                - callBackUrl
                - input
              x-apidog-ignore-properties: []
            example:
              model: wan/2-2-a14b-image-to-video-turbo
              callBackUrl: https://your-domain.com/api/callback
              input:
                image_url: >-
                  https://file.aiquickdraw.com/custom-page/akr/section-images/1755166042585gtf2mlrk.png
                prompt: >-
                  Overcast lighting, medium lens, soft lighting, low contrast
                  lighting, edge lighting, low angle shot, desaturated colors,
                  medium close-up shot, clean single shot, cool colors, center
                  composition.The camera captures a low-angle close-up of a
                  Western man outdoors, sharply dressed in a black coat over a
                  gray sweater, white shirt, and black tie. His gaze is fixed on
                  the lens as he advances. In the background, a brown building
                  looms, its windows glowing with warm, yellow light above a
                  dark doorway. As the camera pushes in, a blurred black object
                  on the right side of the frame drifts back and forth,
                  partially obscuring the view against a dark, nighttime
                  background.
                resolution: 720p
                enable_prompt_expansion: false
                seed: 0
                acceleration: none
                nsfw_checker: false
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
                  taskId: task_wan_1765172522239
          headers: {}
          x-apidog-name: ''
        '500':
          description: request failed
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                    description: >-
                      Response status code


                      - **200**: Success - Request has been processed
                      successfully

                      - **401**: Unauthorized - Authentication credentials are
                      missing or invalid

                      - **402**: Insufficient Credits - Account does not have
                      enough credits to perform the operation

                      - **404**: Not Found - The requested resource or endpoint
                      does not exist

                      - **422**: Validation Error - The request parameters
                      failed validation checks

                      - **429**: Rate Limited - Request limit has been exceeded
                      for this resource

                      - **455**: Service Unavailable - System is currently
                      undergoing maintenance

                      - **500**: Server Error - An unexpected error occurred
                      while processing the request

                      - **501**: Generation Failed - Content generation task
                      failed

                      - **505**: Feature Disabled - The requested feature is
                      currently disabled
                  msg:
                    type: string
                    description: Response message, error description when failed
                  data:
                    type: object
                    properties: {}
                    x-apidog-orders: []
                    x-apidog-ignore-properties: []
                x-apidog-orders:
                  - code
                  - msg
                  - data
                required:
                  - code
                  - msg
                  - data
                x-apidog-ignore-properties: []
              example:
                code: 500
                msg: >-
                  Server Error - An unexpected error occurred while processing
                  the request
                data: null
          headers: {}
          x-apidog-name: 'Error '
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
      x-apidog-folder: docs/en/Market/Video Models/Wan
      x-apidog-status: released
      x-run-in-apidog: https://app.apidog.com/web/project/1184766/apis/api-28506416-run
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