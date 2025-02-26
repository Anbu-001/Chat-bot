import React, { useState, useRef } from "react";
import axios from "axios";
import RecordRTC from "recordrtc";

function App() {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorder = useRef(null);

  // Start recording audio
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder.current = new RecordRTC(stream, {
        type: "audio",
        mimeType: "audio/wav",
        recorderType: RecordRTC.StereoAudioRecorder,
        desiredSampRate: 16000,
      });

      mediaRecorder.current.startRecording();
      setIsRecording(true);
    } catch (err) {
      console.error("Error accessing microphone:", err);
    }
  };

  // Stop recording and send audio to backend
  const stopRecording = async () => {
    if (!mediaRecorder.current) return;

    mediaRecorder.current.stopRecording(async () => {
      const blob = mediaRecorder.current.getBlob();
      const formData = new FormData();
      formData.append("file", blob, "audio.wav");

      setIsRecording(false);

      try {
        const res = await axios.post("http://backend:8000/speech-to-text/", formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });

        if (res.data.text) {
          setMessage(res.data.text);
          handleSendMessage(res.data.text);
        } else {
          console.error("Speech recognition failed:", res.data.error);
          setMessage("Speech recognition failed.");
        }
      } catch (err) {
        console.error("Error sending audio:", err);
        setMessage("Error processing audio.");
      }
    });
  };

  // Send text message to chatbot
  const handleSendMessage = async (text) => {
    try {
      const res = await axios.post("http://backend:8000/chat/", { text });
      setResponse(res.data.response);
    } catch (err) {
      console.error("Error fetching chatbot response:", err);
      setResponse("Error getting chatbot response.");
    }
  };

  return (
    <div style={{ textAlign: "center", padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1>Speech-to-Text Chatbot</h1>
      
      <button 
        onClick={startRecording} 
        disabled={isRecording} 
        style={{
          padding: "10px 20px",
          fontSize: "16px",
          margin: "10px",
          cursor: "pointer",
          backgroundColor: isRecording ? "#ccc" : "#28a745",
          color: "white",
          border: "none",
          borderRadius: "5px"
        }}>
        🎙 Start Recording
      </button>

      <button 
        onClick={stopRecording} 
        disabled={!isRecording} 
        style={{
          padding: "10px 20px",
          fontSize: "16px",
          margin: "10px",
          cursor: "pointer",
          backgroundColor: !isRecording ? "#ccc" : "#dc3545",
          color: "white",
          border: "none",
          borderRadius: "5px"
        }}>
        ⏹ Stop Recording
      </button>

      <p><strong>You said:</strong> {message}</p>
      <p><strong>Chatbot:</strong> {response}</p>
    </div>
  );
}

export default App;
