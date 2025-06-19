import { Button } from "@/components/ui/button";
import { ArrowRight, Sparkles } from "lucide-react";

const CTA = () => {
  return (
    <section className="relative py-20 px-4">
      <div className="absolute inset-0 bg-gradient-to-br from-purple-600/10 via-blue-600/5 to-indigo-600/10"></div>
      <div className="relative mx-auto max-w-4xl">
        <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-purple-600 via-blue-600 to-indigo-700 p-12 text-center shadow-2xl">
          <div className="absolute inset-0 bg-black/10"></div>
          <div className="relative">
            
          <h2 className="text-2xl font-bold text-white sm:text-4xl lg:text-4xl mb-6">
            Ready to experiment?
          </h2>

          <p className="text-xl text-white/90 mb-8 max-w-2xl mx-auto">
          Try for free and see how AI can help you turn content into short clips.
          </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button 
                size="lg" 
                className="bg-white text-purple-600 hover:bg-gray-100 px-8 py-4 text-lg font-semibold rounded-xl shadow-lg hover:shadow-xl transition-all duration-300"
                onClick={() => window.location.href = '/generate-video'}
              >
                Try Now
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </div>
            
            <p className="text-white/80 text-sm mt-6">
              ✨ Completely for free • 🚀 3 generations per day
            </p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default CTA;
