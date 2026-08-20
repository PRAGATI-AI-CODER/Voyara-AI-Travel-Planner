export default function Hero() {
  return (
    <section className="relative flex min-h-screen items-center justify-center overflow-hidden bg-[#f7f8f4] px-6 py-20">
      <div className="absolute inset-0 -z-0 bg-[radial-gradient(circle_at_20%_20%,rgba(120,160,120,0.12),transparent_30%),radial-gradient(circle_at_80%_70%,rgba(80,130,160,0.10),transparent_30%)]" />

      <div className="relative z-10 mx-auto flex w-full max-w-5xl flex-col items-center text-center">
        <div className="mb-6 inline-flex items-center rounded-full border border-black/10 bg-white/70 px-4 py-2 text-sm font-medium text-gray-700 backdrop-blur">
          <span className="mr-2">✦</span>
          AI-powered travel intelligence
        </div>

        <h1 className="max-w-4xl text-5xl font-semibold tracking-tight text-gray-900 sm:text-6xl lg:text-7xl">
          Your journey,
          <span className="block text-gray-500">
            intelligently planned.
          </span>
        </h1>

        <p className="mt-6 max-w-2xl text-lg leading-8 text-gray-600 sm:text-xl">
          Tell Voyara where you want to go, what you love, and how you want
          to travel. We&apos;ll turn it into a journey built around you.
        </p>

        <div className="mt-10 flex flex-col gap-4 sm:flex-row">
          <a
            href="#trip-planner"
            className="rounded-full bg-gray-900 px-7 py-3.5 text-sm font-semibold text-white transition hover:bg-gray-700"
          >
            Start planning <span className="ml-1">→</span>
          </a>

          <a
            href="#trip-planner"
            className="rounded-full border border-gray-300 bg-white px-7 py-3.5 text-sm font-semibold text-gray-700 transition hover:bg-gray-50"
          >
            Explore Voyara
          </a>
        </div>

        <div className="mt-16 grid w-full max-w-3xl grid-cols-1 gap-4 text-left sm:grid-cols-3">
          <Feature
            title="Personalized"
            description="Plans shaped around your interests, budget, and travel style."
          />

          <Feature
            title="Context-aware"
            description="Uses travel knowledge and relevant information to build better plans."
          />

          <Feature
            title="Intelligent"
            description="Designed to reason about destinations, constraints, and itineraries."
          />
        </div>
      </div>
    </section>
  );
}

function Feature({
  title,
  description,
}: {
  title: string;
  description: string;
}) {
  return (
    <div className="rounded-2xl border border-black/10 bg-white/70 p-5 shadow-sm backdrop-blur transition duration-300 hover:-translate-y-1 hover:shadow-md">
      <h2 className="font-semibold text-gray-900">{title}</h2>

      <p className="mt-2 text-sm leading-6 text-gray-600">
        {description}
      </p>
    </div>
  );
}