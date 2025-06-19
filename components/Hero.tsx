import { Button } from "@/components/ui/button";
import Image from "next/image";

const Hero = () => {
  return (
    <section className="relative overflow-hidden px-4 py-20 lg:py-32">
      <div className="absolute inset-0 bg-gradient-to-br from-purple-600/10 via-blue-600/5 to-indigo-600/10"></div>
      <div className="relative mx-auto max-w-7xl">
        <div className="text-center">
          
          <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl lg:text-6xl mb-6">
            Generate Viral Reels in
            <span className="bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent"> Seconds</span>
          </h1>
          
          <p className="mx-auto max-w-2xl text-xl text-gray-600 mb-10">
            Transform Reddit content into engaging video content with voiceover.
            No editing skills required.
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
            <div className="aspect-video rounded-2xl bg-gradient-to-br from-purple-100 to-blue-100 shadow-2xl overflow-hidden relative">
              <Image 
                src="/product_guide.png" 
                alt="Product Guide" 
                fill
                className="object-contain"
              />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
