"use client";
import { useState } from 'react';
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import axios from 'axios';
import Loader from '@/components/Loader'; // Import the custom loader
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Clipboard, Check } from "lucide-react";

export default function Home() {
  const [markdown, setMarkdown] = useState('');
  const [copied, setCopied] = useState(false);
  const [Newmarkdown, setNewMarkdown] = useState('');
  const [loading, setLoading] = useState(false);

  const handleInputChange = (event) => {
    setMarkdown(event.target.value);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(Newmarkdown).then(() => {
      setCopied(true);

      setTimeout(() => setCopied(false), 2000); // Reset after 2 sec
    });
  };

  const handleSubmit = () => {
    setLoading(true);
    const api_url = "http://127.0.0.1:8000/generate_readme/" + String(markdown);
    axios.post(api_url)
      .then((response) => {
        const res = response.data.readme;
        const string = res.replace(/\\n/g, '\n');
        setNewMarkdown(string);
        setLoading(false);
        console.log(string);
      })
      .catch((error) => {
        console.log(error);
        setLoading(false); // Reset loading state in case of error
      });
  };

  return (
    <>
      {loading && <Loader />} {/* Show loader when loading */}
      <div className='border-b-4 border-Black-500'>
        <div className='p-10 text-4xl font-bold'>
          <h1 className='cursor-pointer text-4xl font-bold'>Auto Doc AI</h1>
        </div>
      </div>
      <div className="flex flex-col items-center justify-center min-h-screen px-4">
        <div className="w-full max-w-2xl">
          <Input
            type="text"
            placeholder="Add GitHub URL"
            value={markdown}
            onChange={handleInputChange}
            className="mb-4 w-full"
          />
          <Button onClick={handleSubmit} className="w-full">Submit</Button>
        </div>
        <div className="w-full max-w-2xl mt-8 relative">
          <h2 className="text-lg font-bold mb-2 text-center">Preview</h2>
          <div className="border border-gray-300 rounded-lg p-4 bg-gray-100 min-h-64 relative">
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              children={Newmarkdown}
            />
            {/* Copy Button */}
            <Button
              onClick={handleCopy}
              variant="outline"
              size="icon"
              className="absolute top-2 right-2"
            >
              {copied ? <Check className="w-5 h-5 text-green-500" /> : <Clipboard className="w-5 h-5" />}
            </Button>
          </div>
        </div>
      </div>
    </>
  );
}