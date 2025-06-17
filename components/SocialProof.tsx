import { Star } from "lucide-react";

const testimonials = [
  {
    name: "Sarah Chen",
    role: "Content Creator",
    content: "This AI tool transformed my content strategy. I'm getting 10x more engagement!",
    rating: 5
  },
  {
    name: "Marcus Johnson",
    role: "Marketing Director",
    content: "Our team productivity increased by 300%. We're creating viral content daily now.",
    rating: 5
  },
  {
    name: "Emily Rodriguez", 
    role: "Influencer",
    content: "From 10K to 100K followers in 3 months. This tool is absolutely game-changing.",
    rating: 5
  }
];

const stats = [
  { value: "2M+", label: "Reels Created" },
  { value: "50K+", label: "Active Creators" },
  { value: "300%", label: "Avg. Engagement Boost" },
  { value: "4.9/5", label: "User Rating" }
];

const SocialProof = () => {
  return (
    <section className="py-20 px-4 bg-gray-50">
      <div className="mx-auto max-w-7xl">
        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-20">
          {stats.map((stat, index) => (
            <div key={index} className="text-center">
              <div className="text-3xl md:text-4xl font-bold text-gray-900 mb-2">
                {stat.value}
              </div>
              <div className="text-gray-600">{stat.label}</div>
            </div>
          ))}
        </div>

        {/* Testimonials */}
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl mb-4">
            Loved by creators worldwide
          </h2>
          <p className="text-xl text-gray-600">
            Join thousands of successful creators who are already using AI to scale their content
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {testimonials.map((testimonial, index) => (
            <div key={index} className="bg-white rounded-2xl p-6 shadow-sm">
              <div className="flex mb-4">
                {[...Array(testimonial.rating)].map((_, i) => (
                  <Star key={i} className="h-5 w-5 text-yellow-400 fill-current" />
                ))}
              </div>
              <p className="text-gray-700 mb-4 italic">
                &quot;{testimonial.content}&quot;
              </p>
              <div>
                <div className="font-semibold text-gray-900">{testimonial.name}</div>
                <div className="text-sm text-gray-500">{testimonial.role}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default SocialProof;
