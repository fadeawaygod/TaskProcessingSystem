# Sequence Diagram
## Table of Contents
- API Sequence Diagram
  - [Table of Contents](#table-of-contents)
  - [Export Meeting Note to Google Drive](#export-meeting-note-to-google-drive)
  - [Import Meeting Audio](#import-meeting-audio)
  - [Create Meetings by Audio](#create-meetings-by-audio)
  
---
## Export Meeting Note to Google Drive
```mermaid
sequenceDiagram
    participant Web Client
    participant API Server
    participant DB
    participant Google Server
    Web Client->>+API Server: GET workspaces/{workspace_id}/integrations?type=GOOGLE_DRIVE
    API Server->>-Web Client: integrations
    opt if there is no Google Drive integration
        Web Client->>Web Client: user google login with google js libaray to get the authorization code
        Web Client->>+API Server: PUT workspaces/{workspace_id}/integrations/google_drive with authorization code
        API Server->>+Google Server: POST oauth2.googleapis.com/token to get id token
        Google Server->>-API Server: id tokens
        API Server->>DB: save refresh token
        API Server->>-Web Client: integration&access token
        Web Client->>Web Client: user select Google drive folder with google js libaray to get folder id
        Web Client->>+API Server: POST workspaces/{workspace_id}/google_drive/append_folder with folder id&name
        API Server->>DB: save folder id&name
        API Server->>-Web Client: ok
    end
    Web Client->>+API Server: POST workspaces/{workspace_id}/meetings/{meeting_id}/sync_to_google_drive
    API Server->>Google Server: COPY the public template to users folder 
    API Server->>Google Server: relpace place holders 
    API Server->>-Web Client: ok

```


## Import Meeting Audio
```mermaid
sequenceDiagram
    Client->>+APIServer: POST /workspaces/{workspace_id}/meetings
    APIServer-->>-Client: ok 
    Client->>+APIServer: POST /workspaces/{workspace_id}/meetings/{meeting_id}/upload_audio_url <br> with file name
    APIServer-->>-Client: ok with upload_audio_url presign_url
    Client->>+S3Server: upload meeting audio with presign_url
    S3Server-->>-Client: ok
    Client->>+APIServer: POST /workspaces/{workspace_id}/meetings/{meeting_id}/analyze_audio
    APIServer-->>-Client: job payload
    APIServer->>+Worker: create a job and publish an event to internal queue
    Worker-->>Worker: processing
    Worker->>+DashBoardNLPServer: analyze
    DashBoardNLPServer->>-Worker: ok

    Client->>+APIServer: Get jobs/{job_id}
    APIServer-->>-Client: job payload

    DashBoardNLPServer->>+APIServer: dashboard analysis result callback
    opt if the callback URL is set in workspace integration
      APIServer->>+ClientCallbackServer: analyze result&job result
      ClientCallbackServer->>-APIServer: ok    
   end
    APIServer->>-DashBoardNLPServer: ok

```

## Create Meetings by Audio
```mermaid
sequenceDiagram
    Client->>+APIServer: POST /workspaces/{workspace_id}/generate_folder_presigned_post
    APIServer-->>-Client: ok with presigned urls
    Client->>+S3Server: upload several meeting wav files with presigned urls
    S3Server-->>-Client: ok
    Client->>+APIServer: POST /workspaces/{workspace_id}/create_meetings_by_audio
    APIServer-->>-Client: job payload
    APIServer->>+Worker: create a job and publish an event to internal queue
    Worker-->>Worker: processing
    Worker->>+DashBoardNLPServer: analyze meetings sequentially
    DashBoardNLPServer->>-Worker: ok

    Client->>+APIServer: Get jobs/{job_id}
    APIServer-->>-Client: job payload

    DashBoardNLPServer->>+APIServer: dashboard analysis result callback
    opt if the callback URL is set in workspace integration
      APIServer->>+ClientCallbackServer: analyze result&job result
      ClientCallbackServer->>-APIServer: ok    
   end
    APIServer->>-DashBoardNLPServer: ok

```