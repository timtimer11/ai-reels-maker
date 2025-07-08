import { Button } from '@/components/ui/button';

const PredefinedPosts = ({ onGenerate }: { onGenerate: (url: string) => void }) => {
  const predefinedPosts = [
    {
      title: "If your phone is overheating, avoid force-closing background apps—it can actually make the CPU work harder and increase heat.",
      subreddit: "r/YouShouldKnow",
      url: "https://www.reddit.com/r/YouShouldKnow/comments/1lss7b5/ysk_if_your_phone_is_overheating_avoid/"
    },
    {
      title: "I stopped chasing the next big thing and finally made money",
      subreddit: "r/Entrepreneur", 
      url: "https://www.reddit.com/r/Entrepreneur/comments/1l0vuak/i_stopped_chasing_the_next_big_thing_and_finally/"
    },
    {
      title: "I dont think ai will ever be better than humans",
      subreddit: "r/CasualConversation",
      url: "https://www.reddit.com/r/CasualConversation/comments/1e91j0i/i_dont_think_ai_will_ever_be_better_than_humans/"
    }
  ];

  return (
    <div className="w-full max-w-2xl mx-auto">
      <h2 className="text-2xl font-semibold text-gray-900 mb-6 text-center">
        Try with these popular posts
      </h2>
      <div className="space-y-4">
        {predefinedPosts.map((post, index) => (
          <div key={index} className="bg-white border border-gray-200 rounded-lg p-4 shadow-sm">
            <h3 className="font-medium text-gray-900 mb-2">
              {post.title}
            </h3>
            <p className="text-sm text-gray-600 mb-3">{post.subreddit}</p>
            <Button 
              onClick={() => onGenerate(post.url)}
              className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white px-6 py-2 text-sm font-medium rounded-lg shadow-md hover:shadow-lg transition-all duration-300"
            >
              Try this
            </Button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PredefinedPosts; 