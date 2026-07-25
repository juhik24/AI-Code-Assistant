import ReactMarkdown from "react-markdown";
import { Bot, User, FileText } from "lucide-react";

export default function ChatMessage({ message }) {
  const isUser = message.role === "user";

  return (
    <div
      className={`flex mb-8 ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >
      <div
        className={`flex gap-4 max-w-4xl ${
          isUser ? "flex-row-reverse" : ""
        }`}
      >
        {/* Avatar */}
        <div
          className={`w-10 h-10 rounded-full flex items-center justify-center shrink-0 ${
            isUser
              ? "bg-blue-600 text-white"
              : "bg-slate-700 text-white"
          }`}
        >
          {isUser ? <User size={18} /> : <Bot size={18} />}
        </div>

        {/* Message Bubble */}
        <div
          className={`rounded-2xl px-6 py-5 border shadow-sm ${
            isUser
              ? "bg-blue-600 border-blue-600 text-white"
              : "bg-white border-gray-200"
          }`}
        >
          {/* Markdown */}
          <div
            className={`leading-7 whitespace-pre-wrap ${
              isUser ? "text-white" : "text-gray-900"
            }`}
          >
            <ReactMarkdown
              components={{
                p: ({ children }) => (
                  <p className="mb-3">{children}</p>
                ),
                ul: ({ children }) => (
                  <ul className="list-disc ml-5 mb-3">
                    {children}
                  </ul>
                ),
                ol: ({ children }) => (
                  <ol className="list-decimal ml-5 mb-3">
                    {children}
                  </ol>
                ),
                code: ({ children }) => (
                  <code className="bg-gray-100 text-red-600 rounded px-1 py-0.5">
                    {children}
                  </code>
                ),
              }}
            >
              {message.content}
            </ReactMarkdown>
          </div>

          {/* Sources */}
          {!isUser &&
            message.sources &&
            message.sources.length > 0 && (
              <>
                <div className="mt-5 pt-4 border-t border-gray-200">

                  <div className="text-sm font-semibold text-gray-700 mb-3">
                    Sources
                  </div>

                  <div className="flex flex-wrap gap-2">
                    {message.sources.map((source) => (
                      <div
                        key={source}
                        className="flex items-center gap-2 bg-gray-100 rounded-full px-3 py-1 text-sm text-gray-700"
                      >
                        <FileText size={14} />
                        {source.split("/").pop()}
                      </div>
                    ))}
                  </div>

                </div>
              </>
            )}
        </div>
      </div>
    </div>
  );
}