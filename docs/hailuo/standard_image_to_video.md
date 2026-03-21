# Hailuo Standard Image to Video

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
      summary: Hailuo Standard Image to Video
      deprecated: false
      description: >-
        Content generation using hailuo/02-image-to-video-standard


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
      operationId: hailuo-02-image-to-video-standard
      tags:
        - docs/en/Market/Video Models/Hailuo
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
                    - hailuo/02-image-to-video-standard
                  default: hailuo/02-image-to-video-standard
                  description: >-
                    The model name to use for generation. Required field.


                    - Must be `hailuo/02-image-to-video-standard` for this
                    endpoint
                  examples:
                    - hailuo/02-image-to-video-standard
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
                    prompt:
                      description: >-
                        The text prompt describing the video to generate (Max
                        length: 1500 characters)
                      type: string
                      maxLength: 1500
                      examples:
                        - >-
                          Epic aerial shot: A lone samurai stands atop a jagged
                          mountain peak as a storm of sakura petals is swept
                          across the wind. Behind him, the sky is split in two —
                          half daylight, half night. The shot pulls back to
                          reveal that the mountain is actually the curved back
                          of a sleeping dragon that spans across the horizon.
                          Lightning crackles in the distance as the dragon's eye
                          slowly opens, glowing with ancient magic. The samurai
                          doesn’t flinch; he lowers his straw hat and places his
                          hand on the hilt of his blade.
                    image_url:
                      description: >-
                        The URL of the image to use as the first frame of the
                        video (File URL after upload, not file content; Accepted
                        types: image/jpeg, image/png, image/webp; Max size:
                        10.0MB)
                      type: string
                      examples:
                        - >-
                          https://file.aiquickdraw.com/custom-page/akr/section-images/17585207681646umf3lz8.png
                    end_image_url:
                      description: >-
                        Optional URL of the image to use as the last frame of
                        the video (File URL after upload, not file content;
                        Accepted types: image/jpeg, image/png, image/webp; Max
                        size: 10.0MB)
                      type: string
                      examples:
                        - >-
                          https://file.aiquickdraw.com/custom-page/akr/section-images/1758521423357w8586uq8.png
                    duration:
                      description: >-
                        The duration of the video in seconds. 10 seconds videos
                        are not supported for 1080p resolution.
                      type: string
                      enum:
                        - '6'
                        - '10'
                      default: '10'
                      examples:
                        - '10'
                    resolution:
                      description: The resolution of the generated video.
                      type: string
                      enum:
                        - 512P
                        - 768P
                      default: 768P
                      examples:
                        - 768P
                    prompt_optimizer:
                      description: >-
                        Whether to use the model's prompt optimizer (Boolean
                        value (true/false))
                      type: boolean
                      examples:
                        - true
                  required:
                    - prompt
                    - image_url
                  x-apidog-orders:
                    - prompt
                    - image_url
                    - end_image_url
                    - duration
                    - resolution
                    - prompt_optimizer
                  x-apidog-ignore-properties: []
              x-apidog-orders:
                - model
                - callBackUrl
                - input
              x-apidog-ignore-properties: []
            example:
              model: hailuo/02-image-to-video-standard
              callBackUrl: https://your-domain.com/api/callback
              input:
                prompt: >-
                  Epic aerial shot: A lone samurai stands atop a jagged mountain
                  peak as a storm of sakura petals is swept across the wind.
                  Behind him, the sky is split in two — half daylight, half
                  night. The shot pulls back to reveal that the mountain is
                  actually the curved back of a sleeping dragon that spans
                  across the horizon. Lightning crackles in the distance as the
                  dragon's eye slowly opens, glowing with ancient magic. The
                  samurai doesn’t flinch; he lowers his straw hat and places his
                  hand on the hilt of his blade.
                image_url: >-
                  https://file.aiquickdraw.com/custom-page/akr/section-images/17585207681646umf3lz8.png
                end_image_url: >-
                  https://file.aiquickdraw.com/custom-page/akr/section-images/1758521423357w8586uq8.png
                duration: '10'
                resolution: 768P
                prompt_optimizer: true
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
                  taskId: task_hailuo_1765185334551
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
      x-apidog-folder: docs/en/Market/Video Models/Hailuo
      x-apidog-status: released
      x-run-in-apidog: https://app.apidog.com/web/project/1184766/apis/api-28506406-run
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