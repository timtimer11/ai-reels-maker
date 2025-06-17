import { Zap, Brain, Palette, TrendingUp, Clock, Share2 } from "lucide-react";

const features = [
  {
    icon: Brain,
    title: "AI-Powered Generation",
    description: "Advanced AI analyzes trends and creates engaging content tailored to your audience"
  },
  {
    icon: Zap,
    title: "Lightning Fast",
    description: "Generate professional reels in under 30 seconds with our optimized AI engine"
  },
  {
    icon: Palette,
    title: "Custom Branding",
    description: "Apply your brand colors, fonts, and style to maintain consistent visual identity"
  },
  {
    icon: TrendingUp,
    title: "Viral Optimization",
    description: "Built-in algorithms optimize your content for maximum engagement and reach"
  },
  {
    icon: Clock,
    title: "Schedule & Automate",
    description: "Plan and schedule your content across multiple platforms automatically"
  },
  {
    icon: Share2,
    title: "Multi-Platform Export",
    description: "Export in perfect formats for Instagram, TikTok, YouTube Shorts, and more"
  }
];

const Features = () => {
  return (
    <section className="py-20 px-4" id="features">
      <div className="mx-auto max-w-7xl">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl mb-4">
            Everything you need to go viral
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Powerful features designed to help creators, businesses, and influencers 
            create engaging content that drives results.
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
