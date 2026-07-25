import { useState } from "react";
import {
  UploadCloud,
  Globe,
  ArrowRight,
  CheckCircle2,
} from "lucide-react";

export default function RepositoryCard({
  onZipUpload,
  onGithubUpload,
  loading,
  indexed,
}) {
  const [mode, setMode] = useState("zip");
  const [selectedFile, setSelectedFile] = useState(null);
  const [repoUrl, setRepoUrl] = useState("");

  const handleSubmit = () => {
    if (loading) return;

    if (mode === "zip") {
      if (!selectedFile) {
        alert("Please select a ZIP file.");
        return;
      }

      onZipUpload(selectedFile);
    } else {
      if (!repoUrl.trim()) {
        alert("Please enter a GitHub repository URL.");
        return;
      }

      onGithubUpload(repoUrl);
    }
  };

  return (
    <div className="w-full bg-slate-800 border border-slate-700 rounded-3xl shadow-xl overflow-hidden">

      {/* Header */}

      <div className="px-8 pt-8">

        <h2 className="text-2xl font-semibold text-white">
          Upload Repository
        </h2>

        <p className="text-slate-400 mt-2">
          Index a ZIP project or connect a GitHub repository.
        </p>

      </div>

      {/* Success Banner */}

      {indexed && (
        <div className="mx-8 mt-6 rounded-xl border border-green-500/30 bg-green-500/10 p-4">

          <div className="flex items-center gap-3">

            <CheckCircle2
              size={22}
              className="text-green-400"
            />

            <div>

              <p className="font-semibold text-green-300">
                Repository Indexed Successfully
              </p>

              <p className="text-sm text-slate-300 mt-1">
                You can now ask questions about your code.
              </p>

            </div>

          </div>

        </div>
      )}

      {/* Toggle */}

      <div className="px-8 mt-8">

        <div className="grid grid-cols-2 bg-slate-700 rounded-xl p-1">

          <button
            disabled={loading}
            onClick={() => setMode("zip")}
            className={`py-3 rounded-lg transition ${
              mode === "zip"
                ? "bg-blue-600 text-white"
                : "text-slate-300 hover:bg-slate-600"
            }`}
          >
            ZIP Upload
          </button>

          <button
            disabled={loading}
            onClick={() => setMode("github")}
            className={`py-3 rounded-lg transition ${
              mode === "github"
                ? "bg-blue-600 text-white"
                : "text-slate-300 hover:bg-slate-600"
            }`}
          >
            GitHub
          </button>

        </div>

      </div>

      {/* Body */}

      <div className="p-8">

        {mode === "zip" ? (
          <label className="block cursor-pointer">

            <input
              type="file"
              accept=".zip"
              className="hidden"
              disabled={loading}
              onChange={(e) => setSelectedFile(e.target.files[0])}
            />

            <div className="h-56 border-2 border-dashed border-slate-600 hover:border-blue-500 rounded-2xl transition flex flex-col justify-center items-center">

              <UploadCloud
                size={58}
                className="text-blue-400"
              />

              <div className="mt-5 text-lg font-medium text-white">
                {selectedFile
                  ? selectedFile.name
                  : "Drop ZIP here"}
              </div>

              <div className="mt-2 text-sm text-slate-400">
                or click to browse
              </div>

            </div>

          </label>
        ) : (
          <div>

            <label className="text-sm text-slate-400 mb-2 block">
              Repository URL
            </label>

            <div className="flex items-center bg-slate-900 border border-slate-600 rounded-xl px-4">

              <Globe
                size={18}
                className="text-slate-500"
              />

              <input
                value={repoUrl}
                disabled={loading}
                onChange={(e) => setRepoUrl(e.target.value)}
                placeholder="https://github.com/user/repository"
                className="flex-1 bg-transparent outline-none py-4 px-3 text-white placeholder:text-slate-500"
              />

            </div>

          </div>
        )}

      </div>

      {/* Footer */}

      <div className="border-t border-slate-700 px-8 py-6">

        <button
          onClick={handleSubmit}
          disabled={loading}
          className="w-full h-14 rounded-xl text-white font-semibold flex items-center justify-center gap-3 transition disabled:opacity-60 bg-blue-600 hover:bg-blue-700"
        >
          {loading ? (
            <>
              <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
              Indexing Repository...
            </>
          ) : indexed ? (
            <>
              <CheckCircle2 size={20} />
              Indexed Successfully
            </>
          ) : (
            <>
              Index Repository
              <ArrowRight size={18} />
            </>
          )}
        </button>

      </div>

    </div>
  );
}