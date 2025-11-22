import React, { useState } from 'react';
import axios from 'axios';
import { Upload, Search, Clock, Loader2 } from 'lucide-react';

const API_URL = "http://localhost:8000";

export default function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState("");
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setStatus("Uploading & Processing Video (This uses CPU/GPU)...");
    
    const formData = new FormData();
    formData.append("file", file);

    try {
      await axios.post(`${API_URL}/upload_video`, formData);
      setStatus("Ready! Ask me anything about the video.");
    } catch (error) {
      setStatus("Error processing video.");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!query) return;
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append("query", query);
      const res = await axios.post(`${API_URL}/search`, formData);
      setResults(res.data.results);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8 font-sans">
      <div className="max-w-3xl mx-auto space-y-8">
        
        {/* Header */}
        <div className="text-center space-y-2">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
            Video Intelligence Agent
          </h1>
          <p className="text-gray-400">Upload a video and ask complex questions using AI.</p>
        </div>

        {/* Upload Section */}
        <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow-lg">
          <div className="flex items-center gap-4">
            <input 
              type="file" 
              accept="video/*"
              onChange={(e) => setFile(e.target.files[0])}
              className="block w-full text-sm text-gray-400
                file:mr-4 file:py-2 file:px-4
                file:rounded-full file:border-0
                file:text-sm file:font-semibold
                file:bg-blue-600 file:text-white
                hover:file:bg-blue-700"
            />
            <button 
              onClick={handleUpload}
              disabled={loading || !file}
              className="flex items-center gap-2 bg-green-600 px-4 py-2 rounded-lg font-medium hover:bg-green-700 disabled:opacity-50 transition-colors"
            >
              {loading ? <Loader2 className="animate-spin" size={18} /> : <Upload size={18} />}
              Process
            </button>
          </div>
          {status && <p className="mt-4 text-sm text-blue-300 animate-pulse">{status}</p>}
        </div>

        {/* Search Section */}
        <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 shadow-lg">
          <div className="flex gap-2">
            <input 
              type="text" 
              placeholder="e.g., 'Find frame with 3 people' or 'When did the car appear?'"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
              className="flex-1 bg-gray-900 border border-gray-600 rounded-lg px-4 py-3 focus:ring-2 focus:ring-blue-500 outline-none text-white placeholder-gray-500"
            />
            <button 
              onClick={handleSearch}
              className="bg-blue-600 px-6 rounded-lg hover:bg-blue-700 transition-colors text-white"
            >
              <Search size={20} />
            </button>
          </div>
        </div>

        {/* Results Section */}
        <div className="space-y-4">
          {results.map((res, index) => (
            <div key={index} className="bg-gray-800 p-4 rounded-lg border border-gray-700 flex items-center justify-between hover:bg-gray-750 transition">
              <div className="flex items-center gap-4">
                <div className="bg-gray-700 p-3 rounded-full text-blue-400">
                  <Clock size={20} />
                </div>
                <div>
                  <p className="font-bold text-lg text-blue-300">
                    {new Date(res.timestamp * 1000).toISOString().substr(14, 5)}
                    <span className="text-sm text-gray-500 ml-2">({Math.round(res.timestamp)}s)</span>
                  </p>
                  <p className="text-gray-400 text-sm">{res.description || "Visual match found"}</p>
                </div>
              </div>
              <div className="text-xs text-gray-500 bg-gray-900 px-2 py-1 rounded">
                Match Score: {res.score.toFixed(3)}
              </div>
            </div>
          ))}
          {results.length === 0 && query && !loading && (
            <p className="text-center text-gray-500 mt-4">No relevant moments found.</p>
          )}
        </div>

      </div>
    </div>
  );
}
