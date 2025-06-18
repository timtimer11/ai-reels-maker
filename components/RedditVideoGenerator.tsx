import { useState } from 'react';
import { Button } from '@/components/ui/button';

const RedditVideoGenerator = ({ onGenerate }: { onGenerate: (url: string) => void }) => {
  const [redditUrl, setRedditUrl] = useState("");

  const isValidRedditUrl = (url: string) => {
    if (!url) return false;
    return url.includes('reddit.com/r/') && url.includes('/comments/');
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      {/* Input field for Reddit URL */}
      <div className="w-full mb-4">
        <input
          type="text"
          value={redditUrl}
          onChange={(e) => setRedditUrl(e.target.value)}
          placeholder="https://www.reddit.com/r/.../comments/..."
          className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500"
        />
      </div>

      {/* Generate button */}
      <Button 
        onClick={() => onGenerate(redditUrl)}
        className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white px-8 py-4 text-lg font-semibold rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 w-full"
        disabled={!isValidRedditUrl(redditUrl)}
      >
        Generate Video
      </Button>
    </div>
  );
};

export default RedditVideoGenerator; 