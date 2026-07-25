export default function LoadingBubble() {
  return (
    <div className="flex justify-start my-6">
      <div className="bg-white border border-gray-200 rounded-2xl px-5 py-4 shadow-sm">
        <div className="flex gap-2">

          <div className="w-2 h-2 rounded-full bg-blue-500 animate-bounce"></div>

          <div
            className="w-2 h-2 rounded-full bg-blue-500 animate-bounce"
            style={{ animationDelay: "0.15s" }}
          ></div>

          <div
            className="w-2 h-2 rounded-full bg-blue-500 animate-bounce"
            style={{ animationDelay: "0.3s" }}
          ></div>

        </div>
      </div>
    </div>
  );
}