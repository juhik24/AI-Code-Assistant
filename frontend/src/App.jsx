import { useState, useEffect } from "react";
import api from "./api";

import RepositoryCard from "./components/RepositoryCard";
import ChatInput from "./components/ChatInput";
import ChatMessage from "./components/ChatMessage";
import LoadingBubble from "./components/LoadingBubble";

function App() {
  const [messages, setMessages] = useState([]);

  const [loadingAnswer, setLoadingAnswer] = useState(false);
  const [loadingRepo, setLoadingRepo] = useState(false);

  const [status, setStatus] = useState("");
  const [repoIndexed, setRepoIndexed] = useState(false);
  const [progress, setProgress] = useState(null);

  const [sessionId, setSessionId] = useState(
    localStorage.getItem("session_id") || ""
  );


  useEffect(() => {
    if (!sessionId) {
      setMessages([]);
      return;
    }

    const loadHistory = async () => {
      try {
        const res = await api.get(`/history/${sessionId}`);
        setMessages(res.data.messages);
      } catch (err) {
        console.error("Failed to load chat history:", err);
      }
    };

    loadHistory();
  }, [sessionId]);

  useEffect(() => {
  if (!loadingRepo || !sessionId) return;

  const interval = setInterval(async () => {
    try {
      const res = await api.get(`/progress/${sessionId}`);

      setProgress(res.data);

      if (res.data.status === "completed") {
        clearInterval(interval);

        setLoadingRepo(false);
        setRepoIndexed(true);

        setStatus(
          `✅ Repository indexed successfully (${res.data.total} chunks)`
        );
      }
    } catch (err) {
      console.error(err);
    }
  }, 1000);

  return () => clearInterval(interval);
}, [loadingRepo, sessionId]);

  const clearChat = () => {
    setMessages([]);
  };

  const newChat = () => {
    setMessages([]);
    setSessionId("");
    setRepoIndexed(false);
    setStatus("");

    localStorage.removeItem("session_id");
  };

  const uploadZip = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  try {
    clearChat();

    setLoadingRepo(true);
    setRepoIndexed(false);
    setProgress(null);

    const res = await api.post("/upload", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    setSessionId(res.data.session_id);
    localStorage.setItem("session_id", res.data.session_id);

    setStatus("Repository uploaded. Indexing started...");
  } catch (err) {
    console.error(err);

    setLoadingRepo(false);
    setRepoIndexed(false);

    setStatus("❌ Failed to upload repository.");
  }
};

  const uploadGithub = async (repoUrl) => {
  try {
    clearChat();

    setLoadingRepo(true);
    setRepoIndexed(false);
    setProgress(null);

    const res = await api.post("/github", {
      repo_url: repoUrl,
    });

    setSessionId(res.data.session_id);
    localStorage.setItem("session_id", res.data.session_id);
    console.log("Session ID:", res.data.session_id);

    setStatus("Repository uploaded. Indexing started...");
  } catch (err) {
    console.error(err);

    setLoadingRepo(false);
    setRepoIndexed(false);

    setStatus("❌ Failed to index GitHub repository.");
  }
};

  const askQuestion = async (question) => {
    if (!sessionId) {
      alert("Please upload or index a repository first.");
      return;
    }

    const userMessage = {
      role: "user",
      content: question,
    };

    setMessages((prev) => [...prev, userMessage]);

    setLoadingAnswer(true);

    try {
      const res = await api.post("/chat", {
        session_id: sessionId,
        question,
      });

      const assistantMessage = {
        role: "assistant",
        content: res.data.answer,
        sources: res.data.sources,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      console.error(err);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Something went wrong while generating the response.",
          sources: [],
        },
      ]);
    } finally {
      setLoadingAnswer(false);
    }
  };

  return (
  <div className="min-h-screen bg-[#0f172a] text-white">

    {/* Header */}
    <header className="border-b border-slate-700 bg-[#111827]">
      <div className="max-w-6xl mx-auto h-16 flex items-center justify-between px-6">

        <div>
          <h1 className="text-2xl font-bold">
            Code Assistant
          </h1>

          <p className="text-sm text-slate-400">
            Chat with your codebase
          </p>
        </div>

        <div className="flex items-center gap-4">

        {repoIndexed && (
          <span className="flex items-center gap-2 text-green-400 text-sm font-medium">
            <span className="w-2 h-2 rounded-full bg-green-400"></span>
            Repository Indexed
          </span>
        )}

        {sessionId && (
          <button
            onClick={newChat}
            className="px-4 py-2 rounded-lg bg-slate-700 hover:bg-slate-600 transition"
          >
            + New Chat
          </button>
        )}

      </div>

      </div>
    </header>

    {/* Main */}

    <main className="max-w-5xl mx-auto flex flex-col h-[calc(100vh-64px)]">

      {/* Welcome */}

      {messages.length === 0 && (

        <div className="py-10">

          <div className="text-center mb-10">

            <h2 className="text-5xl font-bold">
              Welcome 👋
            </h2>

            <p className="mt-3 text-slate-400">
              Upload a repository and start asking questions.
            </p>

          </div>

          <RepositoryCard
            onZipUpload={uploadZip}
            onGithubUpload={uploadGithub}
            loading={loadingRepo}
            indexed={repoIndexed}
          />

          {loadingRepo && progress ? (
            <div className="mt-6 rounded-xl bg-slate-800 border border-slate-700 p-5">

              <p className="font-semibold text-lg">
                {progress.stage}
              </p>

              <div className="w-full bg-slate-700 rounded-full h-3 mt-4 overflow-hidden">
                <div
                  className="bg-blue-500 h-3 transition-all duration-300"
                  style={{ width: `${progress.percentage}%` }}
                />
              </div>

              <p className="mt-3 text-sm text-slate-300">
                {progress.completed} / {progress.total} chunks
              </p>

              <p className="text-sm text-slate-400 mt-1">
                {progress.percentage}% complete
              </p>

              {progress.status === "waiting" && (
                <p className="text-yellow-400 mt-2">
                  Processing is taking a little longer than usual...
                </p>
              )}
            </div>
          ) : (
            status && (
              <div
                className={`mt-6 rounded-xl px-4 py-3 text-sm ${
                  repoIndexed
                    ? "bg-green-500/10 border border-green-500/30 text-green-300"
                    : "bg-slate-800 border border-slate-700 text-slate-300"
                }`}
              >
                {status}
              </div>
            )
          )}

        </div>

      )}

      {/* Chat */}

      <div className="flex-1 overflow-y-auto py-8">

        {messages.map((message, index) => (
          <ChatMessage
            key={index}
            message={message}
          />
        ))}

        {loadingAnswer && <LoadingBubble />}

      </div>

      {/* Input */}

      <div className="sticky bottom-0 bg-[#0f172a] py-6">

        <ChatInput
          onSend={askQuestion}
          disabled={!sessionId}
          loading={loadingAnswer}
        />

      </div>

    </main>

  </div>
);

} 

export default App;