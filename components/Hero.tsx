import { Button } from "@/components/ui/button";
import { Play, Sparkles } from "lucide-react";

const Hero = () => {
  return (
    <section className="relative overflow-hidden px-4 py-20 lg:py-32">
      <div className="absolute inset-0 bg-gradient-to-br from-purple-600/10 via-blue-600/5 to-indigo-600/10"></div>
      <div className="relative mx-auto max-w-7xl">
        <div className="text-center">
          <div className="inline-flex items-center rounded-full bg-purple-100 px-4 py-2 text-sm font-medium text-purple-800 mb-8">
            <Sparkles className="mr-2 h-4 w-4" />
            The new way to go viral
          </div>
          
          <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl lg:text-6xl mb-6">
            Generate Viral Reels in
            <span className="bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent"> Seconds</span>
          </h1>
          
          <p className="mx-auto max-w-2xl text-xl text-gray-600 mb-10">
            Transform Reddit content into engaging video content with voiceover.
            No editing skills required – just pure creativity unleashed.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-16">
            <Button 
              size="lg" 
              className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white px-8 py-4 text-lg font-semibold rounded-xl shadow-lg hover:shadow-xl transition-all duration-300"
              onClick={() => window.location.href = '/generate-video'}
            >
              Generate Now
            </Button>
          </div>
          
          <div className="relative mx-auto max-w-4xl">
            <div className="aspect-video rounded-2xl bg-gradient-to-br from-purple-100 to-blue-100 shadow-2xl overflow-hidden">
              <div className="h-full w-full flex items-center justify-center">
                <div className="text-center">
                  <Play className="mx-auto h-16 w-16 text-purple-600 mb-4" />
                  <p className="text-lg font-medium text-gray-700">Product Demo Video</p>
                  <p className="text-sm text-gray-500">See AI reels in action</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
