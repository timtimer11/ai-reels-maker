import { Zap, Brain, Palette } from "lucide-react";

const features = [
  {
    icon: Brain,
    title: "Smart Content Extraction",
    description: "Just paste a link to Reddit post and AI will grab the best parts to turn them into a scroll-stopping content"
  },
  {
    icon: Zap,
    title: "No Editing, No Extra Tools",
    description: "Skip the hassle of generating voiceovers and stitching them with video clips - it's all handled in single click"
  },
  {
    icon: Palette,
    title: "Ready for Reels & TikTok",
    description: "Auto-captions and sticky background video work together to boost watch time"
  }
];


const Features = () => {
  return (
    <section className="py-20 px-4" id="features">
      <div className="mx-auto max-w-7xl">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl mb-4">
           Turn Reddit posts into engaging videos
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Built for creators who want an easier way to turn Reddit content into short-form content.
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div 
              key={index} 
              className="group p-6 rounded-2xl bg-white shadow-sm hover:shadow-lg transition-all duration-300 border border-gray-100 hover:border-purple-200"
            >
              <div className="mb-4">
                <div className="inline-flex p-3 rounded-xl bg-gradient-to-br from-purple-100 to-blue-100 group-hover:from-purple-200 group-hover:to-blue-200 transition-all duration-300">
                  <feature.icon className="h-6 w-6 text-purple-600" />
                </div>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                {feature.title}
              </h3>
              <p className="text-gray-600">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Features;
