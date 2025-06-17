import { Button } from "@/components/ui/button";
import { Check, Crown, Rocket } from "lucide-react";

const plans = [
  {
    name: "Starter",
    price: "Free",
    description: "Perfect for trying out AI reel creation",
    features: [
      "5 reels per month",
      "Basic AI templates",
      "720p export quality",
      "Watermark included",
      "Community support"
    ],
    cta: "Start Free",
    popular: false
  },
  {
    name: "Creator",
    price: "$19",
    period: "/month",
    description: "For serious content creators and small businesses",
    features: [
      "100 reels per month",
      "Premium AI templates",
      "4K export quality",
      "No watermark",
      "Custom branding",
      "Priority support",
      "Analytics dashboard"
    ],
    cta: "Start Creating",
    popular: true
  },
  {
    name: "Agency",
    price: "$49",
    period: "/month", 
    description: "For agencies and teams managing multiple accounts",
    features: [
      "Unlimited reels",
      "Advanced AI features",
      "White-label solution",
      "Team collaboration",
      "API access",
      "Dedicated account manager",
      "Custom integrations"
    ],
    cta: "Contact Sales",
    popular: false
  }
];

const Pricing = () => {
  return (
    <section className="py-20 px-4" id="pricing">
      <div className="mx-auto max-w-7xl">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl mb-4">
            Simple, transparent pricing
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Choose the perfect plan to scale your content creation. 
            All plans include our core AI features.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {plans.map((plan, index) => (
            <div 
              key={index}
              className={`relative rounded-2xl p-8 ${
                plan.popular 
                  ? 'bg-gradient-to-b from-purple-50 to-blue-50 border-2 border-purple-200 shadow-lg' 
                  : 'bg-white border border-gray-200 shadow-sm'
              }`}
            >
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                  <div className="inline-flex items-center rounded-full bg-gradient-to-r from-purple-600 to-blue-600 px-4 py-2 text-sm font-medium text-white">
                    <Crown className="mr-1 h-4 w-4" />
                    Most Popular
                  </div>
                </div>
              )}

              <div className="text-center mb-8">
                <h3 className="text-2xl font-bold text-gray-900 mb-2">{plan.name}</h3>
                <div className="mb-4">
                  <span className="text-4xl font-bold text-gray-900">{plan.price}</span>
                  {plan.period && <span className="text-gray-500">{plan.period}</span>}
                </div>
                <p className="text-gray-600">{plan.description}</p>
              </div>

              <ul className="space-y-4 mb-8">
                {plan.features.map((feature, featureIndex) => (
                  <li key={featureIndex} className="flex items-center">
                    <Check className="h-5 w-5 text-green-500 mr-3 flex-shrink-0" />
                    <span className="text-gray-700">{feature}</span>
                  </li>
                ))}
              </ul>

              <Button 
                className={`w-full py-3 text-lg font-semibold rounded-xl transition-all duration-300 ${
                  plan.popular
                    ? 'bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white shadow-lg hover:shadow-xl'
                    : 'bg-gray-900 hover:bg-gray-800 text-white'
                }`}
              >
                {plan.popular && <Rocket className="mr-2 h-5 w-5" />}
                {plan.cta}
              </Button>
            </div>
          ))}
        </div>

        <div className="text-center mt-12">
          <p className="text-gray-600">
            All plans include a 14-day free trial. No credit card required. 
            <span className="text-purple-600 font-medium"> Cancel anytime.</span>
          </p>
        </div>
      </div>
    </section>
  );
};

export default Pricing;
