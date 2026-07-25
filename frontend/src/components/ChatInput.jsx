import { useState } from "react";
import { ArrowUp } from "lucide-react";

export default function ChatInput({
  onSend,
  disabled = false,
  loading = false,
}) {
  const [message, setMessage] = useState("");

  const handleSend = () => {
    if (!message.trim() || loading || disabled) return;

    onSend(message);
    setMessage("");
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="bg-[#1e293b] border border-slate-700 rounded-3xl px-3">
      <div className="flex items-end gap-3">

        <textarea
          rows={2}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask anything about your repository..."
          className="flex-1 resize-none outline-none bg-transparent text-white placeholder:text-slate-500"
          disabled={disabled || loading}
        />

        <button
          onClick={handleSend}
          disabled={disabled || loading || !message.trim()}
          className="w-11 h-11 rounded-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white flex items-center justify-center transition"
        >
          <ArrowUp size={18} />
        </button>

      </div>
    </div>
  );
}