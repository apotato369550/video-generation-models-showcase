# Extend AI Video

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /api/v1/runway/extend:
    post:
      summary: Extend AI Video
      deprecated: false
      description: >-
        Extend existing AI-generated videos to create longer sequences.


        ### Usage Guide

        - Add additional segments to your AI-generated videos

        - Maintain visual consistency while extending narratives

        - Create longer sequences for storytelling or demonstrations


        ### Parameter Details

        - `taskId` identifies the original video to extend

        - `prompt` guides how the video should continue

        - `quality` video resolution, optional values are 720p or 1080p. 

        - `waterMark` video watermark text content, empty string means no
        watermark


        ### Developer Notes

        - Extended videos are stored for 14 days before automatic deletion

        - Extension maintains the same aspect ratio as the original video

        - Extension works best when continuing the same subject/theme as the
        original video
      operationId: extend-ai-video
      tags:
        - docs/en/Market/Video Models/Runway API
      parameters: []
      requestBody:
        content:
          application/json:
            schema:
              type: object
              required:
                - taskId
                - prompt
                - quality
              properties:
                taskId:
                  type: string
                  description: >-
                    Unique identifier of the original video generation task.
                    Must be a valid task ID from a previously generated video.
                  examples:
                    - ee603959-debb-48d1-98c4-a6d1c717eba6
                prompt:
                  type: string
                  description: >-
                    Descriptive text that guides the continuation of the video.
                    Explain what actions, movements, or developments should
                    happen next. Be specific but maintain consistency with the
                    original video content.
                  examples:
                    - >-
                      The cat continues dancing with more energy and excitement,
                      spinning around with colorful light effects intensifying
                quality:
                  type: string
                  description: 'Video resolution, optional values are 720p or 1080p. '
                  examples:
                    - 720p
                waterMark:
                  type: string
                  description: >-
                    Video watermark text content. An empty string indicates no
                    watermark, while a non-empty string will display the
                    specified text as a watermark in the bottom right corner of
                    the video.
                  examples:
                    - kie.ai
                callBackUrl:
                  type: string
                  description: >-
                    The URL to receive AI video extension task completion
                    updates. Required for all video extension requests.


                    - System will POST task status and results to this URL when
                    video extension completes

                    - Callback includes extended video URLs, cover images, and
                    task information

                    - Your callback endpoint should accept POST requests with
                    JSON payload containing extension results

                    - For detailed callback format and implementation guide, see
                    [Video Extension
                    Callbacks](https://docs.kie.ai/runway-api/extend-ai-video-callbacks)

                    - Alternatively, use the Get AI Video Details endpoint to
                    poll task status

                    - To ensure callback security, see [Webhook Verification
                    Guide](/common-api/webhook-verification) for signature
                    verification implementation
                  examples:
                    - https://api.example.com/callback
              x-apidog-orders:
                - taskId
                - prompt
                - quality
                - waterMark
                - callBackUrl
              x-apidog-ignore-properties: []
            example:
              taskId: ee603959-debb-48d1-98c4-a6d1c717eba6
              prompt: >-
                The cat continues dancing with more energy and excitement,
                spinning around with colorful light effects intensifying
              imageUrl: https://file.com/m/xxxxxxxx.png
              expandPrompt: true
              waterMark: kie.ai
              callBackUrl: https://api.example.com/callback
      responses:
        '200':
          description: Request successful
          content:
            application/json:
              schema:
                allOf:
                  - type: object
                    properties:
                      code:
                        type: integer
                        enum:
                          - 200
                          - 401
                          - 404
                          - 422
                          - 429
                          - 451
                          - 455
                          - 500
                        description: >-
                          Response status code


                          - **200**: Success - Request has been processed
                          successfully

                          - **401**: Unauthorized - Authentication credentials
                          are missing or invalid

                          - **404**: Not Found - The requested resource or
                          endpoint does not exist

                          - **422**: Validation Error - The request parameters
                          failed validation checks.The request parameters are
                          incorrect, please check the parameters.

                          - **429**: Rate Limited - Request limit has been
                          exceeded for this resource

                          - **451**: Unauthorized - Failed to fetch the image.
                          Kindly verify any access limits set by you or your
                          service provider.

                          - **455**: Service Unavailable - System is currently
                          undergoing maintenance

                          - **500**: Server Error - An unexpected error occurred
                          while processing the request
                      msg:
                        type: string
                        description: Status message
                        examples:
                          - success
                      data:
                        type: object
                        properties:
                          taskId:
                            type: string
                            description: >-
                              Task ID for tracking task status. Use this ID with
                              the "Get AI Video Details" endpoint to query
                              extension task details and results.
                            examples:
                              - 5c79****be8e
                        x-apidog-orders:
                          - taskId
                        x-apidog-ignore-properties: []
                    x-apidog-orders:
                      - code
                      - msg
                      - data
                    x-apidog-ignore-properties: []
              example:
                code: 200
                msg: success
                data:
                  taskId: ee603959-debb-48d1-98c4-a6d1c717eba6
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
      callbacks:
        onVideoExtended:
          '{$request.body#/callBackUrl}':
            post:
              summary: Video Extension Completion Callback
              description: >-
                When video extension is complete, the system will send a POST
                request to the provided callback URL to notify the result
              requestBody:
                required: true
                content:
                  application/json:
                    schema:
                      type: object
                      required:
                        - code
                        - data
                        - msg
                      properties:
                        code:
                          type: integer
                          description: Status code, 200 indicates success
                          example: 200
                        msg:
                          type: string
                          description: Status message
                          example: All generated successfully.
                        data:
                          type: object
                          required:
                            - image_url
                            - task_id
                            - video_id
                            - video_url
                          properties:
                            image_url:
                              type: string
                              description: Cover image URL of the generated video
                              example: https://file.com/m/xxxxxxxx.png
                            task_id:
                              type: string
                              description: Task ID
                              example: ee603959-debb-48d1-98c4-a6d1c717eba6
                            video_id:
                              type: string
                              description: Video ID
                              example: 485da89c-7fca-4340-8c04-101025b2ae71
                            video_url:
                              type: string
                              description: Accessible video URL, valid for 14 days
                              example: https://file.com/k/xxxxxxx.mp4
              responses:
                '200':
                  description: Callback received successfully
                  content:
                    application/json:
                      schema:
                        allOf:
                          - type: object
                            properties:
                              code:
                                type: integer
                                enum:
                                  - 200
                                  - 400
                                  - 500
                                description: >-
                                  Response status code


                                  - **200**: Success - Request has been
                                  processed successfully

                                  - **400**: Get image info failed.

                                  Inappropriate content detected. Please replace
                                  the image or video.

                                  Incorrect image format.

                                  Please try again later. You can upgrade to
                                  Standard membership to start generating now.

                                  Reached the limit for concurrent generations.

                                  Unsupported width or height. Please adjust the
                                  size and try again.

                                  Upload failed due to network reasons, please
                                  re-enter.

                                  Your prompt was caught by our AI moderator. 
                                  Please adjust it and try again!

                                  Your prompt/negative prompt cannot exceed 2048
                                  characters. Please check if your input is too
                                  long.

                                  Your video creation prompt contains NSFW
                                  content, which isn't allowed under our policy.
                                  Kindly revise your prompt and generate again.

                                  - **500**: Server Error - An unexpected error
                                  occurred while processing the request
                              msg:
                                type: string
                                description: Error message when code != 200
                                example: success
                      example:
                        code: 200
                        msg: success
      x-apidog-folder: docs/en/Market/Video Models/Runway API
      x-apidog-status: released
      x-run-in-apidog: https://app.apidog.com/web/project/1184766/apis/api-28506235-run
components:
  schemas: {}
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