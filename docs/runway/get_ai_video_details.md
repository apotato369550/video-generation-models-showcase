# Generate AI Video

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /api/v1/runway/generate:
    post:
      summary: Generate AI Video
      deprecated: false
      description: >-
        Create dynamic AI-generated videos from text prompts or image
        references.


        ### Usage Guide

        - Create short videos (5-10 seconds) using AI visualization

        - Generate videos based on text descriptions or reference images

        - Suitable for social media content, digital art, or concept
        visualization


        ### Parameter Details

        - `prompt` describes what you want to show in the video

        - `imageUrl` provides visual reference for AI

        - `aspectRatio` determines video orientation (vertical or horizontal)

        - `duration` control the video duration (5 or 10 seconds), where if a
        10-second video is selected, 1080p resolution cannot be selected 

        - `quality` video resolution (720p or 1080p), where if 1080p is
        selected, 10-second video cannot be generated

        - `waterMark` video watermark text content, empty string means no
        watermark


        ### Developer Notes

        - Generated videos are stored for 14 days before automatic deletion

        -  For text-only generation, aspect ratio must be explicitly specified
      operationId: generate-ai-video
      tags:
        - docs/en/Market/Video Models/Runway API
      parameters: []
      requestBody:
        content:
          application/json:
            schema:
              type: object
              required:
                - prompt
                - duration
                - quality
              properties:
                prompt:
                  type: string
                  description: >-
                    Descriptive text that guides the AI video generation. Be
                    specific about subject, action, style, and setting. When
                    used with an image, describes how to animate or modify the
                    image content. Maximum length is 1800 characters.
                  examples:
                    - >-
                      A fluffy orange cat dancing energetically in a colorful
                      room with disco lights
                imageUrl:
                  type: string
                  description: >-
                    Optional reference image URL to base the video on. When
                    provided, the AI will create a video animating or extending
                    this image.
                  examples:
                    - https://example.com/cat-image.jpg
                duration:
                  type: number
                  description: >-
                    Video duration, optional values are 5 or 10. If 10-second
                    video is selected, 1080p resolution cannot be used
                  examples:
                    - '5'
                quality:
                  type: string
                  description: >-
                    Video resolution, optional values are 720p or 1080p. If
                    1080p is selected, 10-second video cannot be generated
                  examples:
                    - 720p
                aspectRatio:
                  type: string
                  enum:
                    - '16:9'
                    - '4:3'
                    - '1:1'
                    - '3:4'
                    - '9:16'
                  description: >-
                    Video aspect ratio parameter. **Required parameter for
                    text-to-video generation requests. This parameter is invalid
                    when imageUrl is passed, and the aspect ratio will
                    ultimately be determined by the provided image.**
                  examples:
                    - '9:16'
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
                    The URL to receive AI video generation task completion
                    updates. Required for all video generation requests.


                    - System will POST task status and results to this URL when
                    video generation completes

                    - Callback includes generated video URLs, cover images, and
                    task information

                    - Your callback endpoint should accept POST requests with
                    JSON payload containing video results

                    - For detailed callback format and implementation guide, see
                    [Video Generation
                    Callbacks](https://docs.kie.ai/runway-api/generate-ai-video-callbacks)

                    - Alternatively, use the Get AI Video Details endpoint to
                    poll task status

                    - To ensure callback security, see [Webhook Verification
                    Guide](/common-api/webhook-verification) for signature
                    verification implementation
                  examples:
                    - https://api.example.com/callback
              x-apidog-orders:
                - prompt
                - imageUrl
                - duration
                - quality
                - aspectRatio
                - waterMark
                - callBackUrl
              x-apidog-ignore-properties: []
            example:
              prompt: >-
                A fluffy orange cat dancing energetically in a colorful room
                with disco lights
              imageUrl: https://example.com/cat-image.jpg
              model: runway-duration-5-generate
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

                          - **451**: Unauthorized - Failed to fetch the image.
                          Kindly verify any access limits set by you or your
                          service provider.

                          - **455**: Service Unavailable - System is currently
                          undergoing maintenance

                          - **500**: Server Error - An unexpected error occurred
                          while processing the request
                      msg:
                        type: string
                        description: Error message when code != 200
                        examples:
                          - success
                    x-apidog-orders:
                      - code
                      - msg
                    x-apidog-ignore-properties: []
                  - type: object
                    properties:
                      data:
                        type: object
                        properties:
                          taskId:
                            type: string
                            description: >-
                              Unique identifier for the generation task, can be
                              used with `Get AI Video Details` to query task
                              status
                            examples:
                              - ee603959-debb-48d1-98c4-a6d1c717eba6
                        x-apidog-orders:
                          - taskId
                        x-apidog-ignore-properties: []
                    x-apidog-orders:
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
        onVideoGenerated:
          '{$request.body#/callBackUrl}':
            post:
              summary: Video Generation Completion Callback
              description: >-
                When video generation is complete, the system will send a POST
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

                                  - **400**: get image info failed.

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
      x-run-in-apidog: https://app.apidog.com/web/project/1184766/apis/api-28506233-run
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