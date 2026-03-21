# Get Aleph Video Details

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /api/v1/aleph/record-info:
    get:
      summary: Get Aleph Video Details
      deprecated: false
      description: >-
        > Retrieving comprehensive information about Runway Alpeh video
        generation tasks


        ## Overview


        Retrieve detailed information about your Runway Alpeh video generation
        tasks, including current status, generation parameters, video URLs, and
        error details. This endpoint is essential for monitoring task progress
        and accessing completed videos.


        :::highlight purple
          Use this endpoint to poll task status if you're not using callbacks, or to retrieve detailed information for completed tasks.
        :::
      operationId: get-aleph-video-details
      tags:
        - docs/en/Market/Video Models/Runway API/Aleph
      parameters:
        - name: taskId
          in: query
          description: >-
            Unique identifier of the Aleph video generation task. This is the
            taskId returned when creating an Aleph video.
          required: true
          example: ee603959-debb-48d1-98c4-a6d1c717eba6
          schema:
            type: string
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
                          failed validation checks

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
                              Unique identifier of the Aleph AI video generation
                              task
                            examples:
                              - ee603959-debb-48d1-98c4-a6d1c717eba6
                          paramJson:
                            type: string
                            description: >-
                              JSON string containing the original generation
                              request parameters
                            examples:
                              - >-
                                {"prompt":"A majestic eagle soaring through
                                mountain
                                clouds","videoUrl":"https://example.com/input-video.mp4"}
                          response:
                            type: object
                            description: >-
                              Response data containing generated video
                              information
                            properties:
                              taskId:
                                type: string
                                description: Task ID associated with this generation
                                examples:
                                  - ee603959-debb-48d1-98c4-a6d1c717eba6
                              resultVideoUrl:
                                type: string
                                description: >-
                                  URL to access and download the generated
                                  video, valid for 14 days
                                examples:
                                  - https://file.com/k/xxxxxxx.mp4
                              resultImageUrl:
                                type: string
                                description: >-
                                  URL of a thumbnail image from the generated
                                  video
                                examples:
                                  - https://file.com/m/xxxxxxxx.png
                            x-apidog-orders:
                              - taskId
                              - resultVideoUrl
                              - resultImageUrl
                            x-apidog-ignore-properties: []
                          completeTime:
                            type: string
                            format: date-time
                            description: Timestamp when the video generation was completed
                            examples:
                              - '2023-08-15T14:30:45Z'
                          createTime:
                            type: string
                            format: date-time
                            description: Timestamp when the task was created
                            examples:
                              - '2023-08-15T14:25:00Z'
                          successFlag:
                            type: integer
                            format: int32
                            description: >-
                              Success status: 1 = success, 0 = failed or in
                              progress
                            enum:
                              - 0
                              - 1
                            examples:
                              - 1
                          errorCode:
                            type: integer
                            format: int32
                            description: Error code when generation fails (0 if successful)
                            examples:
                              - 0
                          errorMessage:
                            type: string
                            description: >-
                              Detailed error message explaining the reason for
                              failure (empty if successful)
                            examples:
                              - ''
                        x-apidog-orders:
                          - taskId
                          - paramJson
                          - response
                          - completeTime
                          - createTime
                          - successFlag
                          - errorCode
                          - errorMessage
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
                  paramJson: >-
                    {"prompt":"A majestic eagle soaring through mountain clouds
                    at sunset","videoUrl":"https://example.com/input-video.mp4"}
                  response:
                    taskId: ee603959-debb-48d1-98c4-a6d1c717eba6
                    resultVideoUrl: https://file.com/k/xxxxxxx.mp4
                    resultImageUrl: https://file.com/m/xxxxxxxx.png
                  completeTime: '2023-08-15T14:30:45Z'
                  createTime: '2023-08-15T14:25:00Z'
                  successFlag: 1
                  errorCode: 0
                  errorMessage: ''
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
      x-apidog-folder: docs/en/Market/Video Models/Runway API/Aleph
      x-apidog-status: released
      x-run-in-apidog: https://app.apidog.com/web/project/1184766/apis/api-28506237-run
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