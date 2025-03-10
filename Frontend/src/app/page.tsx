"use client";
import { useState } from 'react';
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import ReactMarkdown from 'react-markdown';
import axios from 'axios';
export default function Home() {
  const [markdown, setMarkdown] = useState('');
  const [Newmarkdown, setNewMarkdown] = useState('');

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setMarkdown(event.target.value);
  };



  const handleSubmit = () => {
      const api_url = "http://127.0.0.1:8000/generate_readme/"+ String(markdown);
      axios.post(api_url)
      .then((response) => {
          const res = response.data.readme;
          const string = res.replace(/\\n/g, '\n');
          setNewMarkdown(string);
      }
      )
      .catch((error) => {
          console.log(error);
      }
      );
    };

  return (
    <>
      <div className="grid grid-cols-2 gap-4 p-4">
        <div>
          <Input 
            type="text" 
            placeholder="Add GitHub URL" 
            value={markdown} 
            onChange={handleInputChange} 
          />
          <Button onClick={handleSubmit}>Submit</Button>
        </div>
        <div>
          <h2 className="text-lg font-bold mb-2">Preview</h2>
          <div className="border border-gray-300 rounded-lg p-4 bg-gray-100 min-h-64">
            <ReactMarkdown>{Newmarkdown}</ReactMarkdown>
          </div>
        </div>
      </div>
    </>
  );
}