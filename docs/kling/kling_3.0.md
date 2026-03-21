# Kling 3.0

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
      summary: Kling 3.0
      deprecated: false
      description: >-
        Generate high-quality videos with advanced multi-shot capabilities and
        element references using Kling 3.0 AI 


        ## Overview


        Kling 3.0 is an advanced video generation model that supports both
        single-shot and multi-shot video creation with element references. It
        offers two generation modes (standard and pro) with different resolution
        options, and supports sound effects for enhanced video output.


        ## Key Features


        - **Dual Generation Modes**: Choose between `std` (standard resolution)
        and `pro` (higher resolution) modes

        - **Multi-Shot Support**: Create videos with multiple shots, each with
        its own prompt and duration

        - **Element References**: Reference images in your prompts using
        `@element_name` syntax

        - **Sound Effects**: Optional sound effects to enhance video output

        - **Flexible Aspect Ratios**: Support for 16:9, 9:16, and 1:1 aspect
        ratios

        - **Configurable Duration**: Video duration from 3 to 15 seconds


        ## Resolution Mappings


        The resolution depends on both the `mode` and `aspect_ratio` parameters:


        <Tabs groupId="mode">

        <TabItem value="std" label="Standard Mode (std)">


        | Aspect Ratio | Resolution |

        |--------------|------------|

        | 16:9         | 1280×720   |

        | 9:16         | 720×1280   |

        | 1:1          | 720×720    |


        </TabItem>

        <TabItem value="pro" label="Pro Mode (pro)">


        | Aspect Ratio | Resolution |

        |--------------|------------|

        | 16:9         | 1920×1080  |

        | 9:16         | 1080×1920  |

        | 1:1          | 1080×1080  |


        </TabItem>

        </Tabs>


        :::info[]

        Pro mode provides higher resolution output but may take longer to
        generate and consume more credits.

        :::


        ## Single-Shot vs Multi-Shot Mode


        ### Single-Shot Mode (`multi_shots: false`)

        - Uses the main `prompt` field for video generation

        - Supports first and last frame images via `image_urls`

        - Sound effects are optional


        ### Multi-Shot Mode (`multi_shots: true`)

        - Uses `multi_prompt` array to define multiple shots

        - Each shot has its own prompt and duration (1-12 seconds)

        - Only supports first frame image (via `image_urls[0]`)

        - Sound effects default to enabled

        - The maximum number of characters per shot is 500



        ## Aspect Ratio Auto-Adaptation


        When you provide `image_urls` (first and/or last frame images), the
        `aspect_ratio` parameter becomes optional. The system will automatically
        adapt the aspect ratio based on the uploaded images, so you don't need
        to specify it manually.


        :::tip[]

        If you upload reference images, you can omit the `aspect_ratio`
        parameter and let the system automatically match the aspect ratio of
        your images.

        :::


        ## Element References


        You can reference images or videos in your prompts using the
        `@element_name` syntax. Define elements in the `kling_elements` array:


        - **Image Elements**: 2-4 image URLs (JPG/PNG, max 10MB each)


        :::tip[]

        Use descriptive element names and ensure the element name in
        `kling_elements` matches the name used in your prompt (without the @
        symbol).

        A single task can reference a maximum of 3 elements, and each `@element`
        will occupy 37 characters.

        :::


        ## File Upload Requirements


        Before using element references, upload your image  files:


        ### 1. Upload Files


        Use the File Upload API to upload your source images.


        :::info[File Upload API]

        Learn how to upload files and get file URLs: [File Upload API
        Quickstart](/file-upload-api/quickstart)

        :::


        ### 2. Get File URLs


        After upload, you'll receive file URLs that you can use in
        `element_input_urls` .


        :::caution[]

        - Image formats: JPG, PNG (max 10MB per file, 2-4 files per element)

        - Ensure file URLs are accessible and not expired

        :::


        ## Usage Examples


        ### Single-Shot Video with Element Reference


        ```json

        {
          "model": "kling-3.0",
          "input": {
            "prompt": "In a bright rehearsal room, sunlight streams through the window@element_dog",
            "image_urls": [
              "https://static.aiquickdraw.com/tools/example/1764851002741_i0lEiI8I.png"
            ],
            "sound": true,
            "duration": "5",
            "aspect_ratio": "16:9",
            "mode": "pro",
            "multi_shots": false,
            "kling_elements": [
              {
                "name": "element_dog",
                "description": "dog",
                "element_input_urls": [
                  "https://tempfileb.aiquickdraw.com/kieai/market/1770361808044_4RfUUJrI.jpeg",
                  "https://tempfileb.aiquickdraw.com/kieai/market/1770361848336_ABQqRHBi.png"
                ]
              }
            ]
          }
        }

        ```


        ### Multi-Shot Video


        ```json

        {
          "model": "kling-3.0",
          "input": {
            "multi_shots": true,
            "image_urls": [
              "https://static.aiquickdraw.com/tools/example/1764851002741_i0lEiI8I.png"
            ],
            "duration": "5",
            "aspect_ratio": "16:9",
            "mode": "pro",
            "multi_prompt": [
              {
                "prompt": "a happy dog in running@element_cat",
                "duration": 3
              },
              {
                "prompt": "a happy dog play with a cat@element_dog",
                "duration": 3
              }
            ],
            "kling_elements": [
              {
                "name": "element_cat",
                "description": "cat",
                "element_input_urls": [ "https://tempfileb.aiquickdraw.com/kieai/market/1770361808044_4RfUUJrI.jpeg",    "https://tempfileb.aiquickdraw.com/kieai/market/1770361848336_ABQqRHBi.png"
                ]
              },
              {
                "name": "element_dog",
                "description": "dog",
                "element_input_urls": [ "https://tempfileb.aiquickdraw.com/kieai/market/1770361808044_4RfUUJrI.jpeg",    "https://tempfileb.aiquickdraw.com/kieai/market/1770361848336_ABQqRHBi.png"
                ]
              }
            ]
          }
        }

        ```


        ## Query Task Status


        After submitting a task, use the unified query endpoint to check
        progress and retrieve results:


        :::tip[Get Task Details]

        Learn how to query task status and retrieve generation results: [Get
        Task Details](/market/common/get-task-detail)

        :::


        :::tip[]

        For production use, we recommend using the `callBackUrl` parameter to
        receive automatic notifications when generation completes, rather than
        polling the status endpoint.

        :::


        ## Best Practices


        - **Prompt Writing**: Be specific and descriptive in your prompts.
        Include details about motion, camera angles, and scene composition

        - **Element Usage**: Use high-quality reference images/videos for better
        results. Ensure elements match the style and theme of your video

        - **Duration Planning**: For multi-shot videos, plan your shot durations
        to match the total video duration

        - **Mode Selection**: Use `pro` mode for final output when quality is
        important, and `std` mode for faster iterations

        - **Sound Effects**: Enable sound effects for more immersive videos,
        especially for action or dynamic scenes


        ## Related Resources


        <CardGroup cols={2}>
          <Card title="Market Overview" icon="lucide-store" href="/market/quickstart">
          </Card>
          <Card title="Common API" icon="lucide-cog" href="/common-api/get-account-credits">
          </Card>
        </CardGroup>
      operationId: kling-3.0
      tags:
        - docs/en/Market/Video Models/Kling
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
                    - kling-3.0/video
                  default: kling-3.0/video
                  description: >-
                    Generation mode. std has standard resolution, pro has higher
                    resolution.
                  examples:
                    - kling-3.0/video
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
                      type: string
                      description: >-
                        Video generation prompt. Takes effect when multi_shots
                        is false.
                      examples:
                        - >-
                          In a bright rehearsal room, sunlight streams through
                          the window@element_dog
                    image_urls:
                      type: array
                      items:
                        type: string
                        format: uri
                      description: >-
                        First and last frame image URLs. Required when elements
                        are referenced in the prompt (using @element_name
                        syntax). When multi_shots is false: if length is 2,
                        index 0 is the first frame and index 1 is the last
                        frame; if length is 1, the array item serves as the
                        first frame. When multi_shots is true: only the first
                        frame is supported.
                      examples:
                        - - >-
                            https://static.aiquickdraw.com/tools/example/1764851002741_i0lEiI8I.png
                    sound:
                      type: boolean
                      description: >-
                        Whether to enable sound effects. true enables sound
                        effects, false disables them. When multi_shots is true,
                        this field defaults to true.
                      default: false
                      examples:
                        - true
                    duration:
                      type: string
                      description: >-
                        Total video duration in seconds. Integer value, range: 3
                        to 15.
                      enum:
                        - '3'
                        - '4'
                        - '5'
                        - '6'
                        - '7'
                        - '8'
                        - '9'
                        - '10'
                        - '11'
                        - '12'
                        - '13'
                        - '14'
                        - '15'
                      default: '5'
                      examples:
                        - '5'
                    aspect_ratio:
                      type: string
                      description: >-
                        Video aspect ratio. Options: 16:9, 9:16, 1:1. When
                        image_urls(first and last frame images) is provided,
                        this parameter is optional and the aspect ratio will be
                        automatically adapted based on the uploaded images.
                      enum:
                        - '16:9'
                        - '9:16'
                        - '1:1'
                      default: '16:9'
                      examples:
                        - '16:9'
                    mode:
                      type: string
                      description: >-
                        Generation mode. std has standard resolution, pro has
                        higher resolution.


                        Resolution mapping:

                        - **std mode**: 16:9 (1280×720), 9:16 (720×1280), 1:1
                        (720×720)

                        - **pro mode**: 16:9 (1920×1080), 9:16 (1080×1920), 1:1
                        (1080×1080)
                      enum:
                        - std
                        - pro
                      default: pro
                      examples:
                        - pro
                    multi_shots:
                      type: boolean
                      description: >-
                        Whether to use multi-shot mode. true enables multi-shot
                        mode, false enables single-shot mode.
                      default: false
                      examples:
                        - false
                    multi_prompt:
                      type: array
                      description: >-
                        Shot prompts. Takes effect when multi_shots is true.
                        Used to describe the text and duration of each shot.
                        Supports up to 5 shots. Each shot duration is 1-12
                        seconds. If you need to use elements, add them after the
                        prompt.
                      items:
                        type: object
                        properties:
                          prompt:
                            type: string
                            description: >-
                              Prompt text for this shot, a maximum of 500
                              characters per shot. Each @element will occupy 37
                              characters.
                            examples:
                              - a happy dog in running@element_cat
                            maxLength: 500
                          duration:
                            type: integer
                            description: 'Duration of this shot in seconds. Range: 1-12.'
                            minimum: 1
                            maximum: 12
                            examples:
                              - 3
                        required:
                          - prompt
                          - duration
                        x-apidog-orders:
                          - prompt
                          - duration
                        x-apidog-ignore-properties: []
                      examples:
                        - - prompt: a happy dog in running@element_cat
                            duration: 3
                          - prompt: a happy dog play with a cat@element_dog
                            duration: 3
                    kling_elements:
                      type: array
                      items:
                        type: object
                        properties:
                          name:
                            type: string
                            description: >-
                              Element name, used in prompt with @ prefix (e.g.,
                              @element_dog)
                            examples:
                              - element_dog
                          description:
                            type: string
                            description: Element description
                            examples:
                              - dog
                          element_input_urls:
                            type: array
                            items:
                              type: string
                              format: uri
                            description: >-
                              Image URLs for the element. 2-4 URLs required.
                              Accepted formats: JPG, PNG. Maximum file size:
                              10MB per image.
                            examples:
                              - - >-
                                  https://tempfileb.aiquickdraw.com/kieai/market/1770361808044_4RfUUJrI.jpeg
                                - >-
                                  https://tempfileb.aiquickdraw.com/kieai/market/1770361848336_ABQqRHBi.png
                        required:
                          - name
                          - description
                        x-apidog-orders:
                          - name
                          - description
                          - element_input_urls
                        x-apidog-ignore-properties: []
                      description: >-
                        Referenced elements. Detailed information about elements
                        referenced in the prompt. A single task can reference a
                        maximum of three elements.
                      examples:
                        - - name: element_dog
                            description: dog
                            element_input_urls:
                              - >-
                                https://tempfileb.aiquickdraw.com/kieai/market/1770361808044_4RfUUJrI.jpeg
                              - >-
                                https://tempfileb.aiquickdraw.com/kieai/market/1770361848336_ABQqRHBi.png
                      maxItems: 3
                  required:
                    - prompt
                    - sound
                    - duration
                    - aspect_ratio
                    - mode
                    - multi_shots
                    - multi_prompt
                  x-apidog-orders:
                    - prompt
                    - image_urls
                    - sound
                    - duration
                    - aspect_ratio
                    - mode
                    - multi_shots
                    - multi_prompt
                    - kling_elements
                  x-apidog-ignore-properties: []
              x-apidog-orders:
                - model
                - callBackUrl
                - input
              x-apidog-ignore-properties: []
            example:
              model: kling-3.0/video
              callBackUrl: https://your-domain.com/api/callback
              input:
                prompt: >-
                  In a bright rehearsal room, sunlight streams through the
                  window@element_dog
                image_urls:
                  - >-
                    https://static.aiquickdraw.com/tools/example/1764851002741_i0lEiI8I.png
                sound: true
                duration: '5'
                aspect_ratio: '16:9'
                mode: pro
                multi_shots: false
                multi_prompt:
                  - prompt: a happy dog in running@element_cat
                    duration: 3
                  - prompt: a happy dog play with a cat@element_dog
                    duration: 3
                kling_elements:
                  - name: element_dog
                    description: dog
                    element_input_urls:
                      - >-
                        https://tempfileb.aiquickdraw.com/kieai/market/1770361808044_4RfUUJrI.jpeg
                      - >-
                        https://tempfileb.aiquickdraw.com/kieai/market/1770361848336_ABQqRHBi.png
                  - name: element_cat
                    description: cat
                    element_input_urls:
                      - https://your-cdn.com/element_image.jpg
                      - https://your-cdn.com/element_image2.jpg
      responses:
        '200':
          description: Request successful
          content:
            application/json:
              schema:
                allOf:
                  - type: object
                    properties: {}
                  - type: object
                    properties:
                      data:
                        type: object
                        properties:
                          taskId:
                            type: string
                            description: >-
                              Task ID, can be used with Get Task Details
                              endpoint to query task status
                            examples:
                              - task_kling-3.0_1765187774173
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
                  taskId: task_kling-3.0_1765187774173
          headers: {}
          x-apidog-name: ''
        '500':
          description: 请求失败
          content:
            application/json:
              schema:
                type: object
                properties: {}
                x-apidog-orders: []
                x-apidog-ignore-properties: []
          headers: {}
          x-apidog-name: Error
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
      x-apidog-folder: docs/en/Market/Video Models/Kling
      x-apidog-status: released
      x-run-in-apidog: https://app.apidog.com/web/project/1184766/apis/api-28506394-run
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