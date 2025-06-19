import { Linkedin } from "lucide-react";

const Footer = () => {
  return (
    <footer className="bg-gray-900 text-white py-12 px-4">
      <div className="mx-auto max-w-7xl">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div>
            <h3 className="text-2xl font-bold mb-4 bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
              AI Reels Maker
            </h3>
            <p className="text-gray-400 mb-6 max-w-md">
              Made for fun. Don&apos;t get mad if one day the app is down.
            </p>
            <div className="flex space-x-4">
              <a href="https://www.linkedin.com/in/timur-kulbuzhev/" target="_blank" rel="noopener noreferrer">
                <Linkedin className="h-6 w-6 text-gray-400 hover:text-white cursor-pointer transition-colors" />
              </a>
            </div>
          </div>
          
          <div>
            <h4 className="font-semibold mb-4">Contact</h4>
            <ul className="space-y-2 text-gray-400">
              <li 
                className="hover:text-white cursor-pointer transition-colors"
                onClick={() => window.location.href = '/contact'}
              >
                Contact Us (Me)
              </li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-gray-800 mt-12 pt-8 text-center text-gray-400">
          <p>&copy; 2024 AI Reels Maker. All rights reserved (trust me bro)</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
